from __future__ import unicode_literals
from future.utils import viewitems
from iso4217 import Currency


class Field(object):
    def __init__(self, type, name, currency_code=None, unique=False):
        self.type = type
        self.name = name
        self.currency_code = currency_code
        self.unique = unique
        if currency_code is not None:
            self._money = getattr(Currency, currency_code.lower())

    def __eq__(self, other):
        return all([
            self.type == getattr(other, 'type', None),
            self.name == getattr(other, 'name', None),
            self.unique == getattr(other, 'unique', None),
            self.currency_code == getattr(other, "currency_code", None)
        ])

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def date(name, unique=False):
        return Field('date', name,
                     unique=unique)

    @staticmethod
    def datetime(name, unique=False):
        return Field('datetime', name,
                     unique=unique)

    @staticmethod
    def number(name, unique=False):
        return Field('number', name,
                     unique=unique)

    @staticmethod
    def percentage(name, unique=False):
        return Field('percentage', name,
                     unique=unique)

    @staticmethod
    def string(name, unique=False):
        return Field('string', name,
                     unique=unique)

    @staticmethod
    def money(name, currency_code, unique=False):
        return Field('money', name,
                     currency_code=currency_code,
                     unique=unique)

    @classmethod
    def from_schema(cls, json, unique=False):
        type = json.get('type')
        name = json.get('name')
        currency_code = json.get('currency_code', None)
        return cls(type, name,
                   currency_code=currency_code,
                   unique=unique)

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
        unique_fields = frozenset(json.get('unique_by', []))

        def _build_field(name, value):
            unique = name in unique_fields
            return Field.from_schema(value, unique=unique)

        fields = {f[0]: _build_field(f[0], f[1]) for f in viewitems(fields)}
        return cls(session, id, fields)

    @classmethod
    def create(cls, session, id, fields):
        json = {
            'fields': {f[0]: f[1].to_schema() for f in viewitems(fields)}
        }
        unique_by = [f[0] for f in viewitems(fields) if f[1].unique]
        if unique_by:
            json['unique_by'] = unique_by
        url = session.build_url('datasets', id)
        response = session.put(url, json=json)
        response.raise_for_status()
        return cls.from_json(session, response.json())

    def _build_data_json(self, data):
        def _fields_json(entry):
            fields = self.fields
            return {f[0]: fields[f[0]].to_json(f[1])
                    for f in viewitems(entry)}

        json = {
            'data': [_fields_json(entry) for entry in data]
        }
        return json

    def replace(self, data):
        session = self._session
        url = session.build_url('datasets', self.id, 'data')
        json = self._build_data_json(data)

        response = session.put(url, json=json)
        response.raise_for_status()
        return True

    def append(self, data, delete_by=None):
        session = self._session
        url = session.build_url('datasets', self.id, 'data')
        json = self._build_data_json(data)
        if delete_by is not None:
            json['delete_by'] = delete_by

        response = session.post(url, json=json)
        response.raise_for_status()
        return True

    def delete(self):
        session = self._session
        url = session.build_url('datasets', self.id)
        response = self._session.delete(url)
        response.raise_for_status()
        return True
