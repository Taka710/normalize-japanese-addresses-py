import re

from kanjize import kanji2number

from .japaneseNumerics import (
    JAPANESE_NUMERICS,
    OLD_JAPANESE_NUMERICS,
    KANJI_DIGIT_CHARACTERS,
    LARGE_NUMBERS
)


def normalize(japanese: str) -> str:
    for key, value in OLD_JAPANESE_NUMERICS.items():
        japanese = re.sub(key, value, japanese)

    return japanese


def split_large_number(japanese: str) -> dict:
    def kanjize_error_kanji_to_int(kanji_num_str: str) -> int:
        """
        kanjizeが変換できない漢字を数値に変換する
        """

        # 一番最初の漢字が数字でない場合は、先頭に「一」を追加する
        if kanji_num_str[0] not in JAPANESE_NUMERICS:
            kanji_num_str = "一" + kanji_num_str

        #  漢字の数字から数詞を取り除く
        for kanji in KANJI_DIGIT_CHARACTERS:
            kanji_num_str = kanji_num_str.replace(kanji, "")

        # 漢字の位置で桁を判定し、数値に変換する
        result = 0
        for i, kanji in enumerate(kanji_num_str):
            result += int(JAPANESE_NUMERICS[kanji]) * (
                10 ** (len(kanji_num_str) - i - 1)
            )

        return result

    kanji = japanese
    numbers = {}
    for key, value in LARGE_NUMBERS.items():
        match = re.match(f"(.+){key}", kanji)
        if match is not None:
            numbers[key] = kanji2number(match.group())
            kanji = kanji.replace(match.group(), "")
        else:
            numbers[key] = 0

    if len(kanji) > 0:
        try:
            numbers["千"] = kanji2number(kanji)
        except:
            numbers["千"] = kanjize_error_kanji_to_int(kanji)
    else:
        numbers["千"] = 0

    return numbers


def kan2num(value: str) -> str:
    def _kanji_to_integer(kanji_number: str) -> int:
        kanji_number = normalize(kanji_number)

        if (
            re.match("〇", kanji_number) is not None
            or re.match("^[〇一二三四五六七八九]+$", kanji_number) is not None
        ):
            for key, value in JAPANESE_NUMERICS.items():
                kanji_number = kanji_number.replace(key, value)

            return int(kanji_number)
        else:
            number = 0
            numbers = split_large_number(kanji_number)

            for key, value in LARGE_NUMBERS.items():
                if key in numbers:
                    n = numbers[key]
                    number = number + n

            if not str(number).isdigit() or not str(numbers["千"]).isdigit():
                raise TypeError(
                    "The attribute of _kanji_to_integer() must be a Japanese numeral as integer."
                )

            return number + numbers["千"]
    
    # エラーが発生した場合、そのままの文字列を返す
    try:
        for fromValue in find_kanji_numbers(value):
            value = value.replace(fromValue, str(_kanji_to_integer(fromValue)))
    except Exception as e:
        pass

    return value


def find_kanji_numbers(text: str) -> list:
    def isItemLength(item: str) -> bool:
        if item is None:
            return False

        if re.match("^[0-9０-９]+$", item) is None and (
            len(item) > 0
            and "兆" != item
            and "億" != item
            and "万" != item
            and "萬" != item
        ):
            return True
        else:
            return False

    num = "([0-9０-９]*)|([〇一二三四五六七八九壱壹弐弍貳貮参參肆伍陸漆捌玖]*)"
    base_pattern = f"(({num})(千|阡|仟))?(({num})(百|陌|佰))?(({num})(十|拾))?({num})?"
    pattern = (
        f"(({base_pattern}兆)?({base_pattern}億)?({base_pattern}(万|萬))?{base_pattern})"
    )
    regex = re.compile(pattern)

    match = regex.finditer(text)

    match_kanji = ""
    return_kanji = []
    if match is not None:
        for m in match:
            if isItemLength(m.group()):
                match_kanji += m.group()

        if len(match_kanji) > 0:
            return_kanji.append(match_kanji)
    return return_kanji


def zenkaku_to_hankaku(value: str) -> str:
    return (
        value.translate(
            str.maketrans({chr(0xFF10 + i): chr(0x30 + i) for i in range(10)})
        )
        .translate(str.maketrans({chr(0xFF21 + i): chr(0x41 + i) for i in range(26)}))
        .translate(str.maketrans({chr(0xFF41 + i): chr(0x61 + i) for i in range(26)}))
    )
