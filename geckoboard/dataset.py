from __future__ import unicode_literals
from future.utils import iteritems
from iso4217 import Currency


class Field(object):
    def __init__(self, type, name, currency_code=None):
        self.type = type
        self.name = name
        self.currency_code = currency_code
        if currency_code is not None:
            self._money = getattr(Currency, currency_code.lower())

    def __eq__(self, other):
        return all([
            self.type == getattr(other, 'type', None),
            self.name == getattr(other, 'name', None),
            self.currency_code == getattr(other, "currency_code", None)
        ])

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def date(name):
        return Field('date', name)

    @staticmethod
    def datetime(name):
        return Field('datetime', name)

    @staticmethod
    def number(name):
        return Field('number', name)

    @staticmethod
    def percentage(name):
        return Field('percentage', name)

    @staticmethod
    def string(name):
        return Field('string', name)

    @staticmethod
    def money(name, currency_code):
        return Field('money', name, currency_code=currency_code)

    @classmethod
    def from_schema(cls, json):
        type = json.get('type')
        name = json.get('name')
        currency_code = json.get('currency_code', None)
        return cls(type, name, currency_code=currency_code)

    def to_schema(self):
        value = {
            'type': self.type,
            'name': self.name
        }
        if self.type == 'money':
            value['currency_code'] = self.currency_code
        return value

    def to_json(self, value):
        type = self.type
        if type == 'date':
            value = value.isoformat()
        elif type == 'datetime':
            value = value.isoformat() + 'Z'
        elif type == 'money':
            value = value * 10**self._money.exponent

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
        fields = {f[0]: Field.from_schema(f[1]) for f in iteritems(fields)}
        return cls(session, id, fields)

    @classmethod
    def create(cls, session, id, fields):
        json = {
            'fields': {f[0]: f[1].to_schema() for f in iteritems(fields)}
        }
        url = session.build_url(id)
        response = session.put(url, json=json)
        response.raise_for_status()
        return cls.from_json(session, response.json())

    def replace(self, data):
        def _fields_json(entry):
            fields = self.fields
            return {f[0]: fields[f[0]].to_json(f[1])
                    for f in iteritems(entry)}

        json = {
            'data': [_fields_json(entry) for entry in data]
        }
        session = self._session
        url = session.build_url(self.id, 'data')
        response = session.put(url, json=json)
        response.raise_for_status()
        return True

    def delete(self):
        session = self._session
        url = session.build_url(self.id)
        response = self._session.delete(url)
        response.raise_for_status()
        return True
