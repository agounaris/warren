import os
import redis
import pandas as pd


class DataStore(object):

    def __init__(self, config):
        self._config = config
        self._redis = redis.StrictRedis(host=config['app']['redis_url'],
                                        port=int(config['app']['redis_port']),
                                        db=0)

    def save_data(self, tokens, mixed_dataframe):
        tickers = [tokens['dependent_variable']]
        if 'independent_variables' in tokens and isinstance(tokens['independent_variables'], list):
            tickers = tickers + tokens['independent_variables']

        print(tickers)
        for ticker in tickers:
            df = mixed_dataframe[mixed_dataframe['ticker'] == ticker]
            filename = '{}_{}_{}.csv'.format(
                tokens['date_from'],
                tokens['date_to'],
                ticker
            )

            self._redis.set(filename, df.to_csv())

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
                data = self._redis.get(filename)
                data = pd.read_csv(data,
                                   parse_dates=True,
                                   index_col=2)
                frames.append(data)
            except Exception:
                return None

        result = pd.concat(frames)

        return result

    def save_statements(self, tokens, data):
        filename = 'statements_{}.csv'.format(tokens['ticker'].upper())
        self._redis.set(filename, data)

    def get_statements(self, tokens):
        filename = 'statements_{}.csv'.format(tokens['ticker'].upper())

        try:
            data = self._redis.get(filename)
            data = pd.read_csv(cached_file_path,
                               parse_dates=True,
                               index_col=0)
        except Exception:
                return None

        return data
