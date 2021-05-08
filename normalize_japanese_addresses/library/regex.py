import re
import json
import urllib.parse

import kanjize

from .dictionary import toRegex
from .api import apiFetch
from .utils import kan2num


def getPrefectureRegexes(prefs: list):
    pref_regex = '([都道府県])'
    for pref in prefs:
        _pref = re.sub(f'{pref_regex}$', '', pref)
        reg = re.compile(f'^{_pref}{pref_regex}')
        yield pref, reg


def getCityRegexes(pref: str, cities: list):
    cities.sort(key=len)

    for city in cities:
        _city = toRegex(city)
        if re.match('.*?([町村])$', city) is not None:
            _city = re.sub('(.+?)郡', '(\\1郡)?', city)
        yield city, re.compile(f'^{_city}')


def getTownRegexes(pref: str, city: str):
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

    _pref = urllib.parse.quote(pref)
    _city = urllib.parse.quote(city)
    towns: list = list(json.loads(apiFetch(f'/{_pref}/{_city}').text))

    towns.sort(key=len, reverse=True)

    town_regexes = []
    for town in towns:
        _town = town
        _town = re.sub('大?字', '(大?字)?', _town)

        for replace_town in re.finditer('([壱一二三四五六七八九十]+)(丁目?|番([町丁])|条|軒|線|([のノ])町|地割)', _town):
            _town = re.sub(replace_town.group(), getChomeRegex(replace_town.group()), _town)

        _town = toRegex(_town)

        if re.match('^京都市', city) is not None:
            town_regexes.append([re.sub('^大字', '', town), re.compile(f'.*{_town}')])
        else:
            town_regexes.append([re.sub('^大字', '', town), re.compile(f'^{_town}')])

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

    addr = re.sub('([0-9〇一二三四五六七八九十百千]+)(番|番地)([(0-9〇一二三四五六七八九十百千]+)号?', '\\1-\\3', addr)

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
