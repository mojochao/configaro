import os

import munch
import pytest

CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config'))

SAMPLE_DATA = {
    'name': 'defaults',
    'log': {
        'file': 'some-file.txt',
        'level': 'ERROR'
    },
    'monitoring': {
        'haproxy': {
            'disabled': False
        },
        'nginx': {
            'disabled': True
        }
    }
}


# ---------------------------------------------------------------------------
# test internals
# ---------------------------------------------------------------------------

def test__module_path():
    from configaro import _module_path
    assert _module_path(CONFIG_DIR, 'defaults') == os.path.join(CONFIG_DIR, 'defaults.py')


def test__import_module():
    from configaro import _import_module
    module = _import_module(CONFIG_DIR, 'defaults')
    assert module.config == SAMPLE_DATA

    with pytest.raises(ImportError):
        _import_module(CONFIG_DIR, 'default')


def test__merge():
    from configaro import _merge
    defaults = SAMPLE_DATA
    locals = {
        'name': 'locals',
        'log': {
            'level': 'DEBUG'
        },
        'monitoring': {
            'haproxy': {
                'disabled': True
            }
        }
    }
    expected = {
        'name': 'locals',
        'log': {
            'file': 'some-file.txt',
            'level': 'DEBUG'
        },
        'monitoring': {
            'haproxy': {
                'disabled': True
            },
            'nginx': {
                'disabled': True
            }
        }
    }
    merged = dict(_merge(defaults, locals))
    assert merged == expected


def test__load():
    from configaro import _load, _module_path
    path = _module_path(CONFIG_DIR, 'defaults')
    config = _load(path)
    assert config['name'] == 'defaults'


def test__cast():
    from configaro import _cast
    assert _cast('None') is None
    assert isinstance(_cast('False'), bool)
    assert isinstance(_cast('1'), int)
    assert isinstance(_cast('1.234'), float)
    assert isinstance(_cast('Hello'), str)


def test__get():
    from configaro import PropertyNotFoundError, _get
    data = munch.munchify(SAMPLE_DATA)
    assert _get(data, 'name') == 'defaults'
    assert _get(data, 'log.level') == 'ERROR'
    assert _get(data, 'monitoring.haproxy.disabled') is False
    assert _get(data, 'monitoring.nginx.disabled') is True
    with pytest.raises(PropertyNotFoundError):
        assert _get(data, 'monitoring.nginx.disable') is True
    assert _get(data, 'monitoring.nginx.disable', default=None) is None


def test__put():
    from configaro import _get, _put
    data = munch.munchify(SAMPLE_DATA)
    _put(data, 'name', 'locals')
    assert _get(data, 'name') == 'locals'
    _put(data, 'log.level', 'DEBUG')
    assert _get(data, 'log.level') == 'DEBUG'


def test__config_package_dir():
    from configaro import _config_package_dir
    assert _config_package_dir() == CONFIG_DIR


def test___config_module_paths():
    from configaro import _config_module_paths
    expected = [
        os.path.join(CONFIG_DIR, 'defaults.py'),
        os.path.join(CONFIG_DIR, 'locals.py'),
    ]
    paths = _config_module_paths()
    assert sorted(paths) == sorted(expected)


def test__config_data():
    from configaro import _config_data
    data = _config_data()
    assert data
    assert isinstance(data, dict)


def test__ensure_initialized():
    from configaro import NotInitializedError, init, _ensure_initialized
    with pytest.raises(NotInitializedError):
        _ensure_initialized()
    init('tests.config')
    _ensure_initialized()


# ---------------------------------------------------------------------------
# test public interface
# ---------------------------------------------------------------------------


def test_exports():
    from configaro import __all__ as exports
    expected = [
        'ConfigaroError',
        'ConfigNotFoundError',
        'ConfigNotValidError',
        'NotInitializedError',
        'PropertyNotFoundError',
        'PropertyNotScalarError',
        'UpdateNotValidError',
        'get',
        'init',
        'put',
    ]
    assert sorted(exports) == sorted(expected)


def test_initialize():
    from configaro import init
    init('tests.config')


def test_get():
    from configaro import PropertyNotFoundError, get, init
    init('tests.config')
    expected = {
        'name': 'locals',
        'log': {
            'file': 'some-file.txt',
            'level': 'DEBUG'
        },
        'monitoring': {
            'haproxy': {
                'disabled': True
            },
            'nginx': {
                'disabled': True
            }
        }
    }
    config = get()
    assert config.log.level == 'DEBUG'
    assert config == munch.munchify(expected)
    log = get('log')
    assert log.level == 'DEBUG'
    log = munch.unmunchify(log)
    assert log == expected['log']
    assert get('name') == 'locals'
    assert get('log.level') == 'DEBUG'
    assert get('monitoring.haproxy.disabled') is True
    assert get('monitoring.nginx.disabled') is True
    with pytest.raises(PropertyNotFoundError):
        assert get('monitoring.nginx.disable') is True
    assert get('monitoring.nginx.disable', default=None) is None


def test_put():
    from configaro import PropertyNotScalarError, UpdateNotValidError, get, init, put
    init('tests.config')
    put('log.level=INFO')
    config = get()
    assert config.log.level == 'INFO'
    # ensure that we cannot put with a malformed arg
    with pytest.raises(UpdateNotValidError):
        put('log.level')
    # ensure that we cannot put a non-scalar
    with pytest.raises(PropertyNotScalarError):
        put('log=INFO')


def test_ConfigaroError():
    from configaro import ConfigaroError
    message = 'this is an error'
    error = ConfigaroError(message)
    assert error.message == message


def test_NotInitializedError():
    from configaro import ConfigaroError, NotInitializedError
    error = NotInitializedError()
    assert isinstance(error, ConfigaroError)
    assert error.message == 'configaro library uninitialized'


def test_ConfigNotFoundError():
    from configaro import ConfigaroError, ConfigNotFoundError
    path = '/some/path'
    error = ConfigNotFoundError(path)
    assert isinstance(error, ConfigaroError)
    assert error.message == f'config module not found: {path}'
    assert error.path == path
    path = '/another/path'
    error = ConfigNotFoundError(path=path)
    assert error.path == path


def test_ConfigNotValidError():
    from configaro import ConfigaroError, ConfigNotValidError
    path = '/some/path'
    error = ConfigNotValidError(path)
    assert isinstance(error, ConfigaroError)
    assert error.message == f'config module not valid: {path}'
    assert error.path == path
    error = ConfigNotValidError(path=path)
    assert error.path == path


def test_PropertyNotFoundError():
    from configaro import ConfigaroError, PropertyNotFoundError
    data = None
    prop_name = 'prop.inner'
    error = PropertyNotFoundError(data, prop_name)
    assert isinstance(error, ConfigaroError)
    assert error.message == f'config property not found: {prop_name}'
    assert error.data == data
    assert error.prop_name == prop_name
    error = PropertyNotFoundError(prop_name=prop_name, data=data)
    assert error.data == data
    assert error.prop_name == prop_name


def test_PropertyNotScalarError():
    from configaro import ConfigaroError, PropertyNotScalarError
    data = None
    prop_name = 'prop.inner'
    error = PropertyNotScalarError(data, prop_name)
    assert isinstance(error, ConfigaroError)
    assert error.message == f'config property not scalar: {prop_name}'
    assert error.data == data
    assert error.prop_name == prop_name
    error = PropertyNotScalarError(prop_name=prop_name, data=data)
    assert error.data == data
    assert error.prop_name == prop_name


def test_UpdateNotValidError():
    from configaro import ConfigaroError, UpdateNotValidError
    update = 'prop=value'
    error = UpdateNotValidError(update)
    assert isinstance(error, ConfigaroError)
    assert error.message == f'config update not valid: {update}'
    assert error.update == update
    error = UpdateNotValidError(update=update)
    assert error.update == update
