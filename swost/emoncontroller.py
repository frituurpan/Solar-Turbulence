__author__ = 'frituurpan'

"""
Receives data array and posts it to emoncms
"""

import requests


class EmonController:
    debug = False

    emonUrl = ""
    apiKey = ""
    config = ""
    post_mode = '!timestamp'

    def __init__(self, config):
        """
        :type config: SwostConfig
        :return:
        """
        self.emonUrl = config.get_post_url()
        self.apiKey = config.get_api_key()
        self.config = config

    def create_payload(self, gas_total, energy_total, current_watts):
        """
        :param gas_total:
        :param energy_total:
        :return:
        """

        if self.is_debug():
            node_id = 17
        else:
            node_id = 20

        if self.post_mode == 'timestamp':
            offset = '0'
        else:
            offset = '4'

        params = '[[' + offset + ',' + str(node_id) + ',' + str(gas_total) + ',' + str(energy_total) + ',' + str(
            current_watts) + ']]'
        return params

    def build_url(self, pay_load, unix_timestamp=''):
        if unix_timestamp == '':
            raise Exception('No timestamp present')

        url = str(self.emonUrl) + '?' + 'apikey=' + self.apiKey + '&data=' + str(pay_load)

        if self.post_mode == 'timestamp':
            url = url + '&time=' + str(unix_timestamp)
        return url

    @staticmethod
    def post_url_func(url):
        print requests.get(url=url)

    def is_debug(self):
        return self.config.debug()

    def post(self, transmission):
        """
        :type transmission:TransmissionModel
        :return:
        """
        # if self.check_config():
        # return False

        gas_total = int(transmission.get_gas_m3() * 1000)
        energy_total = int(transmission.get_total_kwh() * 1000)
        current_watts = int(transmission.get_current_watts() * 1000)
        if gas_total > 0 and energy_total > 0:
            payload = self.create_payload(gas_total, energy_total, current_watts)

            post_url = self.build_url(payload, transmission.get_timestamp())
            print post_url
            self.post_url_func(post_url)

    def check_config(self):
        if 'API_KEY_HERE' in self.config.get_api_key():
            if self.is_debug() is False:
                return False
        return True