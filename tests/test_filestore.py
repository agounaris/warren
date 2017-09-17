from warren.cache.filestore import DataStore

config = {
        'app': {
            'app_directory': 'warren',
        }
    }


class TestFilestore(object):

    def test_init(self):
        dataStore = DataStore(config)
        assert isinstance(dataStore, DataStore)
