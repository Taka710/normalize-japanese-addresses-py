import re

addrPatches = [
    {
        'pref': '香川県',
        'city': '仲多度郡まんのう町',
        'town': '勝浦',
        'pattern': re.compile('^字?家6'),
        'result': '家六',
    },
    {
        'pref': '愛知県',
        'city': 'あま市',
        'town': '西今宿',
        'pattern': re.compile('^字?梶村1'),
        'result': '梶村一',
    },
    {
        'pref': '香川県',
        'city': '丸亀市',
        'town': '原田町',
        'pattern': re.compile('^字?東三分1'),
        'result': '東三分一',
    },
]


def patchAddr(
        pref: str,
        city: str,
        town: str,
        addr: str
):
    _addr = addr
    for patch in addrPatches:
        if patch['pref'] == pref and patch['city'] == city and patch['town'] == town:
            _addr = re.sub(patch['pattern'], patch['result'], _addr)

    return _addr
