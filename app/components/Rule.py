__author__ = 'mayank'
from app.components import Action, Condition, RuleType


class Rule(object):
    """
    Rule class. This class checks for basic rule JSON tempelate.
    """

    def __init__(self, rule_json):

        condition = 'condition'
        action = 'action'

        if condition not in rule_json.keys():
            raise KeyError('Expected field "{}" in the JSON object'.format(condition))

        if action not in rule_json.keys():
            raise KeyError('Expected field "{}" in the JSON object'.format(action))

        condition_obj = Condition.Condition(rule_json.get('condition', {})).get_value()
        action_obj = Action.Action(rule_json.get('action', {})).get_value()
        rule_type = rule_json.get('ruleType')
        rule_type_obj = RuleType.RuleType.fetch_value_from_store(rule_type)
        partial = rule_type_obj.get('partial', False)
        default_rule = rule_json.get('default', False)
        if not rule_type:
            raise KeyError('"ruleType" not defined')

        rule_name = rule_json.get('ruleName')
        if not rule_name:
            raise KeyError('"ruleName" not defined')

        self.rule = {
            action: action_obj,
            '_condition': condition_obj,
            "_meta": {
                "_ruleType": rule_type,
                '_ruleName': rule_name,
                '_partial': partial,
                '_enabled': True,
                '_default': default_rule
            },
            "_id": rule_type + rule_name
        }

    def get_rule(self):
        return self.rule


if __name__ == '__main__':
    print(Rule({'condition': {'a': {'operator': "ls", "dataType": "sadf", "value": "sdaf"}},
                'action': {'a': 2},
                'ruleType': 'luggage',
                'ruleName': 'luggage'}).get_rule())
