from ofm_helper.common_settings import *

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/code/staticfiles/'

LOGGING['handlers']['file'] = {
    'level': 'ERROR',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': 'logs/error.log',
    'backupCount': 3,
    'maxBytes': 1024 * 1024 * 5,  # 5MB
    'formatter': 'standard'
}

LOGGING['loggers']['django']['handlers'] = ['file', 'console']
LOGGING['loggers']['django.request']['handlers'] = ['file', 'console']
