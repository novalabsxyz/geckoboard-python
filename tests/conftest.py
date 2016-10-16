from __future__ import unicode_literals

import os
import pytest
from betamax import Betamax
from betamax_serializers import pretty_json
from betamax_matchers import json_body

from requests.auth import _basic_auth_str
from geckoboard import Session, Dataset, Field as F

Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
Betamax.register_request_matcher(json_body.JSONBodyMatcher)
API_TOKEN = os.environ.get('GECKO_API_KEY', 'X' * 10)
RECORD_MODE = os.environ.get('GECKO_RECORD_MODE', 'none')
RECORD_FOLDER = os.environ.get('GECKO_RECORD_FOLDER', 'tests/cassettes')

with Betamax.configure() as config:
    config.cassette_library_dir = RECORD_FOLDER
    record_mode = RECORD_MODE
    cassette_options = config.default_cassette_options
    cassette_options['record_mode'] = record_mode
    cassette_options['serialize_with'] = 'prettyjson'
    config.define_cassette_placeholder('<AUTH_TOKEN>',
                                       _basic_auth_str(API_TOKEN, None))
    config.define_cassette_placeholder('<AUTH_TOKEN>', API_TOKEN)


@pytest.fixture
def recorder(request):
    """Generate and start a recorder using a geckoboard.Session."""
    cassette_name = ''

    if request.module is not None:
        cassette_name += request.module.__name__ + '.'

    if request.cls is not None:
        cassette_name += request.cls.__name__ + '.'

    cassette_name += request.function.__name__

    session = Session(API_TOKEN)
    recorder = Betamax(session)

    matchers = ['method', 'uri']
    recorder.use_cassette(cassette_name,
                          match_requests_on=matchers)
    recorder.start()
    request.addfinalizer(recorder.stop)
    return recorder


@pytest.fixture
def session(recorder):
    """Return the session object used by the current recorder."""
    return recorder.session


@pytest.fixture
def tmp_dataset(session):
    fields = {
        'date': F.date('Date'),
        'datetime': F.datetime('Date Time'),
        'number': F.number('Number'),
        'percentage': F.percentage('Percentage'),
        'string': F.string('String'),
        'money': F.money('Dollars', 'USD'),
    }
    dataset = Dataset.create(session, 'test', fields)
    yield dataset
    dataset.delete()
