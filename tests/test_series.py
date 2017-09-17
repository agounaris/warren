from warren.plugins.series import Plugin


class TestSeries(object):

    def test_init(self):
        args = [
            '2015-01-10',
            '2015-10-10',
            'MSFT',
        ]
        plugin = Plugin('test', 'test', args)
        assert isinstance(plugin, Plugin)

    def test_validation_failure_wrong_arguments(self):
        args = [
            'efwfew',
            2
        ]

        plugin = Plugin('test', {'test': 'test'}, args)

        validated_args = plugin._validate_arguments(args)

        assert len(validated_args) == 0
