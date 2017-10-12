__author__ = 'mayank'


class Action(object):

    def __init__(self, obj):
        if self._type_check(obj):
            self.value = obj
        else:
            raise TypeError('Action is not valid')

    @staticmethod
    def _type_check(value):
        if not isinstance(value, dict):
            raise TypeError('{} is expected to be \'dict\' type'.format(value))
        return True

    def get_value(self):
        return self.value
