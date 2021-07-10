import requests


def apiFetch(endpoint: str = ''):
    return requests.get(f'{endpoint}')
