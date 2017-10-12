import operator
import copy

import pymongo

from app.components.Rule import Rule
from app.components.RuleType import RuleType
from app.dao import mongo_dao
from app.utils import datatype_utils
from app.utils import ranking_utils
from app.config import config
from app.utils import dao_connector_util


__author__ = 'mayank'


def update_status(args):
    rule_type = args.get('ruleType')
    rule_name = args.get('ruleName')
    status = args.get('enable')
    if not rule_type or not rule_name or status is None:
        raise KeyError('"ruleType", "ruleName", "enable" are expected as params')
    query = {'ruleType': rule_type, 'ruleName': rule_name}
    update_doc = {'_enabled': status}
    res = dao_connector_util.DaoConnector(connection_db='mongodb').update(query, update_doc)
    return {'message': str(res)}


def add_rule(args, match_dict):
    params = copy.deepcopy(args)
    params.update(match_dict)
    rule_obj = Rule(params).get_rule()
    query = {'_meta._ruleType': params.get('ruleType'), '_meta._ruleName': params.get('ruleName')}
    update_doc = rule_obj
    res = dao_connector_util.DaoConnector(connection_db='mongodb').update(query, update_doc)
    return res


def get_rule(match_dict):
    query = {'_meta._ruleType': match_dict.get('ruleType'),
             '_meta._ruleName': match_dict.get('ruleName')}
    res = dao_connector_util.DaoConnector(connection_db='mongodb').get_one(query)
    return res


def delete_rule(match_dict):
    COL = mongo_dao.MongoDao(config.mongo_config.get('URI'),
                             config.mongo_config.get('DB'),
                             config.mongo_config.get('COL')).get_collection()
    mongo_res = COL.remove({'_meta._ruleType': match_dict.get('ruleType'),
                              '_meta._ruleName': match_dict.get('ruleName')})
    return mongo_res


def remove_internal_fields(doc):
    item = {k: v for k, v in doc.items() if not k.startswith('_')}
    return item


def add_rule_type(args, match_dict):
    COL = mongo_dao.MongoDao(config.mongo_config.get('URI'),
                             config.mongo_config.get('DB'),
                             config.mongo_config.get('RULE_TYPE_COL')).get_collection()
    params = copy.deepcopy(args)
    params.update(match_dict)
    rule_type_obj = RuleType(params).get_value()
    COL.ensure_index('ruleType', pymongo.ASCENDING)
    mongo_res = str(COL.update({'ruleType': rule_type_obj.get('ruleType')}, rule_type_obj, upsert=True))
    return mongo_res


def get_rule_type(match_dict):
    COL = mongo_dao.MongoDao(config.mongo_config.get('URI'),
                             config.mongo_config.get('DB'),
                             config.mongo_config.get('RULE_TYPE_COL')).get_collection()
    rule_type = match_dict.get('ruleType')
    doc = COL.find_one({'ruleType': rule_type})
    if doc:
        doc.pop('_id')
    else:
        doc = {}
    return doc


def delete_rule_type(match_dict):
    COL = mongo_dao.MongoDao(config.mongo_config.get('URI'),
                             config.mongo_config.get('DB'),
                             config.mongo_config.get('RULE_TYPE_COL')).get_collection()
    rule_type = match_dict.get('ruleType')
    doc = COL.remove({'ruleType': rule_type})
    return doc


def get_default_rules(rule_type):
    COL = mongo_dao.MongoDao(config.mongo_config.get('URI'),
                             config.mongo_config.get('DB'),
                             config.mongo_config.get('COL')).get_collection()
    doc_list = []
    for doc in COL.find({'_meta._ruleType': rule_type, '_meta._default': True}):
        doc.pop('_id')
        doc_list.append(doc)
    return doc_list


def find_rule(args, match_dict, query_params):
    COL = mongo_dao.MongoDao(config.mongo_config.get('URI'),
                             config.mongo_config.get('DB'),
                             config.mongo_config.get('COL')).get_collection()

    # Search for all enabled rules
    query = {'_meta._enabled': True}

    # Searching within a rule type
    rule_type = match_dict.get('ruleType')
    if not rule_type or rule_type == '*':
        pass
    else:
        query.update({'_meta._ruleType': rule_type})

    cursor = COL.find(query)
    exact_match_doc_list = []
    partial_match_doc_list = []
    main_doc_list = []
    for doc in cursor:
        doc.pop('_id')
        condition = doc.get('_condition', {})
        if not condition:
            continue
        meta = doc.get('_meta', {})
        partial = meta.get('_partial', False)
        # TODO: Brute force here. Needs to be optimized.
        all_match = True
        matched_attributes_list = []
        for key, value in args.items():
            if key not in condition.keys():
                continue
            condition_field = condition[key]
            condition_operator = condition_field.get('operator')
            condition_data_type = condition_field.get('dataType')
            condition_value = condition_field.get('value')
            condition_case_sensitivity = condition_field.get('caseSensitive', True)
            cls = getattr(datatype_utils, condition_data_type)
            instance = cls(value, case_sensitive=condition_case_sensitivity)
            func = getattr(instance, condition_operator)
            if not func(condition_value):
                all_match = False
            else:
                matched_attributes_list.append(condition_field)
        if all_match:
            exact_match_doc_list.append(doc)
        elif partial:
            score = ranking_utils.get_score(matched_attributes_list, args)
            if score > 0:
                doc.update({'_score': score})
                partial_match_doc_list.append((score, doc))

    if exact_match_doc_list:
        main_doc_list = exact_match_doc_list
    else:
        partial_match_doc_list = sorted(partial_match_doc_list, key=operator.itemgetter(0), reverse=True)
        partial_match_doc_list = [doc for score, doc in partial_match_doc_list]
        main_doc_list = partial_match_doc_list

    # Return default rule if no rule matched
    if not main_doc_list:
        main_doc_list = get_default_rules(rule_type)

    main_doc_list = [remove_internal_fields(doc)
                     if query_params.get('factors', "false") != "true"
                     else doc
                     for doc in main_doc_list]
    return main_doc_list

