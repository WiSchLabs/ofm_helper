from ofm_helper.common_settings import *

DEBUG = True

USE_DISPLAY_FOR_AWS = True

ALLOWED_HOSTS = ['*']

LOGGING['loggers']['django']['handlers'] = ['file']
