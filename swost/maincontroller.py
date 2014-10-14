import Queue
from requests import ConnectionError
import time
from swost.mysql import MySQL

__author__ = 'frituurpan'

"""
Controls the main program flow
Starts buffer and receives signal if serialparser has parsed a complete message

The serial classes run in their own threads, so this class just waits a lot
"""


class MainController:
    """
    :type serialParser: SerialParser
    """
    serialParser = -1
    emonController = -1

    signalListeners = {}

    config = ''
    mysql = -1

    def __init__(self, serial_parser, emon_controller, config):
        """
        :type serial_parser:SerialParser
        :param emon_controller:
        :return:
        """
        self.config = config
        self.serialParser = serial_parser
        self.emonController = emon_controller
        self.get_serial_parser().register_observer(self)

    def start(self):
        # self.get_serial_parser().get_serial_buffer().daemon = True
        self.get_serial_parser().get_serial_buffer().start()
        # self.get_serial_parser().daemon = True
        self.get_serial_parser().start()

    def get_serial_parser(self):
        """
        :rtype: SerialParser
        """
        return self.serialParser

    def get_emon_controller(self):
        return self.emonController

    def notify(self):
        self.push_input()

    def push_input(self):
        serial_input = self.serialParser.get_completed_transmissions()
        for transmission in serial_input:
            try:
                self.emonController.post(transmission)
                serial_input.remove(transmission)
                if self.get_db():
                    try:
                        self.get_db().log(4, 16, transmission.get_total_kwh(), transmission.get_gas_m3(),
                                        transmission.get_current_watts())
                    except StandardError, e:
                        print e
            except ConnectionError:
                print "connection timeout, sleeping"
                time.sleep(10)

    def get_db(self):
        if self.mysql is False:
            return False
        if self.mysql == -1:
            try:
                mysql = MySQL()
                mysql.open(self.get_config().get_db_host(), self.get_config().get_db_user(),
                           self.get_config().get_db_password(), self.get_config().get_db_database())
                self.mysql = mysql
            except StandardError, e:
                print e
                self.mysql = False
        return self.mysql

    def shutdown(self):
        self.get_serial_parser().get_serial_buffer().join()
        self.get_serial_parser().join()

    def get_config(self):
        """
        :rtype: SwostConfig
        """
        return self.config