__author__ = 'mayank'
from japronto import Application
import logging
import logging.config
import json
from app.utils import rule_util
import traceback


from app.config.logging_config import config as log_config_dict

# Setup logging
logging.config.dictConfig(log_config_dict)

info_logger = logging.getLogger('info_logger')
debug_logger = logging.getLogger('debug_logger')
error_logger = logging.getLogger('error_logger')


application = Application()


def ping(request):
    info_logger.info('/ping')
    return request.Response(code=200,
                            text=json.dumps({'message': 'Hey, I\'m running'}),
                            mime_type='application/json')


def get_rule_type(request):
    try:
        match_dict = request.match_dict
        info_logger.info('REQ: {}'.format(str(match_dict)))
        res = rule_util.get_rule_type(match_dict)
        info_logger.info('RES: {}'.format(str(res)))
        return request.Response(code=200,
                                text=json.dumps(res),
                                mime_type='application/json')
    except Exception:
        error_logger.error(traceback.print_exc())


def delete_rule_type(request):
    match_dict = request.match_dict
    info_logger.info('REQ: {}'.format(str(match_dict)))
    res = rule_util.delete_rule_type(match_dict)
    info_logger.info('RES: {}'.format(str(res)))
    return request.Response(code=200,
                            text=json.dumps(res),
                            mime_type='application/json')


def add_rule(request):
    try:
        args = request.json
        match_dict = request.match_dict
        info_logger.info('REQ: {}'.format(str(args)))
        res = rule_util.add_rule(args, match_dict)
        info_logger.info('RES: {}'.format(str(res)))
        return request.Response(code=200,
                                text=json.dumps({'message': res}),
                                mime_type='application/json')
    except Exception:
        error_logger.error(traceback.print_exc())


def get_rule(request):
    try:
        match_dict = request.match_dict
        info_logger.info('REQ: {}'.format(str(match_dict)))
        res = rule_util.get_rule(match_dict)
        info_logger.info('RES: {}'.format(str(res)))
        return request.Response(code=200,
                                text=json.dumps(res),
                                mime_type='application/json')
    except Exception:
        error_logger.error(traceback.print_exc())


def delete_rule(request):
    match_dict = request.match_dict
    info_logger.info('REQ: {}'.format(str(match_dict)))
    res = rule_util.delete_rule(match_dict)
    info_logger.info('RES: {}'.format(str(res)))
    return request.Response(code=200,
                            text=json.dumps(res),
                            mime_type='application/json')


def find_rule(request):
    try:
        args = request.json
        match_dict = request.match_dict
        info_logger.info('REQ: {}'.format(str(args)))
        query_params = request.query
        res = rule_util.find_rule(args, match_dict, query_params)
        info_logger.info('REQS: {}'.format(str(res)))
        return request.Response(code=200,
                                text=json.dumps(res),
                                mime_type='application/json')
    except Exception:
        error_logger.error(traceback.print_exc())


def update_rule_status(request):
    try:
        args = request.json
        info_logger.info('REQ: {}'.format(str(args)))
        res = rule_util.update_status(args)
        info_logger.info('RES: {}'.format(str(res)))
        return request.Response(code=200,
                                text=json.dumps(res),
                                mime_type='application/json')
    except Exception:
        error_logger.error(traceback.print_exc())


def add_rule_type(request):
    try:
        args = request.json
        match_dict = request.match_dict
        info_logger.info('REQ: {}'.format(str(args)))
        res = rule_util.add_rule_type(args, match_dict)
        info_logger.info('RES: {}'.format(str(res)))
        return request.Response(code=200,
                                text=json.dumps({'message': res}),
                                mime_type='application/json')
    except Exception:
        error_logger.error(traceback.print_exc())


router = application.router
router.add_route('/', ping, methods=['GET'])
router.add_route('/rule/type/{ruleType}', add_rule_type, methods=['PUT'])
router.add_route('/rule/type/{ruleType}', get_rule_type, methods=['GET'])
router.add_route('/rule/type/{ruleType}', delete_rule_type, methods=['DELETE'])
router.add_route('/rule/type/{ruleType}/rule/{ruleName}', add_rule, methods=['PUT'])
router.add_route('/rule/type/{ruleType}/rule/{ruleName}', get_rule, methods=['GET'])
router.add_route('/rule/type/{ruleType}/rule/{ruleName}', delete_rule, methods=['DELETE'])
router.add_route('/rule/type/{ruleType}/rule/search', find_rule, methods=['POST'])
router.add_route('/rule/status/update', update_rule_status, methods=['POST'])


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
