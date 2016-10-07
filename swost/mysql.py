import arrow

__author__ = 'Administrator'

import MySQLdb


class MySQL:
    conn = ''
    x = ''
    table = 'log'
    usageTable = 'usage'

    config = {}

    createTable = "CREATE TABLE `log` (`time` timestamp DEFAULT CURRENT_TIMESTAMP,`offset` tinyint(1) unsigned DEFAULT NULL,`node` smallint(2) unsigned DEFAULT NULL,`value1` int(10) unsigned DEFAULT NULL,`value2` int(10) unsigned DEFAULT NULL,`value3` int(10) unsigned DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1;"
    createUsageTable = "CREATE TABLE `usage` (`id` int(10) unsigned NOT NULL AUTO_INCREMENT, `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, `el_high` mediumint(10) unsigned NOT NULL, `el_low` mediumint(10) unsigned NOT NULL, `gas` mediumint(10) unsigned NOT NULL, PRIMARY KEY (`id`), UNIQUE KEY `time` (`time`)) ENGINE=InnoDB DEFAULT CHARSET=latin1"

    def open(self, host, user, password, database):

        self.config = {
            'host': host,
            'user': user,
            'passwd' : password,
            'db' : database
        }

        self.connect(self.config)

    def connect(self, config):
        conn = MySQLdb.connect(host=config['host'],
                               user=config['user'],
                               passwd=config['passwd'],
                               db=config['db'])

        x = conn.cursor()
        self.conn = conn
        self.x = x
        self.check_table()

    def check_table(self):
        check_sql = 'SHOW TABLES LIKE "' + self.table + '"'
        exits = False
        self.x.execute(check_sql)
        for _ in self.x:
            exits = True

        if not exits:
            self.x.execute(self.createTable)
            self.x.execute(self.createUsageTable)


    def close(self):
        self.conn.close()

    def log(self, offset, node, value1, value2, value3):
        value1 = value1 * 1000
        value2 = value2 * 1000
        value3 = value3 * 1000
        try:
            utc = arrow.utcnow()
            utc.to('Europe/Amsterdam')
            stamp = utc.format('YYYY-MM-DD HH:mm:ss')
            self.x.execute("""INSERT INTO """ + self.table + """(`time`, `offset`, `node`, `value1`, `value2`, `value3`) VALUES (%s,%s,%s,%s,%s,%s)""",
                           (stamp, offset, node, value1, value2, value3))
            self.conn.commit()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect(self.config)
        except StandardError, e:
            print e
            self.conn.rollback()


    def logRaw(self, el_normal, el_low, el_usage, gas):

        try:
            utc = arrow.utcnow()
            utc.to('Europe/Amsterdam')
            stamp = utc.format('YYYY-MM-DD HH:mm:ss')
            self.x.execute("""INSERT INTO `""" + self.usageTable + """` (`time`, `el_normal`, `el_low`, `el_usage`, `gas`) VALUES (%s,%s,%s,%s,%s)""",
                           (stamp, el_normal, el_low, el_usage, gas))
            self.conn.commit()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect(self.config)
        except StandardError, e:
            print e
            self.conn.rollback()