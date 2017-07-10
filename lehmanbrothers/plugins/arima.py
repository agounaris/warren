from .abstractplugin import AbstractPlugin
from voluptuous import Schema, ExactSequence

class Plugin(AbstractPlugin):

    def __init__(self, *args):
        self._name = __name__
        self._args = self._validate_arguments(*args)
        # print(self._args)

    def run(self):
        if not self._args:
            return None

        print(self._args)
        return "hello"

    @property
    def name(self):
        return self._name

    def _validate_arguments(self, args):
        validate = Schema(ExactSequence([str, str, str]))
        try:
            validate(args)
        except Exception:
            print('Invalid input')
            print(ExactSequence([str, str, str]))
            return []
        return args

    def input_schema(self):
        schema = Schema({
            'symbol': str,
            'start_date': str,
            'end_date': str,
            'predict_days': int,
        })
        return schema

    def output_schema(self):
        schema = Schema({
            'predicted_price': float
        })
        return schema