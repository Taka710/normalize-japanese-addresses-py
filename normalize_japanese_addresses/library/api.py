import urllib.parse

import requests


def api_fetch(endpoint: str = '') -> requests.Response:
    if endpoint.startswith('http'):
        return requests.get(endpoint)
    elif endpoint.startswith('file'):
        filepath = urllib.parse.unquote(endpoint.replace("file://", ""))
        with open(filepath, 'rb') as fp:
            res = requests.Response()
            res._content = fp.read()
            res.status_code = 200
            return res
    else:
        raise ValueError("Invalid endpoint type")
