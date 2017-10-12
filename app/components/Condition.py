__author__ = 'mayank'
from app.components import Field


class Condition(object):

    def __init__(self, obj):
        if not isinstance(obj, dict):
            raise TypeError('Expected <dict> found {}'.format(str(type(obj))))

        if obj == {}:
            raise ValueError('"condition" object cannot be empty')

        value = {}
        for field in self.validated_fields(obj):
            value.update(field)

        self.value = value

    def validated_fields(self, condition_obj):
        try:
            for key in condition_obj.keys():
                field = condition_obj[key]
                field_obj = {key: Field.Field(field).get_value()}
                yield field_obj
        except:
            raise TypeError('Field obj is not valid')

    @staticmethod
    def _validate_field_tempelate(field):
        if not isinstance(field, dict):
            raise TypeError("Field needs to be a JSON object")
        mandatory_key_list = ['operator', 'value', 'dataType']
        return True if set(mandatory_key_list) <= set(field.keys()) else False

    def get_value(self):
        return self.value
