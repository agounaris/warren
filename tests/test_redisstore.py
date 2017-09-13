from lehmanbrothers.cache.redisstore import DataStore


class TestRedisstore(object):

    def test_init(self):
        dataStore = DataStore('test')
        assert isinstance(dataStore, DataStore)
