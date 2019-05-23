import os
from clientmanagement.settings.base import BASE_DIR

LOG_ROOT = BASE_DIR +'/logs'
CLIENTMANAGEMENT_VERSION = '1.7.0'
USE_TZ = True
TIME_ZONE = "America/New_York"
TICKET_FILES = os.path.join(os.path.abspath("."), "uploads", "tickets")
TOOLS_FILES = os.path.join(os.path.abspath("."), "uploads", "tools")
CLIENT_FILES = os.path.join(os.path.abspath("."), "uploads", "clients")
MEDIA_ROOT = os.path.join(os.path.abspath("."), "uploads")
IMAGE_FILE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.ico', '.gif', '.bmp']
VERSION_STATIC_FILES = False
DEFAULT_API_KEY_LENGTH = None
DEFAULT_API_EXPIRATION_PERIOD_DAYS = 7

ENABLE_MAIL_CHECK = True
SEND_EMAILS_ON_NEW_TICKET_CREATED_AUTOMATICALLY = True
SEND_EMAILS_ON_NEW_TICKET_MANUAL = True
SEND_EMAILS_TEAM_ON_TICKET_CREATE_TO_SUPPORT = True

LINK_TOOL_STRING_LENGTH = 25
CANCEL_CAPTCHA = False
LOG_SIZE = 10000000
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'logging.NullHandler',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'logfile-django': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/application_main.log",
            'maxBytes': LOG_SIZE,
            'backupCount': 2,
            'formatter': 'verbose',
        },
        'logfile-error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/application_error.log",
            'maxBytes': LOG_SIZE,
            'backupCount': 2,
            'formatter': 'verbose',
        },
        'logfile-template': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/template.log",
            'maxBytes': LOG_SIZE,
            'backupCount': 2,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django.template': {
            'handlers': ['logfile-template'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['logfile-error', 'console'],
            'level': 'ERROR',
        },
        'django': {
            'handlers': ['null', ],
        },
        'py.warnings': {
            'handlers': ['null', ],
        },
        '': {
            'handlers': ['logfile-django', 'logfile-error'],
            'level': "DEBUG",
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(module)s %(name)-1s:%(lineno)d %(levelname)-5s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)-1s:%(lineno)d %(message)s'
        },
    },

    'logfile': {
        'level':'DEBUG',
        'class':'logging.handlers.RotatingFileHandler',
        'filename': LOG_ROOT + "/logfile",
        'maxBytes': 1000000,
        'backupCount': 5,
        'formatter': 'verbose',
    },
}

