from normalize_japanese_addresses.library.utils import kan2num, findKanjiNumbers


def test_kan2num_0001():
    assert kan2num('千二百三十四') == "1234"


def test_kan2num_0002():
    assert kan2num('五百三十七の1') == "537の1"


def test_kan2num_0003():
    assert kan2num('五百三十七-1') == "537-1"


def test_findKanjiNumbers_0001():
    assert findKanjiNumbers('千二百三十四') == ['千二百三十四']


def test_findKanjiNumbers_0002():
    assert findKanjiNumbers('五百三十七の1') == ['五百三十七']
