from normalize_japanese_addresses import normalize


# Python版に追加したテスト
def test_normalize_add_0001():
    assert normalize('鹿児島市山下町') == \
           {"pref": "鹿児島県", "city": "鹿児島市", "town": "山下町", "addr": "",
            "lat": 31.596716, "lng": 130.55643, "level": 3}


def test_normalize_add_0002():
    assert normalize('北海道札幌市西区24-2-2-3-3') ==            \
           {"pref": "北海道", "city": "札幌市西区", "town": "二十四軒二条二丁目", "addr": "3-3",
            "lat": 43.074273, "lng": 141.315099, "level": 3}


def test_normalize_add_0003():
    assert normalize('北海道札幌市西区24-2-2-3-3', level=1) ==            \
           {"pref": "北海道", "city": "", "town": "", "addr": "札幌市西区24-2-2-3-3",
            "lat": None, "lng": None, "level": 1}

