import ConfigParser

__author__ = 'frituurpan'


class SwostConfig:
    """
    Read config file and publish the settings
    No magic please
    """

    configParser = -1
    configBlockName = 'config'

    def __init__(self, config_file_path):
        config_parser = ConfigParser.RawConfigParser()
        config_parser.read(config_file_path)
        self.configParser = config_parser

    def get_config(self):
        return self.configParser

    def get_post_url(self):
        return self.get_config().get(self.configBlockName, 'post_url')

    def get_api_key(self):
        return self.get_config().get(self.configBlockName, 'api_key')

    def debug(self):
        return self.get_config().getboolean(self.configBlockName, 'debug')

    def get_port(self):
        if self.debug():
            return self.get_debug_port()
        return self.get_production_port()

    def get_production_port(self):
        return self.get_config().get(self.configBlockName, 'port')

    def get_debug_port(self):
        return self.get_config().get(self.configBlockName, 'debug_port')