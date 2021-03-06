import os
from swost.swostconfig import SwostConfig
from swost.emoncontroller import EmonController
from swost.maincontroller import MainController
from swost.serialbuffer import SerialBuffer
from swost.serialparser import SerialParser

__author__ = 'frituurpan'
"""
Main program executable, yay!
"""


currentDir = os.path.dirname(os.path.abspath(__file__))
configFilePath = currentDir + r'/swost.conf'

config = SwostConfig(configFilePath)

serialBuffer = SerialBuffer(config)
serialParser = SerialParser(serialBuffer, config)

emonController = EmonController(config)

mainController = MainController(serialParser, emonController, config)

try:
    mainController.start()
except Exception:
    mainController.shutdown()