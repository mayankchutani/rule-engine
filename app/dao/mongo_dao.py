__author__ = 'mayank'
import os
import logging
import traceback

import ssl
from pymongo import MongoClient


class MongoDao(object):
    def __init__(self, uri, database_name, collection_name, username='', password=''):
        logging.debug('Initializing mongodb...')

        self.uri = uri
        self.database_name = database_name
        self.username = username
        self.password = password
        self.collection_name = collection_name
        self.database = self._build_connection()

    def _build_ssl_connection(self):
        logging.debug('Building SSL mongo connection...')

        ca_cert_path = os.path.join(os.getenv('CREDS_DIR'), 'ca.cert.pem')
        server_key_path = os.path.join(os.getenv('PRIVATE_CREDS_DIR'), 'container.key.pem')
        server_cert_path = os.path.join(os.getenv('CREDS_DIR'), 'container.cert.pem')

        self.client = MongoClient(
            self.uri,
            ssl=True,
            ssl_ca_certs=ca_cert_path,
            ssl_certfile=server_cert_path,
            ssl_keyfile=server_key_path,
            ssl_cert_reqs=ssl.CERT_NONE,
            connect=False
        )
        db = self.client[self.database_name]
        try:
            authentication = db.authenticate(
                name=self.username,
                password=self.password,
                source='admin'
            )
            if authentication is True:
                logging.debug('Mongodb authenticated. Access granted...')
        except Exception:
            logging.exception(traceback.print_exc())
        return db

    def _build_simple_connection(self):
        logging.getLogger('debug_logger').debug('building simple connection')
        logging.debug('Building simple mongo connection...')
        logging.getLogger('debug_logger').debug(str(self.uri))
        self.client = MongoClient(self.uri, connect=False)
        db = self.client[self.database_name]
        # try:
        #     authentication = db.authenticate(
        #         name=self.username,
        #         password=self.password,
        #         source='admin'
        #     )
        #     if authentication is True:
        #         logging.debug('Mongodb authenticated. Access granted...')
        # except Exception:
        #     logging.exception(traceback.print_exc())
        col = db[self.collection_name]
        return col

    def _build_connection(self):
        logging.getLogger('debug_logger').debug('build connection...')
        if os.getenv('MONGO_SSL_ENABLED', '') == "true":
            self.collection = self._build_ssl_connection()
        else:
            self.collection = self._build_simple_connection()

    def get_collection(self):
        return self.collection

    def execute_query(self, query):
        return self.collection.find(query)

    def update(self, query, body, upsert=True):
        return self.collection.update(query, {'$set': body}, upsert=upsert)

    def find_one(self, query):
        return self.collection.find_one(query)

    def remove(self, query, multi=True):
        return self.collection.remove(query, multi=multi)

    def find(self, query):
        return self.collection.find(query)
