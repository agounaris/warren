from .abstractplugin import AbstractPlugin


class Plugin(AbstractPlugin):

    def __init__(self, *args):
        self._name = __name__
        self._args = self._validate_arguments(args)
        print(self._args)

    def run(self):
        return "hello"

    @property
    def name(self):
        return self._name

    def _validate_arguments(args):
        return args

# def run():
#     return "hello"
