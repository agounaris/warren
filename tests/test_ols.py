import pytest

from warren.plugins.ols import Plugin


class TestOls(object):

    def test_init(self):
        args = [
            '2015-01-10',
            '2015-10-10',
            'MSFT',
            'AAPL',
        ]
        plugin = Plugin('test', {'test': 'test'}, args)
        assert isinstance(plugin, Plugin)

    def test_name(self):
        args = [
            '2015-01-10',
            '2015-10-10',
            'MSFT',
            'AAPL',
        ]
        plugin = Plugin('test', {'test': 'test'}, args)
        assert plugin.name is not None

    def test_validation_failure_wrong_type(self):
        args = [
            '2015-01-10',
            '2015-10-10',
            'MSFT',
            3
        ]

        plugin = Plugin('test', {'test': 'test'}, args)

        validated_args = plugin._validate_arguments(args)

        assert len(validated_args) == 0

    def test_validation_missing_indepentent_variables(self):
        args = [
            '2015-01-10',
            '2015-10-10',
            'MSFT'
        ]

        plugin = Plugin('test', {'test': 'test'}, args)

        validated_args = plugin._validate_arguments(args)

        assert len(validated_args) == 0
