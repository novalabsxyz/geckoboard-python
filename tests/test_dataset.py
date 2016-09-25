from __future__ import unicode_literals

from geckoboard import Dataset, Field as F
from datetime import date, datetime, timedelta
from builtins import dict


def test_create_delete(session):
    fields = {
        'date': F.date('Date'),
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


def test_replace(tmp_dataset):
    start_date = date(2016, 9, 23)

    def _day_date(day_offset):
        return start_date + timedelta(days=day_offset)

    data = [{
        'date': _day_date(offset),
        'datetime': datetime(2016, 9, 23),
        'number': 22,
        'percentage': 0.5,
        'string': "test string",
        'money': 7.95
    } for offset in range(5)]

    assert tmp_dataset.replace(data) is True
