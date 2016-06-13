from ofm_helper.common_settings import *

DEBUG = False

CONFIGURATION_FILE = os.path.join(CONFIGURATION_BASE_PATH, 'prod.cfg')

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/code/staticfiles/'
