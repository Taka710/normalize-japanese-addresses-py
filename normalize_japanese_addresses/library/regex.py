import re
import json
import urllib.parse
from typing import List, Dict, Any, Optional, Union, Generator, Tuple, Callable, Pattern

import kanjize
from cachetools import TTLCache
import time

import functools
from functools import wraps

from .api import api_fetch
from .utils import kan2num, find_kanji_numbers

JIS_OLD_KANJI = (
    "亞,圍,壹,榮,驛,應,櫻,假,會,懷,覺,樂,陷,歡,氣,戲,據,挾,區,徑,溪,輕,藝,儉,圈,權,嚴,恆,國,齋,雜,蠶,殘,兒,實,釋,從,縱,敍,燒,條,剩,壤,釀,眞,盡,醉,髓,聲,竊,"
    "淺,錢,禪,爭,插,騷,屬,對,滯,擇,單,斷,癡,鑄,敕,鐵,傳,黨,鬪,屆,腦,廢,發,蠻,拂,邊,瓣,寶,沒,滿,藥,餘,樣,亂,兩,禮,靈,爐,灣,惡,醫,飮,營,圓,歐,奧,價,繪,擴,學,"
    "罐,勸,觀,歸,犧,擧,狹,驅,莖,經,繼,缺,劍,檢,顯,廣,鑛,碎,劑,參,慘,絲,辭,舍,壽,澁,肅,將,證,乘,疊,孃,觸,寢,圖,穗,樞,齊,攝,戰,潛,雙,莊,裝,藏,續,體,臺,澤,膽,"
    "彈,蟲,廳,鎭,點,燈,盜,獨,貳,霸,賣,髮,祕,佛,變,辯,豐,飜,默,與,譽,謠,覽,獵,勵,齡,勞,壓,爲,隱,衞,鹽,毆,穩,畫,壞,殼,嶽,卷,關,顏,僞,舊,峽,曉,勳,惠,螢,鷄,縣,"
    "險,獻,驗,效,號,濟,册,棧,贊,齒,濕,寫,收,獸,處,稱,奬,淨,繩,讓,囑,愼,粹,隨,數,靜,專,踐,纖,壯,搜,總,臟,墮,帶,瀧,擔,團,遲,晝,聽,遞,轉,當,稻,讀,惱,拜,麥,拔,"
    "濱,竝,辨,舖,襃,萬,譯,豫,搖,來,龍,壘,隸,戀,樓,鰺,鶯,蠣,攪,竈,灌,諫,頸,礦,蘂,靱,賤,壺,礪,檮,濤,邇,蠅,檜,儘,藪,籠,彌,麩".split(
        ","
    )
)

JIS_NEW_KANJI = (
    "亜,囲,壱,栄,駅,応,桜,仮,会,懐,覚,楽,陥,歓,気,戯,拠,挟,区,径,渓,軽,芸,倹,圏,権,厳,恒,国,斎,雑,蚕,残,児,実,釈,従,縦,叙,焼,条,剰,壌,醸,真,尽,酔,髄,声,窃,"
    "浅,銭,禅,争,挿,騒,属,対,滞,択,単,断,痴,鋳,勅,鉄,伝,党,闘,届,脳,廃,発,蛮,払,辺,弁,宝,没,満,薬,余,様,乱,両,礼,霊,炉,湾,悪,医,飲,営,円,欧,奥,価,絵,拡,学,"
    "缶,勧,観,帰,犠,挙,狭,駆,茎,経,継,欠,剣,検,顕,広,鉱,砕,剤,参,惨,糸,辞,舎,寿,渋,粛,将,証,乗,畳,嬢,触,寝,図,穂,枢,斉,摂,戦,潜,双,荘,装,蔵,続,体,台,沢,胆,"
    "弾,虫,庁,鎮,点,灯,盗,独,弐,覇,売,髪,秘,仏,変,弁,豊,翻,黙,与,誉,謡,覧,猟,励,齢,労,圧,為,隠,衛,塩,殴,穏,画,壊,殻,岳,巻,関,顔,偽,旧,峡,暁,勲,恵,蛍,鶏,県,"
    "険,献,験,効,号,済,冊,桟,賛,歯,湿,写,収,獣,処,称,奨,浄,縄,譲,嘱,慎,粋,随,数,静,専,践,繊,壮,捜,総,臓,堕,帯,滝,担,団,遅,昼,聴,逓,転,当,稲,読,悩,拝,麦,抜,"
    "浜,並,弁,舗,褒,万,訳,予,揺,来,竜,塁,隷,恋,楼,鯵,鴬,蛎,撹,竃,潅,諌,頚,砿,蕊,靭,賎,壷,砺,梼,涛,迩,蝿,桧,侭,薮,篭,弥,麸".split(
        ","
    )
)

ttl = 60 * 60 * 24 * 7
cache_prefecture = TTLCache(maxsize=300, ttl=ttl)
cache_cities = {}
cache_towns = TTLCache(maxsize=300, ttl=ttl)


def set_ttl(ttl_value: int) -> None:
    global ttl
    global cache_prefecture
    global cache_towns

    ttl = ttl_value
    cache_prefecture = TTLCache(maxsize=300, ttl=ttl)
    cache_prefecture.clear()
    cache_towns = TTLCache(maxsize=300, ttl=ttl)
    cache_towns.clear()
    clear_cache_of_cities()

def clear_cache_of_cities() -> None:
    global cache_cities
    
    cache_cities.clear()

def get_prefectures(endpoint: str) -> dict:
    global cache_prefecture
    endpoint_url = f"{endpoint}.json"
    prefectures = cache_prefecture.get(endpoint_url)
    if prefectures is None:
        prefectures = json.loads(api_fetch(endpoint_url).text)
        cache_prefecture[endpoint_url] = prefectures
    return prefectures

def get_prefecture_regexes(prefecture_names: list, omit_mode: bool = False) -> list:
    prefecture_regex = "([都道府県])"
    for prefecture_name in prefecture_names:
        _prefecture_name = re.sub(f"{prefecture_regex}$", "", prefecture_name)
        reg = (
            re.compile(f"^{_prefecture_name}{prefecture_regex}")
            if not omit_mode
            else re.compile(f"^{_prefecture_name}{prefecture_regex}?")
        )
        yield prefecture_name, reg

def cities_list_to_tuple(lst) -> tuple:
    # citiesのリストについては、事前に長さでソートする必要があるためTupleに変換する前に実行する
    lst.sort(key=len)
    return tuple(lst)


def cache_cities_with_ttl() -> Callable:
    global cache_cities
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # リスト引数をタプルに変換してキャッシュする
            args_key = tuple(cities_list_to_tuple(arg) if isinstance(arg, list) else arg for arg in args)
            if args_key in cache_cities:
                result, timestamp = cache_cities[args_key]
                if time.time() - timestamp <= ttl:
                    return result
            result = func(*args, **kwargs)
            cache_cities[args_key] = (result, time.time())
            return result

        return wrapper

    return decorator

@cache_cities_with_ttl()
def get_city_regexes(pref: str, cities: list) -> tuple:
    results = []

    for city in cities:
        _city = to_regex(city)
        if re.match(".*?([町村])$", city) is not None:
            _city = re.sub("(.+?)郡", "(\\1郡)?", _city)
        results.append((city, re.compile(f"^{_city}")))

    return results

def get_towns(pref: str, city: str, endpoint: str) -> list:
    global cache_towns

    town_endpoint = "/".join(
        [
            endpoint,
            urllib.parse.quote(pref),
            urllib.parse.quote(city),
        ]
    )

    endpoint_url = f"{town_endpoint}.json"
    towns = cache_towns.get(endpoint_url)
    if towns is None:
        towns = list(json.loads((api_fetch(endpoint_url)).text))
        cache_towns[endpoint_url] = towns

    return towns

def get_town_regexes(pref: str, city: str, endpoint: str) -> list:
    def get_normalized_chome_regex(match_value: str) -> str:
        regexes = [re.sub("(丁目?|番([町丁])|条|軒|線|([のノ])町|地割)", "", match_value)]

        if re.match("^壱", match_value) is not None:
            regexes.append("一")
            regexes.append("1")
            regexes.append("１")
        else:
            num = match_value
            for match in re.finditer("([一二三四五六七八九十]+)", match_value):
                replace_num = str(kan2num(match.group()))
                num = num.replace(match.group(), replace_num)

            num = re.sub("(丁目?|番([町丁])|条|軒|線|([のノ])町|地割)", "", num)

            regexes.append(num)

        _regex = "|".join(regexes)
        _regex = f"({_regex})(([町丁])目?|番([町丁])|条|軒|線|の町?|地割|[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])"

        return _regex

    def towns_length(api_town: dict) -> int:
        # 大字で始まる場合、優先度を低く設定する。
        town_len = len(api_town["town"])
        town_len = town_len - 2 if str(api_town["town"]).startswith("大字") else town_len
        return town_len

    def is_kanji_number_follewed_by_cho(target_town_name: str) -> bool:
        x_cho = re.match(".町", target_town_name)
        if not x_cho:
            return False
        else:
            kanji_numbers = find_kanji_numbers(x_cho.group())
            return len(kanji_numbers) > 0

    api_pre_towns = get_towns(pref, city, endpoint)
    api_towns_set = [x["town"] for x in api_pre_towns]
    api_towns = []

    # 京都かどうかを判定
    is_kyoto = re.match("^京都市", city) is not None
    # 町丁目に「町」が含まれるケースへの対応
    # 通常は「○○町」のうち「町」の省略を許容し同義語として扱うが、まれに自治体内に「○○町」と「○○」が共存しているケースがある。
    # この場合は町の省略は許容せず、入力された住所は書き分けられているものとして正規化を行う。
    # 更に、「愛知県名古屋市瑞穂区十六町1丁目」漢数字を含むケースだと丁目や番地・号の正規化が不可能になる。このようなケースも除外。
    for town in api_pre_towns:
        api_towns.append(town)

        originalTown = town["town"]
        if str(originalTown).find("町") == -1:
            continue

        # 「愛知県名古屋市瑞穂区十六町1丁目」など漢数字を含むケースは、曖昧処理から除外
        if re.match("[壱一二三四五六七八九十百千万]+町", originalTown) is None:
            townAddr = re.sub(
                "(?!^町)町", "", originalTown
            )  # NOTE: 冒頭の「町」は明らかに省略するべきではないので、除外

        if (
            not is_kyoto
            and townAddr not in api_towns_set
            and f"大字{townAddr}" not in api_towns_set
            and not is_kanji_number_follewed_by_cho(  # 大字は省略されるため、大字〇〇と〇〇町がコンフリクトする。このケースを除外
                originalTown
            )
        ):
            # エイリアスとして町なしのパターンを登録
            dict_town = town.copy()
            dict_town["originalTown"] = town["town"]
            dict_town["town"] = townAddr
            api_towns.append(dict_town)

    # 少ない文字数の地名に対してミスマッチしないように文字の長さ順にソート
    towns = sorted(api_towns, key=lambda x: towns_length(x), reverse=True)

    town_regexes = []
    for town in towns:
        _town = town["town"]
        # 横棒を含む場合（流通センター、など）に対応
        _town = re.sub("[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]", "[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]", _town)
        _town = re.sub("大?字", "(大?字)?", _town)

        for replace_town in re.finditer(
            "([壱一二三四五六七八九十]+)(丁目?|番([町丁])|条|軒|線|([のノ])町|地割)", _town
        ):
            _town = re.sub(
                replace_town.group(),
                get_normalized_chome_regex(replace_town.group()),
                _town,
            )

        _town = to_regex(_town)

        return_town = {}
        if "originalTown" in town:
            return_town["originalTown"] = town["originalTown"]
        return_town["town"] = town["town"]
        town_regexes.append([return_town, _town, town["lat"], town["lng"]])

    # X丁目の丁目なしの数字だけ許容するため、最後に数字だけ追加していく
    for town in towns:  
        chome_match = re.search(r'([^一二三四五六七八九十]+)([一二三四五六七八九十]+)(丁目?)', town["town"])
        if chome_match is None:
            continue

        chome_name_part = chome_match.group(1)
        chome_number_kanji = chome_match.group(2)
        chome_number = kan2num(chome_number_kanji)
        chome_pattern = f"^{chome_name_part}({chome_number_kanji}|{chome_number})"
        return_town = {}
        if "originalTown" in town:
            return_town["originalTown"] = town["originalTown"]
        return_town["town"] = town["town"]
        town_regexes.append([return_town, chome_pattern, town["lat"], town["lng"]])
    
    return town_regexes


def replace_addr(addr: str) -> str:
    def replace_1(match_value: str) -> str:
        for num in list(re.finditer("([0-9]+)", match_value)):
            match_value = match_value.replace(
                num.group(), kanjize.number2kanji(int(num.group()))
            )
        return match_value

    addr = re.sub("^-", "", addr)

    patterns = [
        (re.compile("([0-9]+)(丁目)"), lambda m: replace_1(m.group())),
        (
            re.compile("(([0-9〇一二三四五六七八九十百千]+)(番地?)([0-9〇一二三四五六七八九十百千]+)号)\\s*(.+)"),
            lambda m: "{} {}".format(m.group(1), m.group(5)),
        ),
        (
            re.compile("([0-9〇一二三四五六七八九十百千]+)\\s*(番地?)\\s*([(0-9〇一二三四五六七八九十百千]+)\\s*号?"),
            lambda m: "{}-{}".format(m.group(1), m.group(3)),
        ),
        (re.compile("([0-9〇一二三四五六七八九十百千]+)番地?"), r"\1"),
        (re.compile("([0-9〇一二三四五六七八九十百千]+)の"), r"\1-"),
        (
            re.compile("([0-9〇一二三四五六七八九十百千]+)[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]"),
            lambda m: re.sub("[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]", "-", kan2num(m.group())),
        ),
        (
            re.compile("[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]([0-9〇一二三四五六七八九十百千]+)"),
            lambda m: re.sub("[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]", "-", kan2num(m.group())),
        ),
        (re.compile("([0-9〇一二三四五六七八九十百千]+)-"), lambda m: kan2num(m.group())),
        (re.compile("-([0-9〇一二三四五六七八九十百千]+)"), lambda m: kan2num(m.group())),
        (re.compile("-[^0-9]([0-9〇一二三四五六七八九十百千]+)"), lambda m: kan2num(m.group())),
        (re.compile("([0-9〇一二三四五六七八九十百千]+)$"), lambda m: kan2num(m.group())),
    ]

    for pattern, repl in patterns:
        addr = pattern.sub(repl, addr)

    return addr.strip()


def jis_kanji_regexes() -> Generator[Tuple[Pattern, str, str], None, None]:
    for old_kanji, new_kanji in zip(JIS_OLD_KANJI, JIS_NEW_KANJI):
        regex = re.compile(f"{old_kanji}|{new_kanji}")
        yield regex, old_kanji, new_kanji


def jis_kanji_to_both_forms(value: str) -> str:
    _value = value
    for reg, old_kanji, new_kanji in jis_kanji_regexes():
        pattern = re.compile(reg)
        _value = pattern.sub(f"({old_kanji}|{new_kanji})", _value)
    return _value


def to_regex(value: str) -> str:
    # 以下なるべく文字数が多いものほど上にすること
    patterns = [
        ("三栄町|四谷三栄町", "(三栄町|四谷三栄町)"),
        ("鬮野川|くじ野川|くじの川", "(鬮野川|くじ野川|くじの川)"),
        ("通り|とおり", "(通り|とおり)"),
        ("柿碕町|柿さき町", "(柿碕町|柿さき町)"),
        ("埠頭|ふ頭", "(埠頭|ふ頭)"),
        ("番町|番丁", "(番町|番丁)"),
        ("大冝|大宜", "(大冝|大宜)"),
        ("穝|さい", "(穝|さい)"),
        ("杁|えぶり", "(杁|えぶり)"),
        ("薭|稗|ひえ|ヒエ", "(薭|稗|ひえ|ヒエ)"),
        ("[之ノの]", "[之ノの]"),
        ("[ヶケが]", "[ヶケが]"),
        ("[ヵカか力]", "[ヵカか力]"),
        ("[ッツっつ]", "[ッツっつ]"),
        ("[ニ二]", "[ニ二]"),
        ("[ハ八]", "[ハ八]"),
        ("[塚塚]", "[塚塚]"),
        ("[釜竈]", "[釜竈]"),
        ("[條条]", "[條条]"),
        ("[狛拍]", "[狛拍]"),
        ("[藪薮]", "[藪薮]"),
        ("[渕淵]", "[渕淵]"),
        ("[エヱえ]", "[エヱえ]"),
        ("[曾曽]", "[曾曽]"),
        ("[舟船]", "[舟船]"),
        ("[莵菟]", "[莵菟]"),
        ("[市巿]", "[市巿]"),
    ]

    # コンパイル済み正規表現オブジェクトのリストを順番に適用
    for pattern in [(re.compile(p[0]), p[1]) for p in patterns]:
        value = pattern[0].sub("({})".format(pattern[0].pattern), value)

    value = jis_kanji_to_both_forms(value)

    return value


def normalize_town_name(
    addr: str, pref: str, city: str, endpoint: str
) -> Optional[Dict[str, str]]:
    # アドレスの前後の空白を削除する
    addr = addr.strip()
    
    # アドレスの先頭が"大字"で始まっていた場合は削除
    addr = re.sub("^大字", "", addr)

    # 町名の正規化
    regex_prefixes = ["^"]
    if re.match("^京都市", city):
        # 京都は通り名削除のために後方一致を使う
        regex_prefixes.append(".*")

    for regex_prefix in regex_prefixes:
        for town, pattern, lat, lng in get_town_regexes(pref, city, endpoint):
            if regex_prefix == "^":
                regex = re.compile(f"{regex_prefix}{pattern}")
                match = regex.match(addr)
                if match:
                    # 正規表現にマッチした場合、辞書型で町の名前、住所、緯度、経度を返す
                    return {
                        "town": town,
                        "addr": addr[len(match.group()) :],
                        "lat": lat,
                        "lng": lng,
                    }
            else:
                regex = re.compile(f"{regex_prefix}{pattern}")
                match = regex.match(addr)
                if match:
                    # 正規表現にマッチした場合、辞書型で町の名前、住所、緯度、経度を返す
                    return {
                        "town": town,
                        "addr": re.search(pattern, match.group()).group()
                        if len(addr) == len(match.group())
                        else addr[len(match.group()) :],
                        "lat": lat,
                        "lng": lng,
                    }
        
    # 正規表現にマッチしなかった場合は None を返す
    return None
