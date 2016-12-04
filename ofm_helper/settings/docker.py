from ofm_helper.common_settings import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# DB
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'postgres',
         'USER': 'postgres',
         'HOST': 'db',
         'PORT': 5432,
     }
 }

# CACHING
CACHE_HOST = 'redis'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    }
}

# Now we can use our super fast redis as session store
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# LOGGING
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

# PHANTOMJS
PHANTOMJS_REMOTE = True
PHANTOMJS_HOST = 'phantomjs'
