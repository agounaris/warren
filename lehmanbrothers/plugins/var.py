from .abstractplugin import AbstractPlugin
from datetime import datetime
from statsmodels.tsa.api import VAR, DynamicVAR
from marshmallow import Schema, fields, pprint
import pandas as pd
import os


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
        self._filename = filename
        self._args = self._validate_arguments(*args)

    def run(self):
        if not self._args:
            return None

        cached_file_path = os.path.join(self._config['app']['app_directory'], 'cache', self._filename)

        data = self._data_service.get_data(self._args, cached_file_path)

        split_data = {
            self._args['dependent_variable']:
                data[data['ticker'] == self._args['dependent_variable']]['close']
        }
        for i, ticker in enumerate(self._args['independent_variables']):
            split_data[ticker] = data[data['ticker'] == ticker]['close']

        data = pd.DataFrame(split_data).dropna()
        print(data.head())

        model = VAR(data)
        results = model.fit(2)
        print(results.summary())

        return "var"

    @property
    def name(self):
        return self._name

    def _validate_arguments(self, args):
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
