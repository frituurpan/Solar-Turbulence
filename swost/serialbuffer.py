import Queue
import threading
import serial
import sys

__author__ = 'frituurpan'

"""
Reads serial input and puts it into a buffer

Uses its own thread to monitor serial connection
"""


class SerialBuffer(threading.Thread):
    # Serial connection
    ser = -1

    # storage for serial output lines
    queue = {}
    queueArray = []

    #temporary storage for raw serial input
    buffer = ''

    def __init__(self, config):
        """
        :type config:SwostConfig
        """
        super(SerialBuffer, self).__init__()

        self.queue = Queue.Queue(0)  # create a new queue

        # configure serial connection
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.SEVENBITS
        self.ser.parity = serial.PARITY_EVEN
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.xonxoff = 0
        self.ser.rtscts = 0
        self.ser.timeout = None
        self.ser.port = config.get_port()

    def run(self):
        self.open_serial_port()
        while True:
            self.buffer += self.ser.read(self.ser.inWaiting() or 1)  # read all char in buffer
            while '\n' in self.buffer:  # split data line by line and store it in var
                var, self.buffer = self.buffer.split('\n', 1)
                print var
                self.queue.put(var)  # put received line in the queue
                self.queueArray.append(var)

    def get_transmissions(self, pop=False):
        transmissions = []
        while len(self.queueArray) > 19:
            transmissions.append(self.shift(20, self.queueArray))
        return transmissions

    @staticmethod
    def shift(key, array):
        """
        Shift x elements of the beginning of the array
        """
        return array[:+key]

    def get_queue(self):
        return self.queue

    def count_queue(self):
        return len(self.queueArray)

    def open_serial_port(self):
        #Open COM port
        try:
            self.ser.open()
        except StandardError, e:
            print e
            sys.exit("Error opening serial connection %s. Exitting.")

