from __future__ import unicode_literals

import requests


class Session(requests.Session):

    def __init__(self, api_key,
                 base_url='https://api.geckoboard.com/datasets'):
        super(Session, self).__init__()
        self._base_url = base_url
        self.auth = requests.auth.HTTPBasicAuth(api_key, None)

    def build_url(self, *args, **kwargs):
        parts = [kwargs.get('base_url', self._base_url)]
        parts.extend([part for part in args if part is not None])
        return '/'.join(parts)
