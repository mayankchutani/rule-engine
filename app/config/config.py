__author__ = 'mayank'
import os


mongo_config = {
    'URI': os.getenv('MONGO_URI'),
    'DB': 'rule_engine',
    'COL': 'rules',
    'RULE_TYPE_COL': 'rule_type'
}

elasticsearch_config = {
    'HOST': os.getenv('ELASTICSEARCH_HOST'),
    'PORT': os.getenv('ELASTICSEARCH_PORT'),
    'INDEX': 'orm',
    'TYPE': 'entity'
}
