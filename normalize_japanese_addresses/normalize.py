import re
import json
import unicodedata

from .library.regex import getPrefectures, getPrefectureRegexes, getCityRegexes, replace_addr, normalizeTownName, match_banchi_go_pattern
from .library.patchAddr import patchAddr
from .library.utils import zen2han

SPACE = ' '
HYPHEN = '-'

# japanese-addressesのendpoint
endpoint = 'https://geolonia.github.io/japanese-addresses/api/ja'

# オプションのレベル設定
level = 3


def normalize(address: str, **kwargs):
    """
    住所正規化
    :param address: 住所
    :param kwargs: オプション（level:正規化レベル）
    :return: 正規化後の住所
    """

    # オプションの設定
    setOptions(kwargs)

    # 戻り値用
    pref = ''
    city = ''
    town = ''
    lat = None
    lng = None
    ref_level = 0

    # 初期住所設定
    addr = unicodedata.normalize('NFC', address)

    # スペース変換
    addr = addr.replace('　', SPACE).replace(' ', SPACE)
    addr = re.sub(' +', SPACE, addr)

    # 全角の英数字は半角に変換
    addr = zen2han(addr)

    # 数字の後に紐づくハイフン類似文字をすべて半角ハイフンに変換
    hyphen_iter = re.finditer(
        '([0-9０-９一二三四五六七八九〇十百千][-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])|([-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])[0-9０-９一二三四五六七八九〇十]',
        addr)
    for m in hyphen_iter:
        from_value = m.group()
        replace_value = re.sub('[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]', HYPHEN, from_value)
        addr = addr.replace(from_value, replace_value)

    # 町丁目名以前のスペースはすべて削除
    hyphen_iter = re.finditer('(.+)(丁目?|番([町地丁])|条|軒|線|([のノ])町|地割)', addr)
    for m in hyphen_iter:
        from_value = m.group()
        replace_value = from_value.replace(SPACE, '')
        addr = addr.replace(from_value, replace_value)

    # 1番はじめに出てくるアラビア数字以前のスペースを削除
    hyphen_iter = re.finditer('.+?[0-9一二三四五六七八九〇十百千]-', addr)
    for m in hyphen_iter:
        from_value = m.group()
        replace_value = from_value.replace(SPACE, '')
        addr = addr.replace(from_value, replace_value)
        break

    # 都道府県の正規化
    response_prefs = getPrefectures(endpoint)
    prefectures: dict = json.loads(response_prefs.text)
    prefs: list = list(prefectures.keys())
    for _pref, reg in getPrefectureRegexes(prefs):
        if reg.match(addr):
            pref = _pref
            addr = addr[len(reg.match(addr)[0]):]
            break

    if pref == '':
        # 都道府県が省略されている
        matched = []

        for _pref, cities in prefectures.items():

            addr = addr.strip()
            for _city, reg in getCityRegexes(_pref, cities):
                match = reg.match(addr)
                if match is not None:
                    matched.append(
                        {
                            'pref': _pref,
                            'city': _city,
                            'addr': addr[len(match.group()):]
                        }
                    )

        # マッチする都道府県が複数ある場合は町名まで正規化して都道府県名を判別する。（例: 東京都府中市と広島県府中市など）
        if len(matched) == 1:
            pref = matched[0]['pref']
        else:
            for match in matched:
                normalized = normalizeTownName(
                    match['addr'],
                    match['pref'],
                    match['city'],
                    endpoint
                )

                if normalized is not None:
                    pref = match['pref']
                    break

    # 都道府県が省略されている場合に都道府県を抽出（誤検知防止のため、省略
    if pref == '':
        for _pref, reg in getPrefectureRegexes(prefs, True):
            if reg.match(addr):
                pref = _pref
                addr = addr[len(reg.match(addr)[0]):]
                break

    # 市区町村の正規化
    if pref != '' and level >= 2:
        cities = prefectures[pref]

        for _city, reg in getCityRegexes(pref, cities):
            match = reg.match(addr)
            if match is not None:
                city = _city
                addr = addr[len(match.group()):]
                break

    # 町丁目以降の正規化
    if city != '' and level >= 3:
        
        banchiGoQueue = []
        for pattern in match_banchi_go_pattern:
            match = re.match(pattern, addr)
            if match is not None:
                banchiGoQueue.append(match[0])
                addr = addr.replace(match[0], '')
            

        normalized = normalizeTownName(addr, pref, city, endpoint)
        if normalized is not None:
            _town = normalized['town']
            town = _town['originalTown'] if 'originalTown' in _town else _town['town']
            addr = normalized['addr']
            lat = normalized['lat']
            lng = normalized['lng']

        addr = ''.join(banchiGoQueue) + addr
        
        addr = replace_addr(addr)

    addr = patchAddr(pref, city, town, addr)

    # 戻り値のレベルを設定
    ref_level = ref_level + 1 if len(pref) > 0 else ref_level
    ref_level = ref_level + 1 if len(city) > 0 else ref_level
    ref_level = ref_level + 1 if len(town) > 0 else ref_level

    return {
        'pref': pref,
        'city': city,
        'town': town,
        'addr': addr,
        'lat': lat,
        'lng': lng,
        'level': ref_level,
    }


def setOptions(options: dict):
    global level
    global endpoint

    # オプションの設定
    if "level" in options:
        level = options["level"]

    if "endpoint" in options:
        endpoint = options["endpoint"]
