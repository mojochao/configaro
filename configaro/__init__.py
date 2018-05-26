"""Configaro configuration system.

This configuration system provides one that:
    - supports hierarchical configuration data
    - supports attribute dot-addressable access
    - supports defaults and local overrides
    - does not leak module imports into the configuration

"""
import ast
import os
import sys
from importlib import import_module
from importlib.abc import FileLoader, SourceLoader

__all__ = [
    'ConfigaroError',
    'ConfigNotFoundError',
    'ConfigNotValidError',
    'NotInitializedError',
    'PropertyNotFoundError',
    'PropertyNotScalarError',
    'get',
    'initialize',
    'put',
]


# ---------------------------------------------------------------------------
# Constants.
# ---------------------------------------------------------------------------

DEFAULT_LOCALS_ENV_VAR = 'CONFIGARO_LOCALS_MODULE'
DEFAULTS_CONFIG_MODULE = 'defaults'
LOCALS_CONFIG_MODULE = 'locals'


# ---------------------------------------------------------------------------
# Mutable global state.
# ---------------------------------------------------------------------------

_INITIALIZED = False
_CONFIG_DATA = {}
_CONFIG_PACKAGE = None
_LOCALS_ENV_VAR = None
_LOCALS_PATH = None


# ---------------------------------------------------------------------------
# Error types
# ---------------------------------------------------------------------------

class ConfigaroError(BaseException):
    """Base library exception class."""

    def __init__(self, message):
        self.message = message


class NotInitializedError(ConfigaroError):
    """Config file not found error."""

    def __init__(self):
        super().__init__(f'configaro uninitialized')


class ConfigNotFoundError(ConfigaroError):
    """Module not found error."""

    def __init__(self, path):
        super().__init__(f'module not found: {path}')
        self.path = path


class ConfigNotValidError(ConfigaroError):
    """Module does not contain a dict config attribute error."""

    def __init__(self, path):
        super().__init__(f'module missing config: {path}')
        self.path = path


class PropertyNotFoundError(ConfigaroError):
    """Config property not found error."""

    def __init__(self, data, prop):
        super().__init__(f'config property not found: {prop}')
        self.data = data
        self.prop = prop


class PropertyNotScalarError(ConfigaroError):
    """Config property not scalar error."""

    def __init__(self, data, prop):
        super().__init__(f'config property not scalar: {prop}')
        self.data = data
        self.prop = prop


# ---------------------------------------------------------------------------
# External API.
# ---------------------------------------------------------------------------

def initialize(config_package, locals_path=None, locals_env_var=None):
    """Initialize configaro library.

    The required *config_package* argument is used to define the package in
    which the defaults and (possibly) the locals config modules are loaded from.

    If the optional *locals_path* argument is provided it will be used instead
    of any locals config module in the config package.

    If the optional *locals_env_var* argument is provided it will be used as a
    an environment variable configuring the path of the locals config module to load.

    Repeated calls to this function return immediately.  You can not re-initialize
    with different values.

    Args:
        config_package (str): package containing defaults and locals config modules
        locals_path (str): path to locals config module
        locals_env_var (str): name of environment variable providing path to locals config module

    """
    global _INITIALIZED
    if not _INITIALIZED:
        global _CONFIG_PACKAGE
        _CONFIG_PACKAGE = config_package
        global _LOCALS_PATH
        _LOCALS_PATH = locals_path
        global _LOCALS_ENV_VAR
        _LOCALS_ENV_VAR = locals_env_var
        _INITIALIZED = True


def get(*props):
    """Get configuration values.

    If no configuration *props* are provided, returns the whole configuration.

    If one value is provided in *props*, returns that portion of the configuration.

    If multiple values are provided in *props*, returns a list of each portion of
    the configuration identified in *props*.

    Args:
        props (List[str]): configuration properties

    Returns:
        Any | Dict[str, Any]: config values

    Raises:
        configaro.NotInitialized: if library has not been initialized
        configaro.PropertyNotFoundError: if a prop in *props* is not found

    """
    _ensure_initialized()
    data = _config_data()
    if not props:
        return data
    elif len(props) == 1:
        return _get(data, props[0])
    else:
        return [_get(data, arg) for arg in props]


def put(*args, **kwargs):
    """Put configuration values.

    Args:
        args (List[str]): config 'some.knob=value' arguments
        kwargs (Dict[str, Any]): config someknob='value' arguments

    Raises:
        ValueError: if any arg in args is malformed
        configaro.NotInitializedError: if library has not been initialized
        configaro.PropertyNotScalarError: if property is not a scalar

    """
    _ensure_initialized()
    data = _config_data()

    # If the caller wishes to modify nested properties, they must be passed in as
    # property assignment strings, such as 'log.level=INFO'.
    for arg in args:
        name, value = arg.split('=')
        value = _cast(value)

        scopes = name.split('.')
        if len(scopes) > 1:
            config = get('.'.join(scopes[:-1]))
            name = scopes[-1]
        else:
            config = get()
        if isinstance(config[name], dict):
            raise PropertyNotScalarError(data, name)
        config[name] = value

    # If the caller doesn't care about nested properties, the top level property
    # names may be passed in keyword args, such as disable_auth=True.
    for name, value in kwargs.items():
        config = data
        if isinstance(config[name], dict):
            raise PropertyNotScalarError(data, name)
        config[name] = value


# ---------------------------------------------------------------------------
# Internal API
# ---------------------------------------------------------------------------

def _ensure_initialized():
    """Ensure library is initialized.

    Raises:
        configaro.NotInitializedError: if library has not been initialized

    """
    if not _INITIALIZED:
        raise NotInitializedError()


def _config_data():
    """Composed configuration data accessor.

    Returns:
        Dict[str, Any]: composed config data

    """
    global _CONFIG_DATA
    if not _CONFIG_DATA:
        for path in _config_module_paths():
            deltas = _load(path)
            merged = dict(_merge(_CONFIG_DATA, deltas))
            _CONFIG_DATA = merged
        from munch import munchify
        _CONFIG_DATA = munchify(_CONFIG_DATA)
    return _CONFIG_DATA


def _config_module_paths():
    """Configuration module paths accessor.

    Returns:
        List[str]: configuration module paths

    Raises:
        configaro.ConfigNotFoundError: if config file not found

    """
    config_paths = []
    package_dir = _config_package_dir()

    # Start by using 'defaults' module from the config package.
    defaults_path = os.path.join(package_dir, f'{DEFAULTS_CONFIG_MODULE}.py')
    if not os.path.exists(defaults_path):
        raise ConfigNotFoundError(defaults_path)
    config_paths.append(defaults_path)

    # Continue by adding 'locals' module.
    # One specified as file takes highest precedence.
    if _LOCALS_PATH:
        locals_path = _LOCALS_PATH
    # One specified in environment variable takes next highest precedence.
    elif _LOCALS_ENV_VAR:
        locals_path = os.environ.get(_LOCALS_ENV_VAR)
    # Finish if necessary by using 'locals' module in the config package.
    else:
        locals_path = os.path.join(package_dir, f'{LOCALS_CONFIG_MODULE}.py')
    if not os.path.exists(locals_path):
        raise ConfigNotFoundError(locals_path)
    config_paths.append(locals_path)

    return config_paths


def _config_package_dir():
    """Configuration package directory accessor.

    Returns:
        str: configuration package directory

    Raises:
        ImportError: if config package defaults cannot be loaded.

    """
    module = import_module('defaults', _CONFIG_PACKAGE)
    return os.path.dirname(module.__file__)


def _cast(value):
    """Cast string value to real type.

    Args:
        value (str): value to cast

    Returns:
        None | bool | int | float | str: casted value

    """
    # Handle None type values
    if value == 'None':
        return None
    # Handle Boolean type values
    if value == 'False':
        return False
    elif value == 'True':
        return True
    # Handle numeric type values.
    types = [int, float]
    for t in types:
        try:
            return t(value)
        except ValueError:
            pass
    # Must be a string.
    return value


def _get(data, prop):
    """Get data identified by property.

    Arg:
        prop (str): configuration property

    Returns:
        Any | Dict[str, Any]: config values

    Raises:
        configaro.PropertyNotFoundError: if property is not found

    """
    try:
        # NOTE: do not remove the 'data' parameter in function as it is used here
        return eval(f'data.{prop}')
    except AttributeError:
        raise PropertyNotFoundError(data, prop)


def _load(path):
    """Load configuration values from file.

    Args:
        path (str): config file path

    Returns:
        Dict[str, Any]: config data

    Raises:
        ImportError: if module cannot be imported
        configaro.ConfigNotValidError is module does not contain a 'config' dict attribute.

    """
    module_dir = os.path.dirname(path)
    module_name = os.path.basename(path).replace('.py', '')
    module = _import_module(module_dir, module_name)
    try:
        if not isinstance(module.config, dict):
            raise ConfigNotValidError(path)
        return module.config
    except AttributeError:
        raise ConfigNotValidError(path)


def _merge(original, deltas):
    """Merge two dictionaries.

    Args:
        original (dict): original data
        deltas (dict): deltas data

    Yields:
        Tuple[str, Any]: merged keys and values

    """
    for k in set(original.keys()).union(deltas.keys()):
        if k in original and k in deltas:
            if isinstance(original[k], dict) and isinstance(deltas[k], dict):
                yield k, dict(_merge(original[k], deltas[k]))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield k, deltas[k]
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in original:
            yield k, original[k]
        else:
            yield k, deltas[k]


def _import_module(module_dir, module_name):
    """Import module from directory.

    Args:
        module_dir (str): module directory
        module_name (str): module name

    Returns:
         module: imported module

    Raises:
        ImportError: if module cannot be imported

    """
    filename = _module_path(module_dir, module_name)
    if module_name in sys.modules:
        return sys.modules[module_name]
    return _ConfigLoader(module_name, filename).load_module(module_name)


def _module_path(module_dir, module_name):
    """Get module path..

    Args:
        module_dir (str): module directory
        module_name (str): module name

    Returns:
         module: module file path

    """
    filename = os.path.join(module_dir, *module_name.split('.'))
    return os.path.join(filename, '__init__.py') if os.path.isdir(filename) else f'{filename}.py'


class _ConfigLoader(FileLoader, SourceLoader):
    """Configuration module loader class."""

    def get_code(self, fullname):
        source = self.get_source(fullname)
        path = self.get_filename(fullname)
        parsed = ast.parse(source)
        return compile(parsed, path, 'exec', dont_inherit=True, optimize=0)

    def module_repr(self, module):
        return f'<config {module.__name__} from {module.__file__}>'
