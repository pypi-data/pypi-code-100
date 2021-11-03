from os import environ, makedirs


user = environ.get('USER')
dest = environ.get('setux_logdir', '/tmp/setux/log')
dest = f'{dest}/{user}'
makedirs(dest, exist_ok=True)


config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'stdout': {
            'format': '%(message)s'
        },
        'short': {
            'datefmt': '%H:%M',
            'format': '%(asctime)s %(levelname)-7s %(message)s'
        },
        'full': {
            'datefmt': '%H:%M:%S',
            'format': '%(levelno)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'debug': {
            'class': 'logging.FileHandler',
            'filename': f'{dest}/setux_debug.log',
            'formatter': 'full',
            'level': 'DEBUG',
            'mode': 'w'
        },
        'info': {
            'class': 'logging.FileHandler',
            'filename': f'{dest}/setux_info.log',
            'formatter': 'short',
            'level': 'INFO',
            'mode': 'w'
        },
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'stdout',
            'level': 'INFO'
        },
        'pybrary': {
            'class': 'logging.FileHandler',
            'filename': f'{dest}/pybrary.log',
            'formatter': 'full',
            'mode': 'w'
        },
    },
    'loggers': {
        'Setux': {
            'handlers': ['debug', 'info', 'stdout'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'Deploy': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
        'Pybrary': {
            'handlers': ['pybrary'],
            'level': 'NOTSET',
            'propagate': False,
        },
    },
}
