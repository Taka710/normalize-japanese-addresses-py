from normalize_japanese_addresses.library.utils import kan2num, find_kanji_numbers


def test_kan2num_0001():
    assert kan2num('千二百三十四') == "1234"


def test_kan2num_0002():
    assert kan2num('五百三十七の1') == "537の1"


def test_kan2num_0003():
    assert kan2num('五百三十七-1') == "537-1"


def test_find_kanji_numbers_0001():
    assert find_kanji_numbers('千二百三十四') == ['千二百三十四']


def test_find_kanji_numbers_0002():
    assert find_kanji_numbers('五百三十七の1') == ['五百三十七']
