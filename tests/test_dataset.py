from __future__ import unicode_literals

from geckoboard import Dataset, Field as F
from datetime import date, datetime, timedelta


def test_create_delete(session):
    fields = {
        'date': F.date('Date', unique=True),
        'datetime': F.datetime('Date Time'),
        'number': F.number('Number'),
        'percentage': F.percentage('Percentage'),
        'string': F.string('String'),
        'money': F.money('Dollars', 'USD'),
    }
    result = Dataset.create(session, 'test', fields)
    assert result.id == 'test'
    assert result.fields == fields

    invalid_field = F("invalid", None)

    for field in fields.values():
        assert field != invalid_field

    assert result.delete() is True


def _tmp_data(start_date, count):
    def _day_date(day_offset):
        return start_date + timedelta(days=day_offset)

    return [{
        'date': _day_date(offset),
        'datetime': datetime(2016, 9, 23),
        'number': 22,
        'percentage': 0.5,
        'string': "test string",
        'money': 7.95
    } for offset in range(count)]


def test_replace(tmp_dataset):
    data = _tmp_data(date(2016, 9, 23), 5)

    assert tmp_dataset.replace(data) is True


def test_append(tmp_dataset):
    data = _tmp_data(date(2016, 9, 23), 5)

    assert tmp_dataset.append(data, delete_by='date') is True
