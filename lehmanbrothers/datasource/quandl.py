import quandl
import pandas as pd


class Retriever(object):
    def __init__(self, config, cache_service):
        self._config = config
        self._cache_service = cache_service

    def get_data(self, tokens):
        if not tokens:
            return None

        data = self._cache_service.get_data(tokens)
        print(data)
        if data is None or data.empty:
            quandl.ApiConfig.api_key = self._config['quandl']['api_key']

            tickers = [tokens['dependent_variable']]
            if 'independent_variables' in tokens and isinstance(tokens['independent_variables'], list):
                tickers = tickers + tokens['independent_variables']

            data = quandl.get_table('WIKI/PRICES',
                                    qopts={'columns': ['ticker', 'date', 'close']},
                                    ticker=tickers,
                                    date={'gte': tokens['date_from'], 'lte': tokens['date_to']})

            if not isinstance(data, pd.DataFrame):
                return None

            self._cache_service.save_data(tokens, data)
        return data
