__author__ = 'Administrator'


class TransmissionModel:
    raw_data = ''

    def __init__(self, data):
        self.raw_data = data

    def get_total_kwh(self):
        pass

    def get_day_kwh(self):
        key = '1-0:1.8.1'
        val = self.get_row_by_key(key)
        val = str.replace(val, '*kWh)', '')
        val = str.replace(val, key + '(', '')
        return val

    def get_night_kwh(self):
        key = '1-0:1.8.2'
        val = self.get_row_by_key(key)
        val = str.replace(val, '*kWh)', '')
        val = str.replace(val, key + '(', '')
        return val
        pass

    def get_current_watts(self):
        return str.replace(str.replace(self.raw_data[18], '(', ''), ')', '')
        pass

    def get_gas_m3(self):
        # line 18
        pass

    def get_row_by_key(self, key):
        for line in self.raw_data:
            if key in line:
                return line

    @staticmethod
    def get_value_from_row(row):
        return row[row.index('(') + 1:row.index(')')]

    @staticmethod
    def convert_value(val):
        return int(float(val) * 1000)
