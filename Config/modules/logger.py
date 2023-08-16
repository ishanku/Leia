import environ
from Config.basepath import *

env = environ.Env()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(filename)s %(funcName)s %(message)s"
        },
            "non-verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                          "%(funcName)s %(message)s"
            }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "Leia.General": {
            "level": "DEBUG",
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/general.log',
            'maxBytes': 1024 * 500,
            'backupCount': 5,
            "formatter": "verbose",
        }

    },
    "root": {"level": "INFO", "handlers": ["console", "Leia.General"]},
    'loggers': {
        'django': {
            'handlers': ['console', 'Leia.General'],
            'level': env("DJANGO_LOG_LEVEL"),
            'propagate': False,
        },
    },
}