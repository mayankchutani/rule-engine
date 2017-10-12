__author__ = 'mayank'


class MongoQueryBuilder(object):

    def __init__(self, args, query=None):
        if query is None:
            query = {}
        for field, value in args.items():
            query.update({'condition.' + field + '.value': value})
        self.query = query

    def get_query(self):
        print(self.query)
        return self.query



mongo_operator = {
    'less_than': '$lt',
    'greater_than': '$gt',
    'less_than_or_equal_to': '$lte',
    'greater_than_or_equal_to': '$gte',
    'equal_to': '$eq',
    'regex': '$regex'
}
