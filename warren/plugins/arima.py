import pandas as pd
import statsmodels.tsa.api as smt

from .abstractplugin import AbstractPlugin
from marshmallow import Schema, fields
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
from collections import namedtuple


class ArgumentsSchema(Schema):
    date_from = fields.DateTime(required=True, format='%Y-%m-%d')
    date_to = fields.DateTime(required=True, format='%Y-%m-%d')
    dependent_variable = fields.Str(required=True)
    days_to_predict = fields.Int(required=True)


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

        original_data = data.fillna(method='bfill')

        ran = pd.date_range(self._args['date_from'],
                            self._args['date_to'],
                            freq='D')
        original_data = pd.Series(original_data['close'], index=ran)

        original_data = original_data.fillna(method='bfill')
        split = len(original_data) - int(self._args['days_to_predict'])

        train_data, prediction_data = original_data[:split], original_data[
                                                             split:]



        ADF = namedtuple('ADF', 'adf pvalue usedlag nobs critical icbest')
        stationarity_results = ADF(*smt.adfuller(train_data))._asdict()
        significance_level = 0.01

        # if the series are stationary, no need for an integrated order
        order = (1, 0, 1)
        if stationarity_results['pvalue'] > significance_level:
            order = (1, 2, 1)

        # result = self._model_fit(train_data, order)

        # prediction = result.predict(prediction_data.index[0],
                                    # prediction_data.index[-1],
                                    # typ='levels')
        # print(prediction.tail(self._args['days_to_predict']))

        result = self._model_fit(original_data, order)
        print(result.summary())

        forecast = result.forecast(steps=int(self._args['days_to_predict']))[0]
        print(forecast)

        return 'object'

    @property
    def name(self):
        return self._name

    def _validate_arguments(self, args):
        try:
            arguments = {
                'date_from': args.pop(0),
                'date_to': args.pop(0),
                'dependent_variable': args.pop(0),
                'days_to_predict': int(args.pop(0)),
            }

            result = ArgumentsSchema().load(arguments)
            if result.errors:
                print('there are validation errors')
                print(result.errors)
                return []
        except IndexError:
            print('not enough input')
            return []
        return arguments

    # @retry(stop_max_attempt_number=3)
    def _model_fit(self, train_data, order):
        mod = ARIMA(train_data, order=order, freq='D')

        try:
            results = mod.fit(disp=0)
        except ValueError:
            print('No correct model with {order}'.format(order=order))
            order = (order(0), order(1) + 1, order(2))
            self._model_fit(train_data=train_data, order=order)
        return results
