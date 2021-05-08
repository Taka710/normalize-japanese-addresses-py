import re

from kanjize import kanji2int, int2kanji

from .japaneseNumerics import japaneseNumerics, oldJapaneseNumerics

largeNumbers = {'兆': 1000000000000, '億': 100000000, '万': 10000}
smallNumbers = {'千': 1000, '百': 100, '十': 10}


def normalize(japanese: str):
    for key, value in oldJapaneseNumerics.items():
        japanese = re.sub(key, value, japanese)

    return japanese


def splitLargeNumber(japanese: str):
    kanji = japanese
    numbers = {}
    for key, value in largeNumbers.items():
        match = re.match(f'(.+){key}', kanji)
        if match is not None:
            numbers[key] = kanji2int(match.group())
            kanji = kanji.replace(match.group(), '')
        else:
            numbers[key] = 0

    if len(kanji) > 0:
        numbers['千'] = kanji2int(kanji)
    else:
        numbers['千'] = 0

    return numbers


def kan2num(value: str):
    for fromValue in findKanjiNumbers(value):
        value = value.replace(fromValue, str(kanji2number(fromValue)))

    return value


def kanji2number(japanese: str):
    japanese = normalize(japanese)

    if re.match('〇', japanese) is not None or re.match('^[〇一二三四五六七八九]+$', japanese) is not None:
        for key, value in japaneseNumerics.items():
            japanese = japanese.replace(key, value)

        return int(japanese)
    else:
        number = 0
        numbers = splitLargeNumber(japanese)

        for key, value in largeNumbers.items():
            if key in numbers:
                n = value * numbers[key]
                number = number + n

        if not str(number).isdigit() or not str(numbers['千']).isdigit():
            raise TypeError('The attribute of kanji2number() must be a Japanese numeral as integer.')

        return number + numbers['千']


def findKanjiNumbers(text: str):
    def isItemLength(item: str):
        if item is None:
            return False

        if len(item) > 0 and '兆' != item and '億' != item and '万' != item and '萬' != item:
            return True
        else:
            return False

    basePattern = '([0-9０-９一二三四五六七八九壱壹弐貳貮参參肆伍陸漆捌玖]*(千|阡|仟))?([0-9０-９一二三四五六七八九壱壹弐貳貮参參肆伍陸漆捌玖]*(百|陌|佰))?([' \
                  '0-9０-９一二三四五六七八九壱壹弐貳貮参參肆伍陸漆捌玖]*(十|拾))?([0-9０-９〇一二三四五六七八九壱壹弐貳貮参參肆伍陸漆捌玖]+)?'

    pattern = f'({basePattern}兆)?({basePattern}億)?({basePattern}(万 | 萬))?{basePattern}'

    regex = re.compile(pattern)

    match = regex.finditer(text)
    if match is not None:
        return_match = []
        for m in match:
            if isItemLength(m.group()):
                return_match.append(m.group())
        return return_match
    else:
        return []


def zen2han(value: str):
    return value\
        .translate(str.maketrans({chr(0xFF10 + i): chr(0x30 + i) for i in range(10)}))\
        .translate(str.maketrans({chr(0xFF21 + i): chr(0x41 + i) for i in range(26)}))\
        .translate(str.maketrans({chr(0xFF41 + i): chr(0x61 + i) for i in range(26)}))
