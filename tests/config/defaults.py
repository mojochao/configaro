__all__ = ['config']

config = {
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
