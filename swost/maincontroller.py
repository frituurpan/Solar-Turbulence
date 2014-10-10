import Queue

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

    def __init__(self, serial_parser, emon_controller):
        """
        :type serial_parser:SerialParser
        :param emon_controller:
        :return:
        """
        self.serialParser = serial_parser
        self.emonController = emon_controller

    def start(self):
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
        serial_input = self.serialParser.get_data()
        print serial_input
        #serial_input = self.emonController.prepare_data(serial_input)
        #serial_result = self.emonController.post(serial_input)