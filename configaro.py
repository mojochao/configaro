"""**configaro** is a Python 3 configuration library that's music to your ears.

It has been created with the following design goals in mind:

    - provide a single file library with minimal dependencies
    - provide one with a simple, expressive API that is easy to use and gets out of your way
    - provide one that allows for hierarchical config data supporting dot-addressable access
    - provide one that allows for defaults and locals config modules
    - provide one with complete test coverage
    - provide one with complete documentation

If this sounds appealing to you, take a look::

    import configaro as cfg

    # Initialize the library with the name of the package containing your defaults.py config module
    cfg.init('mypkg.config')

    # Get the entire config object
    config = cfg.get()
    print(config)  # prints "{'greeting': 'Hello', 'subject': 'World'}"

    # Config object provide attribute access style in addition to dict access style.
    print('f{config.greeting}, {config.subject}!')  # prints "Hello, World!"

    # Config objects may be updated quite flexibly as well.
    cfg.put(greeting='Goodbye', subject='Folks'}
    cfg.put({'greeting': 'Goodbye', 'subject': 'Folks'})
    cfg.put('greeting=Goodbye subject=Folks')

"""
import ast
import os
import sys
from importlib import import_module
from importlib.abc import FileLoader, SourceLoader
from types import CodeType, ModuleType
from typing import Any, List, Tuple, Union

from munch import Munch, munchify

__all__ = [
    'ConfigError',
    'ConfigModuleNotFoundError',
    'ConfigModuleNotValidError',
    'ConfigObjectNotInitialized',
    'ConfigPropertyNotFoundError',
    'ConfigPropertyNotScalarError',
    'ConfigUpdateNotValidError',
    'get',
    'init',
    'put',
]


DEFAULTS_CONFIG_MODULE_NAME = 'defaults'
LOCALS_CONFIG_MODULE_NAME = 'locals'
LOCALS_ENV_VAR = 'CONFIGARO_LOCALS_MODULE'

_CONFIG_DATA = munchify({})


class ConfigError(BaseException):
    """Base library exception class."""

    def __init__(self, message: str=None):
        self.message = message


class ConfigObjectNotInitialized(ConfigError):
    """Config object not initialized error."""

    def __init__(self):
        super().__init__('config object not initialized')


class ConfigModuleNotFoundError(ConfigError):
    """Config module not found error."""

    def __init__(self, path: str=None):
        super().__init__(f'config module not found: {path}')
        self.path = path


class ConfigModuleNotValidError(ConfigError):
    """Config module does not contain a 'config' attribute of 'dict' type error."""

    def __init__(self, path: str=None):
        super().__init__(f'config module not valid: {path}')
        self.path = path


class ConfigPropertyNotFoundError(ConfigError):
    """Config property not found error."""

    def __init__(self, data: Munch=None, prop_name: str=None):
        super().__init__(f'config property not found: {prop_name}')
        self.data = data
        self.prop_name = prop_name


class ConfigPropertyNotScalarError(ConfigError):
    """Config property not scalar error."""

    def __init__(self, data: Munch=None, prop_name: str=None):
        super().__init__(f'config property not scalar: {prop_name}')
        self.data = data
        self.prop_name = prop_name


class ConfigUpdateNotValidError(ConfigError):
    """Config update not valid error."""

    def __init__(self, update: str=None):
        super().__init__(f'config update not valid: {update}')
        self.update = update


def init(config_package: str, locals_path: str=None, locals_env_var: str=LOCALS_ENV_VAR):
    """Initialize the config object.

    The config object must be initialized before use and is built from one or
    two config modules.  A config module is simply any Python module with a
    module attribute named **config**.  The config object loaded from the
    **defaults** config module, as well as any **locals** config module found.

    The **defaults** config module is always loaded.  The required *config_package*
    argument is used to define the package in which the **defaults** config
    module, named ``defaults.py``, is loaded from::

        init('my_pkg.config')

    The **locals** config module is loaded, next if it exists, from the following
    locations, in precedence order from highest to lowest::

    - one found at path specified by locals env var
    - one found at path specified by locals path
    - one found in config package

    If no other options are provided, the **locals** config module will be loaded,
    if it exists, from the *config_package*.

    If the optional *locals_path* argument is provided it will be used, if it
    exists, instead of any ``locals.py`` config module in the config package::

        init('my_pkg.config', locals_path='/path/to/my/alternatively_named_locals.py')

    If the optional *locals_env_var* argument is provided it will be used as a
    an environment variable configuring the path of the locals config module to
    load, if the module exists::

        init('my_pkg.config', locals_env_var='MY_PKG_CONFIG_LOCALS')

    If the *locals_env_var* argument is not provided the ``CONFIGARO_LOCALS``
    environment variable name will be used instead.

    Repeated initialization has no effect.  You can not re-initialize with
    different values.

    Args:
        config_package: package containing defaults and locals config modules
        locals_path: path to locals config module
        locals_env_var: name of environment variable providing path to locals config module

    """
    global _CONFIG_DATA
    if _CONFIG_DATA:
        return

    for path in _config_module_paths(config_package, locals_path, locals_env_var):
        deltas = _load(path)
        merged = dict(_merge(_CONFIG_DATA, deltas))
        _CONFIG_DATA = merged
    _CONFIG_DATA = munchify(_CONFIG_DATA)


def get(*prop_names: str, **kwargs: str) -> Tuple[Union[Munch, Any]]:
    """Query config values in config object.

    The config object must be initialized before use.

    If no *prop_names* are provided, returns the config root config object::

        config = get()

    If one property name is provided, returns that sub config object::

        prop = get('prop')

    If multiple property names are provided, returns a tuple of sub config objects::

        prop1, prop2 = get('prop1', 'prop2')

    Multiple property names can also be provided in a single string argument as well::

        prop1, prop2 = get('prop1 prop2')

    If a property name is not found, configaro.ConfigPropertyNotFoundError is raised,
    unless a *default* keyword argument is provided::

        prop = get('prop', default=None)

    Args:
        prop_names: config property names
        kwargs: config get keyword args

    Returns:
        property values

    Raises:
        configaro.NotInitialized: if library has not been initialized
        configaro.ConfigPropertyNotFoundError: if a property in *prop_names* is not found

    """
    if not _CONFIG_DATA:
        raise ConfigObjectNotInitialized()

    if not prop_names:
        return _CONFIG_DATA
    elif len(prop_names) == 1:
        return _get(_CONFIG_DATA, prop_names[0], **kwargs)
    else:
        return tuple([_get(_CONFIG_DATA, arg, **kwargs) for arg in prop_names])


def put(*args: str, **kwargs: str):
    """Modify config values in config object.

    The config object must be initialized before use.

    This function supports many expressive styles of usage.

    The entire config object can be updated with a single dict data argument::

        put({'prop_a': True, 'prop_b': 23})

    Similarly, any sub config object can be updated with a string property and
    dict data argument::

        put(prop={'prop_a': True, 'prop_b': 23})
        put('nested.prop', {'prop_a': True, 'prop_b': 23})

    Updates can also be specified by ``name=value`` update strings.  If one or
    more string arguments are passed, the updates described by those update
    strings will be applied to the config object::

        put('prop_a=True')
        put('prop_b=23')

    Update strings allow hierarchical configs to be updated::

        put('prop.nested=awesome')

    You can also batch up multiple updates in a single update string::

        put('prop_a=True prop.nested=awesome')

    If you are updating root config properties you can simply use keyword
    arguments::

        put(prop_a=True, prop_d={'greeting': 'Hello', 'subject': 'world'})

    Args:
        args: config dict object or one or more 'some.knob=value' update strings
        kwargs: config update keyword args

    Raises:
        configaro.ConfigObjectNotInitialized: if library has not been initialized
        configaro.ConfigPropertyNotScalarError: if property is not a scalar
        configaro.ConfigUpdateNotValidError: if update string is not valid

    """
    if not _CONFIG_DATA:
        raise ConfigObjectNotInitialized()

    # Handle passing in a single dict arg.
    if len(args) == 1 and isinstance(args[0], dict):
        _CONFIG_DATA.update(args[0])
        return

    # Handle passing in a prop name and an update value of any sort other than string.
    if len(args) == 2 and isinstance(args[0], str) and not isinstance(args[1], str):
        _put(_CONFIG_DATA, args[0], args[1])
        return

    # Handle positional string arguments.  If the caller wishes to modify
    # nested properties, they must be passed in as update strings, such as
    # 'log.level=INFO'.  Values will be cast from strings to their appropriate
    # type.  Multiple updates can be specified in a single string separated by
    # whitespace.
    if len(args) == 1 and isinstance(args[0], str):
        args = args[0].split()
    for arg in args:
        try:
            name, value = arg.split('=')
            value = _cast(value)
            _put(_CONFIG_DATA, name, value)
        except ValueError:
            raise ConfigUpdateNotValidError(arg)

    # Handle any keyword arguments.  If the caller doesn't care about nested
    # property updates, property names and values may be passed in keyword args.
    for name, value in kwargs.items():
        _put(_CONFIG_DATA, name, value)


def _config_module_paths(config_package: str, locals_path: str=None, locals_env_var: str=LOCALS_ENV_VAR) -> List[str]:
    """Config module paths accessor.

    Returns:
        config module paths

    Raises:
        configaro.ConfigModuleNotFoundError: if config file not found

    """
    config_paths = []
    package_dir = _config_package_dir(config_package)

    # Start by using 'defaults' module from the config package.
    defaults_path = os.path.join(package_dir, f'{DEFAULTS_CONFIG_MODULE_NAME}.py')
    if not os.path.exists(defaults_path):
        raise ConfigModuleNotFoundError(defaults_path)
    config_paths.append(defaults_path)

    # Continue by adding any 'locals' module.
    if not locals_path:
        locals_path = os.environ.get(locals_env_var) or os.path.join(package_dir, f'{LOCALS_CONFIG_MODULE_NAME}.py')
    if locals_path:
        if not os.path.exists(locals_path):
            raise ConfigModuleNotFoundError(locals_path)
        config_paths.append(locals_path)
    return config_paths


def _config_package_dir(config_package: str) -> str:
    """Config package directory accessor.

    Returns:
        config package directory

    Raises:
        ImportError: if config package defaults cannot be loaded.

    """
    module = import_module('defaults', config_package)
    return os.path.dirname(module.__file__)


def _cast(value: str) -> Union[None, bool, int, float, str]:
    """Cast string value to real type.

    Args:
        value: value to cast

    Returns:
        casted value

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


def _get(data: Munch, prop_name: str, **kwargs: str) -> Union[Munch, Any]:
    """Get config value identified by config property in config data.


    Arg:
        data: config data
        prop_name: config property name
        kwargs: keyword arguments

    Returns:
        config value

    Raises:
        configaro.ConfigPropertyNotFoundError: if property is not found and *default* keyword arg is not present

    """
    try:
        return eval(f'data.{prop_name}')  # NOTE: do not remove the 'data' parameter in function as it is used here!
    except AttributeError:
        try:
            return kwargs['default']
        except KeyError:
            raise ConfigPropertyNotFoundError(data, prop_name)


def _put(data: Munch, prop_name: str, prop_value=Any):
    """Put config value identified by config property in config data.

    Arg:
        data: config data
        prop_name: config property name
        prop_value: config value

    Raises:
        configaro.ConfigPropertyNotFoundError: if config property is not found
        configaro.ConfigPropertyNotScalarError: if config property is not scalar and non-dict value is provided

    """
    from munch import Munch
    prop_parts = prop_name.split('.')
    if len(prop_parts) > 1:
        parent_prop_name = '.'.join(prop_parts[:-1])
        prop_name = prop_parts[-1]
        config = _get(data, parent_prop_name)
    else:
        config = data
    if isinstance(config[prop_name], Munch) and not isinstance(prop_value, dict):
        raise ConfigPropertyNotScalarError(config, prop_name)
    config[prop_name] = prop_value


def _load(path: str) -> dict:
    """Load config values from file.

    Args:
        path: config file path

    Returns:
        config data

    Raises:
        ImportError: if module cannot be imported
        configaro.ConfigModuleNotValidError is module does not contain a 'config' dict attribute.

    """
    module_dir = os.path.dirname(path)
    module_name = os.path.basename(path).replace('.py', '')
    module = _import_module(module_dir, module_name)
    try:
        if not isinstance(module.config, dict):
            raise ConfigModuleNotValidError(path)
        return module.config
    except AttributeError:
        raise ConfigModuleNotValidError(path)


def _merge(original: dict, deltas: dict) -> Tuple[str, Any]:
    """Merge two dictionaries.

    Args:
        original: original data
        deltas: deltas data

    Yields:
        merged keys and values

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


def _import_module(module_dir: str, module_name: str) -> ModuleType:
    """Import module from directory.

    Args:
        module_dir: module directory path
        module_name: name of module to import from *module_dir*

    Returns:
         imported module

    Raises:
        ImportError: if module cannot be imported

    """
    filename = _module_path(module_dir, module_name)
    if module_name in sys.modules:
        return sys.modules[module_name]
    return _ConfigLoader(module_name, filename).load_module(module_name)


def _module_path(module_dir: str, module_name: str) -> str:
    """Get module path..

    Args:
        module_dir: module directory
        module_name: module name

    Returns:
         module file path

    """
    filename = os.path.join(module_dir, *module_name.split('.'))
    return os.path.join(filename, '__init__.py') if os.path.isdir(filename) else f'{filename}.py'


class _ConfigLoader(FileLoader, SourceLoader):
    """Config module loader class."""

    def get_code(self, fullname: str) -> CodeType:
        source = self.get_source(fullname)
        path = self.get_filename(fullname)
        parsed = ast.parse(source)
        return compile(parsed, path, 'exec', dont_inherit=True)

    def module_repr(self, module: ModuleType):
        return f'<config module {module.__name__} at {module.__file__}>'
