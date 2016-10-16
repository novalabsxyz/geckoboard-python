from __future__ import unicode_literals


def test_push(session):
    # We use a temporary created RAG widget if you need to re-record
    # this:
    #
    # Set GECKO_RECORD_MODE=once and GECKO_API_KEY to a valid api key
    #
    # Remove the tests/casettes/test_session.test_push.json casette
    #
    # Set widget below  to the id of a new (legacy) RAG widget
    #
    # Run the test. A new casette will be created. You can then safely
    # delete the above RAG widget
    widget = '120885-142a61f0-74a2-0134-3615-22000b5980c2'
    data = {
        'item': [
            {
                'value': 20,
                'text': 'Overdue'
            },
            {},
            {
                'value': 80,
                'text': 'Good'
            },
        ]
    }
    session.push(widget, data)
