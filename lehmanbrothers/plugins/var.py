from .abstractplugin import AbstractPlugin
from voluptuous import Schema, ExactSequence
from datetime import datetime


def Date(fmt='%Y-%m-%d'):
    return lambda v: datetime.strptime(v, fmt)


class Plugin(AbstractPlugin):

    def __init__(self, *args):
        self._name = __name__
        self._args = self._validate_arguments(*args)
        # print(self._args)

    def run(self):
        if not self._args:
            return None
        return "var"

    @property
    def name(self):
        return self._name

    def _validate_arguments(self, args):
        # print(args)
        # seq = [str, Date(), Date(), int]
        # validate = Schema(ExactSequence(seq))
        # try:
        #     validate(args)
        # except Exception:
        #     print('Invalid input')
        #     return []
        return args
