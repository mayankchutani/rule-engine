__author__ = 'mayank'
import dateutil.parser
import re


class Base(object):

    def __init__(self, **kwargs):
        pass

    def equal_to(self, value):
        pass

    @staticmethod
    def _type_check(value):
        pass

    def contains(self, value):
        pass

    def greater_than(self, value):
        pass

    def less_than(self, value):
        pass

    def greater_than_or_equal_to(self, value):
        pass

    def less_than_or_equal_to(self, value):
        pass


class String(Base):

    def __init__(self, value, **kwargs):
        super(String, self).__init__()
        if self._type_check(value):
            self.value = value
        self.case_sensitive = kwargs.get('case_sensitive', True)

    @staticmethod
    def _type_check(value):
        if not isinstance(value, str):
            raise TypeError('{} is expected to be \'str\' type'.format(value))
        return True

    def equal_to(self, value):
        if self._type_check(value):
            if not self.case_sensitive:
                current_value = self.value.lower()
                search_value = value.lower()
            else:
                current_value = self.value
                search_value = value
            return current_value == search_value

    def contains(self, value):
        if not self.case_sensitive:
            current_value = self.value.lower()
            search_value = value.lower()
        else:
            current_value = self.value
            search_value = value
        return current_value in search_value

    def regex(self, value):
        regex_string = value
        if self.case_sensitive:
            compiled_regex = re.compile(r'{}'.format(regex_string))
        else:
            compiled_regex = re.compile(r'{}'.format(regex_string), flags=re.IGNORECASE)
        match = compiled_regex.search(self.value)
        return True if match else False

    def pre(self, value):
        if not self.case_sensitive:
            current_value = self.value.lower()
            search_value = value.lower()
        else:
            current_value = self.value
            search_value = value
        return search_value.startswith(current_value)

    def post(self, value):
        if not self.case_sensitive:
            current_value = self.value.lower()
            search_value = value.lower()
        else:
            current_value = self.value
            search_value = value
        return search_value.endswith(current_value)


class Number(Base):

    def __init__(self, value, **kwargs):
        super(Number, self).__init__()
        if self._type_check(value):
            self.value = value

    @staticmethod
    def _type_check(value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('{} is expected to be \'int\' or \'float\' type'.format(value))
        return True

    def equal_to(self, value):
        return self.value == value

    def less_than(self, value):
        return self.value < value

    def greater_than(self, value):
        return self.value > value

    def less_than_or_equal_to(self, value):
        return self.value <= value

    def greater_than_or_equal_to(self, value):
        return self.value >= value


class Date(object):

    def __init__(self, value, **kwargs):
        super(Date, self).__init__()
        if self._type_check(value):
            self.value = value
        self.date_time = Date._iso_to_datetime(value)

    @staticmethod
    def _iso_to_datetime(value):
        try:
            date_time = dateutil.parser.parse(value)
        except ValueError as err:
            raise err
        return date_time

    def _type_check(self, value):
        if not isinstance(value, str):
            raise TypeError('{} is expected to be \'str\' (iso date format) type'.format(value))
        return True

    def equal_to(self, value):
        return self.date_time == Date._iso_to_datetime(value)

    def less_than(self, value):
        return self.date_time < Date._iso_to_datetime(value)

    def greater_than(self, value):
        return self.date_time > Date._iso_to_datetime(value)

    def less_than_or_equal_to(self, value):
        return self.date_time <= Date._iso_to_datetime(value)

    def greater_than_or_equal_to(self, value):
        return self.date_time >= Date._iso_to_datetime(value)
