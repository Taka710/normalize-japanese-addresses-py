import re
import json
import unicodedata

from typing import Tuple, Optional

from .library.regex import (
    get_prefectures,
    get_prefecture_regexes,
    get_city_regexes,
    replace_addr,
    normalize_town_name,
    set_ttl,
)
from .library.patchAddr import patch_addr
from .library.utils import zenkaku_to_hankaku

SPACE: str = " "
HYPHEN: str = "-"

# japanese-addressesのendpoint
DEFAULT_ENDPOINT = "https://geolonia.github.io/japanese-addresses/api/ja"

# オプションのレベル設定
DEFAULT_LEVEL = 3


def normalize(address: str, **kwargs) -> str:
    """
    住所正規化
    :param address: 住所
    :param kwargs: オプション（level:正規化レベル）
    :return: 正規化後の住所
    """

    # オプションの設定
    level, endpoint = set_options(kwargs)

    # 初期設定
    addr, pref, city, town, lat, lng, ref_level = get_address_parts(address)

    # 住所の前処理
    addr = preprocessing_address(addr)

    # 都道府県情報を取得
    prefectures = get_prefectures(endpoint)
    prefectures_list: list = list(prefectures.keys())

    # 都道府県の正規化
    addr, pref = normalize_prefecture_names(
        addr=addr,
        prefectures=prefectures,
        prefectures_list=prefectures_list,
        endpoint=endpoint,
    )

    # 市区町村の正規化
    if pref != "" and level >= 2:
        addr, city = normalize_city_names(addr=addr, prefectures=prefectures, pref=pref)

    # 町丁目以降の正規化
    if city != "" and level >= 3:
        addr, town, lat, lng = normalize_after_town_names(
            addr=addr, pref=pref, city=city, endpoint=endpoint
        )

    # 住所の後処理
    addr = patch_addr(pref, city, town, addr)

    # 戻り値のレベルを設定
    ref_level = set_level(pref, city, town, ref_level)

    return {
        "pref": pref,
        "city": city,
        "town": town,
        "addr": addr,
        "lat": lat,
        "lng": lng,
        "level": ref_level,
    }


def set_options(options: dict) -> tuple:
    """
    オプションの設定
    """
    level = options.get("level", DEFAULT_LEVEL)
    endpoint = options.get("endpoint", DEFAULT_ENDPOINT)
    option_ttl = options.get("ttl", None)
    if option_ttl is not None and isinstance(option_ttl, int):
        set_ttl(option_ttl)
    return level, endpoint


def get_address_parts(
    address: str,
) -> Tuple[str, str, str, str, Optional[float], Optional[float], int]:
    """
    住所の初期設定
    """
    # 初期化
    pref: str = ""
    city: str = ""
    town: str = ""
    lat: Optional[float] = None
    lng: Optional[float] = None
    ref_level: int = 0

    # 初期住所設定
    addr: str = unicodedata.normalize("NFC", address)
    return addr, pref, city, town, lat, lng, ref_level


def replace_spaces(addr: str) -> str:
    """
    全角スペースを半角スペースに置換する
    """
    addr = addr.replace("　", SPACE).replace(" ", SPACE)
    addr = re.sub(" +", SPACE, addr)
    return addr


def replace_hyphen_like_characters_after_digits(addr: str) -> str:
    """
    数字の後にあるハイフンのような文字をハイフンに置換する
    """
    hyphen_iter = re.finditer(
        "([0-9０-９一二三四五六七八九〇十百千][-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])|([-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])[0-9０-９一二三四五六七八九〇十]",
        addr,
    )
    for m in hyphen_iter:
        from_value = m.group()
        replace_value = re.sub("[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]", HYPHEN, from_value)
        addr = addr.replace(from_value, replace_value)
    return addr


def remove_spaces_before_town_city_district_name(addr: str) -> str:
    """
    町丁目名の前にあるスペースを削除する
    """
    hyphen_iter = re.finditer("(.+)(丁目?|番([町地丁])|条|軒|線|([のノ])町|地割)", addr)
    for m in hyphen_iter:
        from_value = m.group()
        replace_value = from_value.replace(SPACE, "")
        addr = addr.replace(from_value, replace_value)
    return addr


def remove_spaces_before_ward_or_gun(addr: str) -> str:
    """
    区、郡以前のスペースは全て削除する
    """
    hyphen_iter = re.finditer("(.+)((郡.+(町|村))|((市|巿).+(区|區)))", addr)
    for m in hyphen_iter:
        from_value = m.group()
        replace_value = from_value.replace(SPACE, "")
        addr = addr.replace(from_value, replace_value)
    return addr


def remove_leading_spaces_before_the_first_arabic_numeral(addr: str) -> str:
    """
    最初のアラビア数字の前にあるスペースを削除する
    """
    hyphen_iter = re.finditer(".+?[0-9一二三四五六七八九〇十百千]-", addr)
    for m in hyphen_iter:
        from_value = m.group()
        replace_value = from_value.replace(SPACE, "")
        addr = addr.replace(from_value, replace_value)
        break
    return addr


def preprocessing_address(addr: str) -> str:
    """
    住所の前処理
    """

    # スペース変換
    addr = replace_spaces(addr)

    # 全角の英数字は半角に変換
    addr = zenkaku_to_hankaku(addr)

    # 数字の後に紐づくハイフン類似文字をすべて半角ハイフンに変換
    addr = replace_hyphen_like_characters_after_digits(addr)

    # 町丁目名以前のスペースはすべて削除
    addr = remove_spaces_before_town_city_district_name(addr)

    # // 区、郡以前のスペースはすべて削除
    addr = remove_spaces_before_ward_or_gun(addr)

    # 1番はじめに出てくるアラビア数字以前のスペースを削除
    addr = remove_leading_spaces_before_the_first_arabic_numeral(addr)

    return addr


def normalize_prefecture_names(
    addr: str, prefectures: dict, prefectures_list: list, endpoint: str
) -> str:
    """
    都道府県名を正規化する
    """
    pref = ""
    for _pref, reg in get_prefecture_regexes(prefectures_list, False):
        if reg.match(addr):
            pref = _pref
            addr = addr[len(reg.match(addr)[0]) :]
            break

    if pref == "":
        # 都道府県が省略されている
        matched = []

        for _pref, cities in prefectures.items():
            addr = addr.strip()
            for _city, reg in get_city_regexes(_pref, cities):
                match = reg.match(addr)
                if match is not None:
                    matched.append(
                        {
                            "pref": _pref,
                            "city": _city,
                            "addr": addr[len(match.group()) :],
                        }
                    )

        # マッチする都道府県が複数ある場合は町名まで正規化して都道府県名を判別する。（例: 東京都府中市と広島県府中市など）
        if len(matched) == 1:
            pref = matched[0]["pref"]
        else:
            for match in matched:
                normalized = normalize_town_name(
                    match["addr"], match["pref"], match["city"], endpoint
                )

                if normalized is not None:
                    pref = match["pref"]
                    break

    # 都道府県が省略されている場合に都道府県を抽出（誤検知防止のため、省略
    if pref == "":
        for _pref, reg in get_prefecture_regexes(prefectures_list, True):
            if reg.match(addr):
                pref = _pref
                addr = addr[len(reg.match(addr)[0]) :]
                break

    return addr, pref


def normalize_city_names(addr: str, prefectures: dict, pref: str) -> Tuple[str, str]:
    """
    市区町村名を正規化する
    """
    city = ""
    cities = prefectures[pref]

    for _city, reg in get_city_regexes(pref, cities):
        match = reg.match(addr)
        if match is not None:
            city = _city
            addr = addr[len(match.group()) :]
            break

    return addr, city


def normalize_after_town_names(
    addr: str, pref: str, city: str, endpoint: str
) -> Tuple[str, str, float, float]:
    """
    町名以降の住所を正規化する
    """

    town = ""
    lat = None
    lng = None

    normalized = normalize_town_name(addr, pref, city, endpoint)
    if normalized is not None:
        _town = normalized["town"]
        town = _town["originalTown"] if "originalTown" in _town else _town["town"]
        addr = normalized["addr"]
        lat = normalized["lat"]
        lng = normalized["lng"]

    addr = replace_addr(addr)

    return addr, town, lat, lng


def set_level(pref, city, town, ref_level) -> int:
    """
    住所のレベルを設定する
    """
    ref_level += len(pref) > 0
    ref_level += len(city) > 0
    ref_level += len(town) > 0
    return ref_level
