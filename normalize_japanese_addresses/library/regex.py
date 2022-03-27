import re
import json
import urllib.parse

import kanjize
from cachetools import cached, TTLCache

from .api import apiFetch
from .utils import kan2num

JIS_OLD_KANJI = '亞,圍,壹,榮,驛,應,櫻,假,會,懷,覺,樂,陷,歡,氣,戲,據,挾,區,徑,溪,輕,藝,儉,圈,權,嚴,恆,國,齋,雜,蠶,殘,兒,實,釋,從,縱,敍,燒,條,剩,壤,釀,眞,盡,醉,髓,聲,竊,' \
                '淺,錢,禪,爭,插,騷,屬,對,滯,擇,單,斷,癡,鑄,敕,鐵,傳,黨,鬪,屆,腦,廢,發,蠻,拂,邊,瓣,寶,沒,滿,藥,餘,樣,亂,兩,禮,靈,爐,灣,惡,醫,飮,營,圓,歐,奧,價,繪,擴,學,' \
                '罐,勸,觀,歸,犧,擧,狹,驅,莖,經,繼,缺,劍,檢,顯,廣,鑛,碎,劑,參,慘,絲,辭,舍,壽,澁,肅,將,證,乘,疊,孃,觸,寢,圖,穗,樞,齊,攝,戰,潛,雙,莊,裝,藏,續,體,臺,澤,膽,' \
                '彈,蟲,廳,鎭,點,燈,盜,獨,貳,霸,賣,髮,祕,佛,變,辯,豐,飜,默,與,譽,謠,覽,獵,勵,齡,勞,壓,爲,隱,衞,鹽,毆,穩,畫,壞,殼,嶽,卷,關,顏,僞,舊,峽,曉,勳,惠,螢,鷄,縣,' \
                '險,獻,驗,效,號,濟,册,棧,贊,齒,濕,寫,收,獸,處,稱,奬,淨,繩,讓,囑,愼,粹,隨,數,靜,專,踐,纖,壯,搜,總,臟,墮,帶,瀧,擔,團,遲,晝,聽,遞,轉,當,稻,讀,惱,拜,麥,拔,' \
                '濱,竝,辨,舖,襃,萬,譯,豫,搖,來,龍,壘,隸,戀,樓,鰺,鶯,蠣,攪,竈,灌,諫,頸,礦,蘂,靱,賤,壺,礪,檮,濤,邇,蠅,檜,儘,藪,籠'.split(',')

JIS_NEW_KANJI = '亜,囲,壱,栄,駅,応,桜,仮,会,懐,覚,楽,陥,歓,気,戯,拠,挟,区,径,渓,軽,芸,倹,圏,権,厳,恒,国,斎,雑,蚕,残,児,実,釈,従,縦,叙,焼,条,剰,壌,醸,真,尽,酔,髄,声,窃,' \
                '浅,銭,禅,争,挿,騒,属,対,滞,択,単,断,痴,鋳,勅,鉄,伝,党,闘,届,脳,廃,発,蛮,払,辺,弁,宝,没,満,薬,余,様,乱,両,礼,霊,炉,湾,悪,医,飲,営,円,欧,奥,価,絵,拡,学,' \
                '缶,勧,観,帰,犠,挙,狭,駆,茎,経,継,欠,剣,検,顕,広,鉱,砕,剤,参,惨,糸,辞,舎,寿,渋,粛,将,証,乗,畳,嬢,触,寝,図,穂,枢,斉,摂,戦,潜,双,荘,装,蔵,続,体,台,沢,胆,' \
                '弾,虫,庁,鎮,点,灯,盗,独,弐,覇,売,髪,秘,仏,変,弁,豊,翻,黙,与,誉,謡,覧,猟,励,齢,労,圧,為,隠,衛,塩,殴,穏,画,壊,殻,岳,巻,関,顔,偽,旧,峡,暁,勲,恵,蛍,鶏,県,' \
                '険,献,験,効,号,済,冊,桟,賛,歯,湿,写,収,獣,処,称,奨,浄,縄,譲,嘱,慎,粋,随,数,静,専,践,繊,壮,捜,総,臓,堕,帯,滝,担,団,遅,昼,聴,逓,転,当,稲,読,悩,拝,麦,抜,' \
                '浜,並,弁,舗,褒,万,訳,予,揺,来,竜,塁,隷,恋,楼,鯵,鴬,蛎,撹,竃,潅,諌,頚,砿,蕊,靭,賎,壷,砺,梼,涛,迩,蝿,桧,侭,薮,篭 '.split(',')

cache_prefecture = {}
cache_towns = {}


@cached(cache=TTLCache(maxsize=300, ttl=60 * 60 * 24 * 7))
def getPrefectures(endpoint):
    global cache_prefecture
    endpoint_url = f'{endpoint}.json'
    if endpoint_url not in cache_prefecture:
        cache_prefecture[endpoint_url] = apiFetch(f'{endpoint}.json')

    return cache_prefecture[endpoint_url]


def getPrefectureRegexes(prefs: list, omit_mode: bool = False):
    pref_regex = '([都道府県])'
    for pref in prefs:
        _pref = re.sub(f'{pref_regex}$', '', pref)
        reg = re.compile(f'^{_pref}{pref_regex}') if not omit_mode else re.compile(f'^{_pref}{pref_regex}?')
        yield pref, reg


def getCityRegexes(pref: str, cities: list):
    cities.sort(key=len)

    for city in cities:
        _city = toRegex(city)
        if re.match('.*?([町村])$', city) is not None:
            _city = re.sub('(.+?)郡', '(\\1郡)?', _city)
        yield city, re.compile(f'^{_city}')


@cached(cache=TTLCache(maxsize=300, ttl=60 * 60 * 24 * 7))
def getTowns(pref: str, city: str, endpoint: str):
    global cache_towns

    town_endpoint = '/'.join([
        endpoint,
        urllib.parse.quote(pref),
        urllib.parse.quote(city),
    ])

    endpoint_url = f'{town_endpoint}.json'
    if endpoint_url not in cache_towns:
        cache_towns[endpoint_url] = list(json.loads((apiFetch(endpoint_url)).text))

    return cache_towns[endpoint_url]


def getTownRegexes(pref: str, city: str, endpoint):
    def getChomeRegex(match_value: str):
        regexes = [re.sub('(丁目?|番([町丁])|条|軒|線|([のノ])町|地割)', '', match_value)]

        if re.match('^壱', match_value) is not None:
            regexes.append('一')
            regexes.append('1')
            regexes.append('１')
        else:
            num = match_value
            for match in re.finditer('([一二三四五六七八九十]+)', match_value):
                replace_num = str(kanjize.kanji2int(match.group()))
                num = num.replace(match.group(), replace_num)

            num = re.sub('(丁目?|番([町丁])|条|軒|線|([のノ])町|地割)', '', num)

            regexes.append(num)

        _regex = '|'.join(regexes)
        _regex = f'({_regex})(([町丁])目?|番([町丁])|条|軒|線|の町?|地割|[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━])'

        return _regex

    api_towns = getTowns(pref, city, endpoint)
    # 少ない文字数の地名に対してミスマッチしないように文字の長さ順にソート
    towns = sorted(api_towns, key=lambda x: len([i for i in x.get("town")]), reverse=True)

    town_regexes = []
    for town in towns:
        _town = town["town"]
        # 横棒を含む場合（流通センター、など）に対応
        _town = re.sub('[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]', '[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]', _town)
        _town = re.sub('大?字', '(大?字)?', _town)

        for replace_town in re.finditer('([壱一二三四五六七八九十]+)(丁目?|番([町丁])|条|軒|線|([のノ])町|地割)', _town):
            _town = re.sub(replace_town.group(), getChomeRegex(replace_town.group()), _town)

        _town = toRegex(_town)

        if re.match('^京都市', city) is not None:
            # town_regexes.append([town["town"], re.compile(f'.*{_town}')])
            town_regexes.append([town["town"], re.compile(f'.*{_town}'), town["lat"], town["lng"]])
        else:
            town_regexes.append([town["town"], re.compile(f'^{_town}'), town["lat"], town["lng"]])

    return town_regexes


def replace_addr(addr: str):
    def replace_1(match_value: str):
        for num in list(re.finditer('([0-9]+)', match_value)):
            match_value = match_value.replace(num.group(), kanjize.int2kanji(int(num.group())))
        return match_value

    addr = re.sub('^-', '', addr)

    for _find_addr in re.finditer('([0-9]+)(丁目)', addr):
        _rp = replace_1(_find_addr.group())
        addr = addr.replace(_find_addr.group(), _rp)

    addr = re.sub('(([0-9〇一二三四五六七八九十百千]+)(番地?)([0-9〇一二三四五六七八九十百千]+)号)\\s*(.+)', '\\1 \\5', addr)

    addr = re.sub('([0-9〇一二三四五六七八九十百千]+)(番地?)([(0-9〇一二三四五六七八九十百千]+)号?', '\\1-\\3', addr)

    addr = re.sub('([0-9〇一二三四五六七八九十百千]+)番地?', '\\1', addr)

    addr = re.sub('([0-9〇一二三四五六七八九十百千]+)の', '\\1-', addr)

    for _find_addr in re.finditer('([0-9〇一二三四五六七八九十百千]+)[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]', addr):
        _rp = re.sub('[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]', '-', kan2num(_find_addr.group()))
        addr = addr.replace(_find_addr.group(), _rp)

    for _find_addr in re.finditer('[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]([0-9〇一二三四五六七八九十百千]+)', addr):
        _rp = re.sub('[-－﹣−‐⁃‑‒–—﹘―⎯⏤ーｰ─━]', '-', kan2num(_find_addr.group()))
        addr = addr.replace(_find_addr.group(), _rp)

    for _find_addr in re.finditer('([0-9〇一二三四五六七八九十百千]+)-', addr):
        addr = addr.replace(_find_addr.group(), kan2num(_find_addr.group()))

    for _find_addr in re.finditer('-([0-9〇一二三四五六七八九十百千]+)', addr):
        addr = addr.replace(_find_addr.group(), kan2num(_find_addr.group()))

    for _find_addr in re.finditer('-[^0-9]+([0-9〇一二三四五六七八九十百千]+)', addr):
        addr = addr.replace(_find_addr.group(), kan2num(_find_addr.group()))

    for _find_addr in re.finditer('([0-9〇一二三四五六七八九十百千]+)$', addr):
        addr = addr.replace(_find_addr.group(), kan2num(_find_addr.group()))

    addr = addr.strip()

    return addr


def jis_kanji_regexes():
    dict_jis_kanji = dict(zip(JIS_OLD_KANJI, JIS_NEW_KANJI))
    for old_kanji, new_kanji in dict_jis_kanji.items():
        yield re.compile(f'{old_kanji}|{new_kanji}'), old_kanji, new_kanji


def jisKanji(value: str):
    _value = value
    for reg, old_kanji, new_kanji in jis_kanji_regexes():
        _value = re.sub(reg, f'({old_kanji}|{new_kanji})', _value)
    return _value


def toRegex(value: str):
    _value = value
    # 以下なるべく文字数が多いものほど上にすること

    _value = re.sub('三栄町|四谷三栄町', '(三栄町|四谷三栄町)', _value)
    _value = re.sub('鬮野川|くじ野川|くじの川', '(鬮野川|くじ野川|くじの川)', _value)
    _value = re.sub('通り|とおり', '(通り|とおり)', _value)
    _value = re.sub('埠頭|ふ頭', '(埠頭|ふ頭)', _value)
    _value = re.sub('番町|番丁', '(番町|番丁)', _value)
    _value = re.sub('大冝|大宜', '(大冝|大宜)', _value)
    _value = re.sub('穝|さい', '(穝|さい)', _value)
    _value = re.sub('杁|えぶり', '(杁|えぶり)', _value)
    _value = re.sub('薭|稗|ひえ|ヒエ', '(薭|稗|ひえ|ヒエ)', _value)
    _value = re.sub('[之ノの]', '[之ノの]', _value)
    _value = re.sub('[ヶケが]', '[ヶケが]', _value)
    _value = re.sub('[ヵカか力]', '[ヵカか力]', _value)
    _value = re.sub('[ッツっつ]', '[ッツっつ]', _value)
    _value = re.sub('[ニ二]', '[ニ二]', _value)
    _value = re.sub('[ハ八]', '[ハ八]', _value)
    _value = re.sub('[塚塚]', '[塚塚]', _value)
    _value = re.sub('[釜竈]', '[釜竈]', _value)
    _value = re.sub('[條条]', '[條条]', _value)
    _value = re.sub('[狛拍]', '[狛拍]', _value)
    _value = re.sub('[藪薮]', '[藪薮]', _value)
    _value = re.sub('[渕淵]', '[渕淵]', _value)
    _value = re.sub('[エヱえ]', '[エヱえ]', _value)
    _value = re.sub('[曾曽]', '[曾曽]', _value)
    _value = re.sub('[舟船]', '[舟船]', _value)
    _value = re.sub('[莵菟]', '[莵菟]', _value)
    _value = re.sub('[市巿]', '[市巿]', _value)

    _value = jisKanji(_value)

    return _value


def normalizeTownName(addr: str, pref: str, city: str, endpoint: str):
    addr = addr.strip()
    addr = re.sub('^大字', '', addr)
    town_regexes = getTownRegexes(pref, city, endpoint)

    for town_regex in town_regexes:
        _town, reg, lat, lng = town_regex[0], town_regex[1], town_regex[2], town_regex[3]
        match = re.match(reg, addr)

        if not match:
            continue
        return {'town': _town, 'addr': addr[len(match.group()):], 'lat': lat, 'lng': lng}

    return None
