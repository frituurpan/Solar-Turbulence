__author__ = 'frituurpan'

"""
Receives data array and posts it to emoncms
"""


class EmonController:
    def __init__(self):
        a = 1

    def prepare_data(self, data):
        raise Exception("Implement me!")

    def post_data(self, data):
        raise Exception("Implement me!")