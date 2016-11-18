from ofm_helper.common_settings import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'postgres',
         'USER': 'postgres',
         'HOST': 'db',
         'PORT': 5432,
     }
 }

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

PHANTOMJS_REMOTE = True
PHANTOMJS_HOST = 'phantomjs'
