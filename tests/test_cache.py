from normalize_japanese_addresses import normalize
from normalize_japanese_addresses.normalize import get_prefectures, DEFAULT_ENDPOINT
from normalize_japanese_addresses.library.regex import set_ttl, clear_cache_of_cities, cache_cities, get_towns
from unittest.mock import patch, MagicMock

import json
from time import sleep


def test_normalize_cache_0001():
    """
    市区町村がキャッシュされていることを確認
    """
    
    # キャッシュをクリア
    clear_cache_of_cities()
    assert len(cache_cities) == 0

    # 住所正規化でキャッシュが有効になることを確認
    normalize('大阪府堺市北区新金岡町4丁1−8') 
    assert len(cache_cities) != 0

    # キャッシュ時間を保存
    cities_key = cache_cities.keys()
    key_city_0 = list(cities_key)[0]
    cache_cities_ttl_before = cache_cities[key_city_0][1]

    # キャッシュを利用していることを確認
    normalize('大阪府堺市北区新金岡町4丁1−8') 
    cities_key = cache_cities.keys()
    key_city_0 = list(cities_key)[0]
    cache_cities_ttl_after = cache_cities[key_city_0][1]
    assert cache_cities_ttl_before == cache_cities_ttl_after

    # キャッシュ時間を0にして、キャッシュが利用されないことを確認
    set_ttl(0)
    normalize('大阪府堺市北区新金岡町4丁1−8') 
    cities_key = cache_cities.keys()
    key_city_0 = list(cities_key)[0]
    cache_cities_ttl_after = cache_cities[key_city_0][1]
    assert cache_cities_ttl_before != cache_cities_ttl_after


@patch('normalize_japanese_addresses.library.regex.api_fetch')
def test_normalize_cache_0002(mock_api_fetch):
    """
    都道府県がキャッシュされていることを確認
    また、TTLが有効になっていることを確認
    """

    set_ttl(60)

    mock_text1 = '{"data": "dummy"}'
    mock_response = MagicMock()
    mock_response.text = mock_text1
    mock_api_fetch.return_value = mock_response

    # 初回の呼び出しではapi_fetchが呼ばれる
    result_prefecture = get_prefectures(DEFAULT_ENDPOINT)

    # 再度呼び出すと、キャッシュが有効になっている
    mock_text2 = '{"data": "dummy2"}'
    result_prefecture = get_prefectures(DEFAULT_ENDPOINT)
    assert json.loads(mock_text1) == result_prefecture
    assert json.loads(mock_text2) != result_prefecture

    # ttlを0にすると、キャッシュが有効にならずapi_fetchが呼ばれる
    set_ttl(0)

    mock_response.text = mock_text2
    mock_api_fetch.return_value = mock_response
    result_prefecture = get_prefectures(DEFAULT_ENDPOINT)
    assert json.loads(mock_text1) != result_prefecture
    assert json.loads(mock_text2) == result_prefecture

    # 再度呼び出しても、ttl=0のためキャッシュが有効にならずapi_fetchが呼ばれる
    result_prefecture = get_prefectures(DEFAULT_ENDPOINT)
    assert json.loads(mock_text1) != result_prefecture
    assert json.loads(mock_text2) == result_prefecture


@patch('normalize_japanese_addresses.library.regex.api_fetch')
def test_normalize_cache_0003(mock_api_fetch):
    """
    町がキャッシュされていることを確認
    また、TTLが有効になっていることを確認
    """
    def set_mock(mock_api_fetch, mock_text):
        mock_response = MagicMock()
        mock_response.text = mock_text
        mock_api_fetch.return_value = mock_response


    prefecture = '大阪府'
    city = '堺市北区'
    mock_text1 = '[{"town":"奥本町一丁","koaza":"","lat":34.581061,"lng":135.510333}]'
    mock_text2 = '[{"town":"奥本町二丁","koaza":"","lat":34.581061,"lng":135.510333}]'


    set_ttl(60)

    set_mock(mock_api_fetch, mock_text1)

    # 初回の呼び出しではapi_fetchが呼ばれる
    result_towns = get_towns(prefecture, city, DEFAULT_ENDPOINT)

    # 再度呼び出すと、キャッシュが有効になっている
    set_mock(mock_api_fetch, mock_text2)    

    result_towns = get_towns(prefecture, city, DEFAULT_ENDPOINT)
    assert json.loads(mock_text1) == result_towns
    assert json.loads(mock_text2) != result_towns

    # ttlを0にすると、キャッシュが有効にならずapi_fetchが呼ばれる
    set_ttl(0)

    # text1の内容をキャッシュ
    set_mock(mock_api_fetch, mock_text1)
    result_towns = get_towns(prefecture, city, DEFAULT_ENDPOINT)

    # text2の内容を返すようにする
    set_mock(mock_api_fetch, mock_text2)

    # キャッシュが有効にならずapi_fetchが呼ばれる
    result_towns = get_towns(prefecture, city, DEFAULT_ENDPOINT)
    assert json.loads(mock_text1) != result_towns
    assert json.loads(mock_text2) == result_towns
    