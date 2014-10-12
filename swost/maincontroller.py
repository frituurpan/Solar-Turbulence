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
        self.get_serial_parser().register_observer(self)

    def start(self):
        #self.get_serial_parser().get_serial_buffer().daemon = True
        self.get_serial_parser().get_serial_buffer().start()
        #self.get_serial_parser().daemon = True
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
            self.emonController.post(transmission)
            serial_input.remove(transmission)

    def shutdown(self):
        self.get_serial_parser().get_serial_buffer().join()
        self.get_serial_parser().join()