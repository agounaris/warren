from warren.cache.filestore import DataStore


class TestFilestore(object):

    def test_init(self):
        dataStore = DataStore('test')
        assert isinstance(dataStore, DataStore)
