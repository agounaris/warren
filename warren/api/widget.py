from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractWidget(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        """Run whatever you want"""
        return

    @abstractmethod
    def _validate_arguments(args):
        return

    @property
    def name(self):
        return "name"
