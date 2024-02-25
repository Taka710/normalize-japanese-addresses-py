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


# @geolonia/japanese-addresses にある住所データをローカルから読み込むテスト
# テスト実行用に下記コマンドで /tmp/ 以下に住所データを保存する
# curl -sL https://github.com/geolonia/japanese-addresses/archive/refs/heads/master.tar.gz | tar xvfz - -C /tmp/
def test_normalize_add_0004():
    assert normalize('北海道札幌市西区24-2-2-3-3', level=3, endpoint='file:///tmp/japanese-addresses-master/api/ja') ==            \
           {"pref": "北海道", "city": "札幌市西区", "town": "二十四軒二条二丁目", "addr": "3-3",
            "lat": 43.074273, "lng": 141.315099, "level": 3}

# issue #8
# @geolonia/normalize-japanese-addressesで実行した結果と同じになることを確認する
# {pref: '北海道', city: '札幌市中央区', town: '宮の森四条十丁目', addr: '', level: 3}
def test_normalize_add_0005():
    assert normalize('北海道札幌市中央区宮の森４条１０丁目') == \
              {"pref": "北海道", "city": "札幌市中央区", "town": "宮の森四条十丁目", "addr": "",
                "lat": 43.060356, "lng": 141.298776, "level": 3}

# issue #9
# 茨城県行方市をnormalizeするとUnboundLocalErrorが発生する件の修正
def test_normalize_add_0006():
    res = normalize('茨城県行方市')
    assert res['pref'] == '茨城県'
    assert res['city'] == '行方市'
    assert res['level'] == 2

def test_normalize_add_0007():
    res = normalize('千葉県茂原市')
    assert res['pref'] == '千葉県'
    assert res['city'] == '茂原市'
    assert res['level'] == 2
