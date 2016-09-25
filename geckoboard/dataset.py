from __future__ import unicode_literals
from future.utils import iteritems
from iso4217 import Currency


class Field(object):
    def __init__(self, id, type, name, currency_code=None):
        self.id = id
        self.type = type
        self.name = name
        self.currency_code = currency_code
        if currency_code is not None:
            self._money = getattr(Currency, currency_code.lower())

    @staticmethod
    def date(id, name):
        return Field('date', id, name)

    @staticmethod
    def datetime(id, name):
        return Field('datetime', id, name)

    @staticmethod
    def number(id, name):
        return Field('number', id, name)

    @staticmethod
    def percentage(id, name):
        return Field('percentage', id, name)

    @staticmethod
    def string(id, name):
        return Field('string', id, name)

    @staticmethod
    def money(id, name, currency_code):
        return Field('money', id, name)

    @classmethod
    def from_schema(cls, id, json):
        type = json.get('type')
        name = json.get('name')
        currency_code = json.get('currency_code', None)
        return cls(id, type, name, currency_code=currency_code)

    def to_schema(self):
        value = {
            'type': self.type,
            'name': self.name
        }
        if self.type == 'money':
            value['currency_code'] = self.currency_code

        return value

    def to_json(self, value):
        if type == 'date':
            value = value.isoformat()
        elif type == 'datetime':
            value = value.isoformat() + 'Z'
        elif type == 'money':
            value = value * self._money.exponent

        return value


class Dataset(object):

    def __init__(self, session, id, fields):
        self._session = session
        self.id = id
        self.fields = fields

    @classmethod
    def from_json(cls, session, json):
        id = json.get('id')
        fields = json.get('fields')
        fields = {f[0]: Field.from_schema(f[0], f[1])
                  for f in iteritems(fields)}
        return cls(session, id, fields)

    @classmethod
    def create(cls, session, id, fields):
        json = {
            'fields': {field.id: field.to_schema() for field in fields}
        }
        url = session.build_url(id)
        response = session.put(url, json=json)
        response.raise_for_error()
        cls.from_json(session, response.json())

    def replace(self, data):
        session = self._session
        fields = self.fields

        def _fields_json(entry):
            return {f[0]: fields[f[0]].to_json(f[1])
                    for f in iteritems(entry)}

        json = {
            'data': [_fields_json(entry) for entry in data]
        }
        url = session.build_url(self.id, 'data')
        response = session.put(url, json=json)
        response.raise_for_error()
        return True
