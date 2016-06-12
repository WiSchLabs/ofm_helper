import configparser
import os


class ConfigurationProvider:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get(self, config_param):
        if os.environ.get(config_param):
            return os.environ[config_param]
        return self.config.get('configuration', config_param)
