import requests
import requests_cache

currentConfig = {
    'japaneseAddressesApi': 'https://geolonia.github.io/japanese-addresses/api/ja',
}

requests_cache.install_cache(expire_after=1)


def apiFetch(endpoint: str = ''):
    return requests.get(f'{endpoint}')
