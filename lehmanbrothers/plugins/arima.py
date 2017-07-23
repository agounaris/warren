from .abstractplugin import AbstractPlugin
from datetime import date
from marshmallow import Schema, fields, pprint
from datetime import datetime
import os
import pandas as pd

class ArgumentsSchema(Schema):
    date_from = fields.DateTime(required=True, format='%Y-%m-%d') 
    date_to = fields.DateTime(required=True, format='%Y-%m-%d')
    dependent_variable = fields.Str(required=True)
    days_to_predict = fields.Int(required=True)
    # independent_variables = fields.List(fields.String())
    
# class RequestSchema(Schema):
#     function = fields.Str(required=True)
#     arguments = fields.Nested(ArgumentsSchema())


class Plugin(AbstractPlugin):

    def __init__(self, data_service, config=None, filename=None, *args):
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
        print(data)

        return "hello"

    @property
    def name(self):
        return self._name

    def _validate_arguments(self, args):
        try:
            arguments = {
                'date_from': args.pop(0),
                'date_to': args.pop(0),
                'dependent_variable': args.pop(0),
                # 'independent_variables': [arg for arg in args],
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
