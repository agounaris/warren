from .abstractplugin import AbstractPlugin
from datetime import date
from marshmallow import Schema, fields, pprint
from datetime import datetime
import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.tsa.api as smt
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults

class ArgumentsSchema(Schema):
    date_from = fields.DateTime(required=True, format='%Y-%m-%d')
    date_to = fields.DateTime(required=True, format='%Y-%m-%d')
    variables = fields.List(fields.String, required=True)


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

        return 'series'


    def _validate_arguments(self, args):
        try:
            arguments = {
                'date_from': args.pop(0),
                'date_to': args.pop(0),
                'variables': args.pop(0),
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
