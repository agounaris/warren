from .abstractplugin import AbstractPlugin
from datetime import date
from marshmallow import Schema, fields, pprint
from datetime import datetime
import os

class ArgumentsSchema(Schema):
    date_from = fields.DateTime(required=True, format='%Y-%m-%d') 
    date_to = fields.DateTime(required=True, format='%Y-%m-%d')
    dependent_variable = fields.Str(required=True)
    independent_variables = fields.List(fields.String())
    
# class RequestSchema(Schema):
#     function = fields.Str(required=True)
#     arguments = fields.Nested(ArgumentsSchema())


class Plugin(AbstractPlugin):

    def __init__(self, filename=None, *args):
        self._name = __name__
        self._filename = filename
        self._args = self._validate_arguments(*args)

    def run(self):
        if not self._args:
            return None

        import quandl
        quandl.ApiConfig.api_key = "Hxy5g7TB9gbWyzd42vys"

        data = quandl.get_table('WIKI/PRICES', 
                                qopts = { 'columns': ['ticker', 'date', 'close'] }, 
                                ticker = self._args['dependent_variable'], 
                                date = { 'gte': self._args['date_from'], 'lte': self._args['date_to'] })

        
        print(data.to_csv())

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
                'independent_variables': [arg for arg in args],
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
