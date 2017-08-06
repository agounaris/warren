import pandas as pd

class DataStore(object):

    def __init__(self, config):
        self._config = config

    def save_data(self, key, value):
        with open(key, 'w') as file:
            file.write(value)

    def get_data(self, key):
        try:
            data = pd.read_csv(key, parse_dates=True, index_col=2)
        except Exception:
            return None
        return data
