import Queue
import threading
import time

__author__ = 'frituurpan'

"""
Reads the serial buffer, and parses the contents if the message is complete
Sends signal to maincontroller afterwards

Needs own thread for monitoring the buffer
"""


class SerialParser(threading.Thread):

    serialData = -1
    serialBuffer = -1

    completeTransmissions = []

    observers = []

    def __init__(self, serial_buffer):
        self.serialBuffer = serial_buffer

    def start(self):
        self.get_serial_buffer().run()
        self.run()

    def run(self):
        while True:
            try:
                var = self.queue.get(False)  # try to fetch a value from queue
            except Queue.Empty:
                time.sleep(1)
                pass  # if it is empty, do nothing
            else:
                print(var)

        # while True:
        #     time.sleep(0.1)
        #     if self.serialBuffer.count_queue() > 19:
        #         self.move_queue_to_transmissions()
        #         self.notify_observers()
        #     pass

    def get_serial_buffer(self):
        """
        :rtype: SerialBuffer
        """
        return self.serialBuffer

    def move_queue_to_transmissions(self):
        transmissions = self.serialBuffer.get_transmissions(True)
        for transmission in transmissions:
            self.completeTransmissions.append(transmission)

    def get_data(self):
        return self.completeTransmissions

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.notify()
