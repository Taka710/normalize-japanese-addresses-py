import urllib.parse

import requests


def apiFetch(endpoint: str = ''):
    if endpoint.startswith('http'):
        return requests.get(f'{endpoint}')
    elif endpoint.startswith('file'):
        filepath = urllib.parse.unquote(endpoint.replace("file://", ""))
        with open(filepath, encoding="utf-8") as fp:
            # ファイルから読み込んだ内容を擬似的にResponseオブジェクトに格納する
            res = requests.Response()
            res._content = fp.read().encode("utf-8")
            return res
    else:
        raise ValueError("Invalid endpoint type")
