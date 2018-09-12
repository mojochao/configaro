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
    from configaro import ConfigPropertyNotFoundError, _get
    data = munch.munchify(SAMPLE_DATA)
    assert _get(data, 'name') == 'defaults'
    assert _get(data, 'log.level') == 'ERROR'
    assert _get(data, 'monitoring.haproxy.disabled') is False
    assert _get(data, 'monitoring.nginx.disabled') is True
    with pytest.raises(ConfigPropertyNotFoundError):
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
    assert _config_package_dir('tests.config') == CONFIG_DIR


def test___config_module_paths():
    from configaro import _config_module_paths
    expected = [
        os.path.join(CONFIG_DIR, 'defaults.py'),
        os.path.join(CONFIG_DIR, 'locals.py'),
    ]
    paths = _config_module_paths('tests.config')
    assert sorted(paths) == sorted(expected)


def test_exports():
    from configaro import __all__ as exports
    expected = [
        'ConfigError',
        'ConfigModuleNotFoundError',
        'ConfigModuleNotValidError',
        'ConfigObjectNotInitializedError',
        'ConfigPropertyNotFoundError',
        'ConfigPropertyNotScalarError',
        'ConfigUpdateNotValidError',
        'get',
        'init',
        'put',
    ]
    assert sorted(exports) == sorted(expected)


def test_init():
    from configaro import init
    init('tests.config')


def test_get():
    from configaro import ConfigPropertyNotFoundError, get, init
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
    with pytest.raises(ConfigPropertyNotFoundError):
        assert get('monitoring.nginx.disable') is True
    assert get('monitoring.nginx.disable', default=None) is None


def test_put():
    from configaro import ConfigPropertyNotScalarError, ConfigUpdateNotValidError, get, init, put
    init('tests.config')
    put('log.level=INFO')
    config = get()
    assert config.log.level == 'INFO'
    # ensure that we cannot put with a malformed arg
    with pytest.raises(ConfigUpdateNotValidError):
        put('log.level')
    # ensure that we cannot put a non-scalar
    with pytest.raises(ConfigPropertyNotScalarError):
        put('log=INFO')


def test_ConfigaroError():
    from configaro import ConfigError
    message = 'this is an error'
    error = ConfigError(message)
    assert error.message == message


def test_NotInitializedError():
    from configaro import ConfigError, ConfigObjectNotInitializedError
    error = ConfigObjectNotInitializedError()
    assert isinstance(error, ConfigError)
    assert error.message == 'config object not initialized'


def test_ConfigNotFoundError():
    from configaro import ConfigError, ConfigModuleNotFoundError
    path = '/some/path'
    error = ConfigModuleNotFoundError(path)
    assert isinstance(error, ConfigError)
    assert error.message == f'config module not found: {path}'
    assert error.path == path
    path = '/another/path'
    error = ConfigModuleNotFoundError(path=path)
    assert error.path == path


def test_ConfigNotValidError():
    from configaro import ConfigError, ConfigModuleNotValidError
    path = '/some/path'
    error = ConfigModuleNotValidError(path)
    assert isinstance(error, ConfigError)
    assert error.message == f'config module not valid: {path}'
    assert error.path == path
    error = ConfigModuleNotValidError(path=path)
    assert error.path == path


def test_PropertyNotFoundError():
    from configaro import ConfigError, ConfigPropertyNotFoundError
    data = None
    prop_name = 'prop.inner'
    error = ConfigPropertyNotFoundError(data, prop_name)
    assert isinstance(error, ConfigError)
    assert error.message == f'config property not found: {prop_name}'
    assert error.data == data
    assert error.prop_name == prop_name
    error = ConfigPropertyNotFoundError(prop_name=prop_name, data=data)
    assert error.data == data
    assert error.prop_name == prop_name


def test_PropertyNotScalarError():
    from configaro import ConfigError, ConfigPropertyNotScalarError
    data = None
    prop_name = 'prop.inner'
    error = ConfigPropertyNotScalarError(data, prop_name)
    assert isinstance(error, ConfigError)
    assert error.message == f'config property not scalar: {prop_name}'
    assert error.data == data
    assert error.prop_name == prop_name
    error = ConfigPropertyNotScalarError(prop_name=prop_name, data=data)
    assert error.data == data
    assert error.prop_name == prop_name


def test_UpdateNotValidError():
    from configaro import ConfigError, ConfigUpdateNotValidError
    update = 'prop=value'
    error = ConfigUpdateNotValidError(update)
    assert isinstance(error, ConfigError)
    assert error.message == f'config update not valid: {update}'
    assert error.update == update
    error = ConfigUpdateNotValidError(update=update)
    assert error.update == update
