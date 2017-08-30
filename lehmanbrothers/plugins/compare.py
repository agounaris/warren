from .abstractplugin import AbstractPlugin
from datetime import datetime
from marshmallow import Schema, fields, pprint
import pandas as pd
import os

codes = [
    'INTANGIBLES',
    'INVENTORY',
    'ASSETS',
    'ASSETSC',
    'LIABILITIESC',
    'LIABILITIES',
    'EQUITY',
    'CAPEX',
    'DEPAMOR',
    'NCFX',
    'NCF',
    'NCFF',
    'NETINC',
    'NCFI',
    'NCFO',
    'GP',
    'TAXEXP',
    'INTEXP',
    'NETINCCMN',
    'RND',
    'SGNA',
    'REVENUE',
    'EBIT',
    'RETEARN',
    'PAYABLES',
]


class ArgumentsSchema(Schema):
    ticker = fields.Str(required=True)
    statement = fields.Str(required=True)
    year_from = fields.Str(required=True)
    year_to = fields.Str(required=True)


class Plugin(AbstractPlugin):

    def __init__(self, data_service, config=None, *args):
        self._name = __name__
        self._data_service = data_service
        self._config = config
        self._args = self._validate_arguments(*args)

    def run(self):
        if not self._args:
            return None

        fp = self._data_service.get_statements(self._args)

        print(fp.get_balance_sheet_by_year(self._args['year_from']) == fp.get_balance_sheet_by_year(self._args['year_to']))

        return self._args

    @property
    def name(self):
        return self._name

    def _validate_arguments(self, args):
        try:
            arguments = {
                'ticker': args.pop(0),
                'statement': args.pop(0),
                'year_from': args.pop(0),
                'year_to': args.pop(0),
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
