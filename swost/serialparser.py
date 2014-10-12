import Queue
import copy
import threading
import time
from swost.transmissionmodel import TransmissionModel

__author__ = 'frituurpan'

"""
Reads the serial buffer, and parses the contents if the message is complete
Sends signal to maincontroller afterwards

Needs own thread for monitoring the buffer
"""


class SerialParser(threading.Thread):

    serialData = -1
    serialBuffer = -1

    queueArray = []
    completeTransmissions = []

    observers = []

    def __init__(self, serial_buffer):
        super(SerialParser, self).__init__()
        self.serialBuffer = serial_buffer

    def run(self):
        while True:
            try:
                var = self.serialBuffer.queue.get(False)  # try to fetch a value from queue
            except Queue.Empty:
                time.sleep(0.1)
                pass  # if it is empty, do nothing
            else:
                var_cpy = copy.deepcopy(var)
                del var
                self.queueArray.append(var_cpy)
                for row in self.queueArray:
                    if row == '!':
                        self.move_queue_to_transmissions()
                        self.notify_observers()

    def get_serial_buffer(self):
        """
        :rtype: SerialBuffer
        """
        return self.serialBuffer

    def move_queue_to_transmissions(self):
        transmissions = self.get_transmissions()
        for transmission in transmissions:
            transmission_object = TransmissionModel(transmission)
            self.completeTransmissions.append(transmission_object)

    def get_completed_transmissions(self):
        return self.completeTransmissions

    def get_transmissions(self):
        queue_array = copy.deepcopy(self.queueArray)
        transmissions = [queue_array[:21]]
        del self.queueArray[:21]
        return transmissions

    @staticmethod
    def shift(key, array):
        """
        Shift x elements of the beginning of the array
        """
        return array[:+key]

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.notify()
