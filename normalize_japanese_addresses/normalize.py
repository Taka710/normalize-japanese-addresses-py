import re
import json

from .library.api import apiFetch
from .library.regex import getPrefectureRegexes, getCityRegexes, getTownRegexes, replace_addr
from .library.utils import zen2han

SPACE = ' '
HYPHEN = '-'


def normalize(address: str, level: int = 3):
    """
    住所正規化
    :param address: 住所
    :param level: 正規化レベル（0:正規化不可 1:都道府県 2:市区町村 3:丁番地以降）
    :return: 正規化後の住所
    """

    pref = ''
    city = ''
    town = ''
    ref_level = 0

    addr = address

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
    response_prefs = apiFetch()
    prefectures: dict = json.loads(response_prefs.text)
    prefs: list = list(prefectures.keys())
    for _pref, reg in getPrefectureRegexes(prefs):
        if reg.match(addr):
            pref = _pref
            addr = addr[len(pref):]
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
        addr = re.sub('^大字', '', addr)

        for reg_list in getTownRegexes(pref, city):
            if reg_list[1].match(addr) is not None:
                town = reg_list[0]
                addr = addr[len(reg_list[1].match(addr).group()):]
                break

        addr = replace_addr(addr)

    # 戻り値のレベルを設定
    ref_level = ref_level + 1 if len(pref) > 0 else ref_level
    ref_level = ref_level + 1 if len(city) > 0 else ref_level
    ref_level = ref_level + 1 if len(town) > 0 else ref_level

    return {
        'pref': pref,
        'city': city,
        'town': town,
        'addr': addr,
        'level': ref_level,
    }
