from app.dao import mongo_dao
from app.config import config


class DaoConnector(object):

    def __init__(self, connection_db):
        self.connection_db = connection_db

    @staticmethod
    def _mongo_update(query, body):
        conn = mongo_dao.MongoDao(config.mongo_config.get('URI'),
                                 config.mongo_config.get('DB'),
                                 config.mongo_config.get('COL'))
        res = conn.update(query, body)
        return res

    def _elasticsearch_update(self, query, body):
        pass

    @staticmethod
    def _mongo_get_one(query):
        conn = mongo_dao.MongoDao(config.mongo_config.get('URI'),
                                  config.mongo_config.get('DB'),
                                  config.mongo_config.get('COL'))
        doc = conn.find_one(query)
        return doc

    def _elasticsearch_get_one(self, query):
        pass

    def update(self, query, body):
        if self.connection_db == 'mongodb':
            return self._mongo_update(query, body)
        else:
            return self._elasticsearch_update(query, body)

    def get_one(self, query):
        if self.connection_db == 'mongodb':
            return self._mongo_get_one(query)
        else:
            return self._elasticsearch_get_one(query)


