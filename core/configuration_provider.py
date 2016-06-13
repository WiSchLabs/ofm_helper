import configparser
import os

from django.conf import settings


class ConfigurationProvider:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(settings.CONFIGURATION_FILE)

    def get(self, config_group, config_param, use_env_vars=True):
        if use_env_vars and os.environ.get(config_param):
            return os.environ[config_param]
        return self.config.get(config_group, config_param)