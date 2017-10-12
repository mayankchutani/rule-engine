__author__ = 'mayank'
from app.dao import mongo_dao
from app.config import config

class RuleType(object):

    def __init__(self, rule_type_json):
        rule_type = rule_type_json.get('ruleType', '')
        partial = rule_type_json.get('partial', False)

        self.value = {
            'ruleType': rule_type,
            'partial': partial
        }

    def get_value(self):
        return self.value

    @staticmethod
    def fetch_value_from_store(rule_type):
        COL = mongo_dao.MongoDao(config.mongo_config.get('URI'),
                                 config.mongo_config.get('DB'),
                                 config.mongo_config.get('RULE_TYPE_COL')).get_collection()
        doc = COL.find_one({'ruleType': rule_type})
        return doc
