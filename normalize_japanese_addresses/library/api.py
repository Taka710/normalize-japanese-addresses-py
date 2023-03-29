import urllib.parse

import requests


def api_fetch(endpoint: str = ''):
    if endpoint.startswith('http'):
        return requests.get(endpoint)
    elif endpoint.startswith('file'):
        filepath = urllib.parse.unquote(endpoint.replace("file://", ""))
        with open(filepath, 'rb') as fp:
            res = requests.Response()
            res.raw = fp
            return res
    else:
        raise ValueError("Invalid endpoint type")
