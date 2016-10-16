from __future__ import unicode_literals

import requests


class Session(requests.Session):

    def __init__(self, api_key):
        super(Session, self).__init__()
        self._base_url = 'https://api.geckoboard.com'
        self._push_url = 'https://push.geckoboard.com/v1'
        self._api_key = api_key
        self.auth = requests.auth.HTTPBasicAuth(api_key, None)

    def build_url(self, *args, **kwargs):
        parts = [kwargs.get('base_url', self._base_url)]
        parts.extend([part for part in args if part is not None])
        return '/'.join(parts)

    def push(self, widget_id, data):
        json = {
            'api_key': self._api_key,
            'data': data
        }
        url = self.build_url('send', widget_id, base_url=self._push_url)
        res = self.post(url, json=json)
        res.raise_for_status()
        return True
