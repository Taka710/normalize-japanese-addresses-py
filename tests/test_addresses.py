import numpy as np
import pandas as pd
import pytest

from normalize_japanese_addresses import normalize

addresses = pd.read_csv("./csv/addresses.csv")

testData = []
for _, address in addresses.iterrows():
    addr = address['住所']
    pref = address['都道府県']
    city = address['市区町村']
    town = address['町丁目']
    other = address['その他']

    # Nan判定
    addr = '' if addr is np.nan else addr
    pref = '' if pref is np.nan else pref
    city = '' if city is np.nan else city
    town = '' if town is np.nan else town
    other = '' if other is np.nan else other

    # \u3000を全角スペースに変換
    addr = addr.replace('\u3000', '　')
    pref = pref.replace('\u3000', '　')
    city = city.replace('\u3000', '　')
    town = town.replace('\u3000', '　')
    other = other.replace('\u3000', '　')

    testData.append([addr, pref, city, town, other])


@pytest.mark.parametrize("addr, pref, city, town, other", testData)
def test_address(addr: str, pref: str, city: str, town: str, other: str):
    level = 0

    # 戻り値のレベルを設定
    level = level + 1 if len(pref) > 0 else level
    level = level + 1 if len(city) > 0 else level
    level = level + 1 if len(town) > 0 else level

    res = normalize(addr)
    assert res["pref"] == pref
    assert res["city"] == city
    assert res["town"] == town
    assert res["addr"] == other
    assert res["level"] == level
