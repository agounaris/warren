import pandas as pd
import os


class DataStore(object):

    def __init__(self, config):
        self._config = config

    def save_data(self, tokens, mixed_dataframe):
        tickers = [tokens['dependent_variable']]
        if 'independent_variables' in tokens and isinstance(tokens['independent_variables'], list):
            tickers = tickers + tokens['independent_variables']

        for ticker in tickers:
            df = mixed_dataframe[mixed_dataframe['ticker'] == ticker]
            filename = '{}_{}_{}.csv'.format(
                tokens['date_from'],
                tokens['date_to'],
                ticker
            )

            cached_file_path = os.path.join(
                self._config['app']['app_directory'], 'cache', filename)
            with open(cached_file_path, 'w') as file:
                file.write(df.to_csv())

    def get_data(self, tokens):
        tickers = [tokens['dependent_variable']]
        if 'independent_variables' in tokens and isinstance(tokens['independent_variables'], list):
            tickers = tickers + tokens['independent_variables']

        frames = []
        for ticker in tickers:
            filename = '{}_{}_{}.csv'.format(
                tokens['date_from'],
                tokens['date_to'],
                ticker
            )

            try:
                cached_file_path = os.path.join(
                    self._config['app']['app_directory'], 'cache', filename)
                print(cached_file_path)
                data = pd.read_csv(
                    cached_file_path, parse_dates=True, index_col=2)
                frames.append(data)
            except Exception:
                return None

        print(frames)
        result = pd.concat(frames)

        return result

    def save_statements(self, tokens, data):
        filename = 'statements_{}.csv'.format(tokens['ticker'].upper())
        cached_file_path = os.path.join(
                self._config['app']['app_directory'], 'cache', filename)
        with open(cached_file_path, 'w') as file:
            file.write(data)

    def get_statements(self, tokens):
        filename = 'statements_{}.csv'.format(tokens['ticker'].upper())
        try:
            cached_file_path = os.path.join(
                self._config['app']['app_directory'], 'cache', filename)
            print(cached_file_path)
            data = pd.read_csv(cached_file_path, parse_dates=True, index_col=0)
        except Exception:
            return None

        return data
