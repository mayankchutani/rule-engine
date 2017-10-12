__author__ = 'mayank'


class Field(object):

    def __init__(self, obj):
        if self._validate_template(obj):
            self.value = {
                'operator': obj.get('operator'),
                'value': obj.get('value'),
                'dataType': obj.get('dataType'),
                'caseSensitive': obj.get('caseSensitive', True),
                'weight': obj.get('weight', 1)
            }
        else:
            raise TypeError('Field is not valid')

    @staticmethod
    def _validate_template(field):
        if not isinstance(field, dict):
            raise TypeError("Field needs to be a JSON object")
        mandatory_key_list = ['operator', 'value', 'dataType']
        return True if set(mandatory_key_list) <= set(field.keys()) else False

    def get_value(self):
        return self.value
