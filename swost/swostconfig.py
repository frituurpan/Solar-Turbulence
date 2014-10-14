import ConfigParser
import arrow

__author__ = 'frituurpan'


class SwostConfig:
    """
    Read config file and publish the settings
    No magic please
    """

    configParser = -1
    configBlockName = 'config'
    dbConfigBlockName = 'database'

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

    def get_timezone(self):
        return self.get_config().get(self.configBlockName, 'timezone')

    def get_current_timezone_stamp(self):
        utc = arrow.utcnow()
        local = utc.to(self.get_timezone())
        locform = local.format('YYYY-MM-DD HH:mm:ss')
        locutc = arrow.get(locform, 'YYYY-MM-DD HH:mm:ss')
        return locutc.timestamp

    def get_db_host(self):
        return self.get_config().get(self.dbConfigBlockName, 'host')

    def get_db_type(self):
        return self.get_config().get(self.dbConfigBlockName, 'type')

    def get_db_user(self):
        return self.get_config().get(self.dbConfigBlockName, 'user')

    def get_db_password(self):
        return self.get_config().get(self.dbConfigBlockName, 'password')

    def get_db_database(self):
        return self.get_config().get(self.dbConfigBlockName, 'database')