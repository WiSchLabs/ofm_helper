from ofm_helper.common_settings import *

DEBUG = True

ALLOWED_HOSTS = ['*']

LOGGING['handlers']['console']['level'] = 'INFO'
LOGGING['loggers']['django']['level'] = 'INFO'
