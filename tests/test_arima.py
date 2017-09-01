import pytest
from lehmanbrothers.plugins.arima import Plugin


class TestArima(object):

    def test_init(self):
        args = [
            '2015-01-10',
            '2015-10-10',
            'MSFT',
            2,
        ]
        plugin = Plugin('test', 'test', args)
        assert isinstance(plugin, Plugin)

    def test_validation_failure_wrong_type(self):
        args = [
            '2015-01-10',
            '2015-10-10',
            'MSFT',
            'aaa',
        ]

        with pytest.raises(Exception) as e_info:
            plugin = Plugin('test', 'test', args)

