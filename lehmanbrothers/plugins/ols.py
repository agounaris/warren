from .abstractplugin import AbstractPlugin
from marshmallow import Schema, fields, pprint
from datetime import datetime
import os
import numpy as np
# import statsmodels.api as sm
import statsmodels.formula.api as sm
import pandas as pd


def Date(fmt='%Y-%m-%d'):
    return lambda v: datetime.strptime(v, fmt)


class ArgumentsSchema(Schema):
    date_from = fields.DateTime(required=True, format='%Y-%m-%d')
    date_to = fields.DateTime(required=True, format='%Y-%m-%d')
    dependent_variable = fields.Str(required=True)
    independent_variables = fields.List(fields.String, required=True)


class Plugin(AbstractPlugin):
    def __init__(self, data_service, config=None, *args):
        self._name = __name__
        self._data_service = data_service
        self._config = config
        self._args = self._validate_arguments(*args)

    def run(self):
        if not self._args:
            return None

        data = self._data_service.get_data(self._args)

        split_data = {
            self._args['dependent_variable']: list(
                data[data['ticker'] == self._args['dependent_variable']]['close'].values)
        }
        formula = '{}'.format(self._args['dependent_variable'])
        for i, ticker in enumerate(self._args['independent_variables']):
            split_data[ticker] = list(data[data['ticker'] == ticker]['close'].values)
            symbol = '+'
            if i == 0:
                symbol = '~'
            formula = '{formula} {symbol} {ticker}'.format(formula=formula, symbol=symbol, ticker=ticker)


        data = pd.DataFrame(split_data).dropna()

        model = sm.ols(formula=formula, data=data)
        result = model.fit()
        print(result.summary())

        prediction = result.predict()
        print('Price of {} for the last day is {}'.format(self._args['dependent_variable'],
                                                          prediction[-1]))

        return 'ols'

    @property
    def name(self):
        return self._name

    def _validate_arguments(self, args):
        print(args)
        try:
            arguments = {
                'date_from': args.pop(0),
                'date_to': args.pop(0),
                'dependent_variable': args.pop(0),
                'independent_variables': args,
            }

            if not arguments['independent_variables']:
                raise IndexError

            result = ArgumentsSchema().load(arguments)
            if result.errors:
                print('there are validation errors')
                print(result.errors)
                return []
        except IndexError:
            print('not enough input')
            return []
        return arguments
