from normalize_japanese_addresses.library.utils import kan2num, find_kanji_numbers


def test_kan2num_0001():
    assert kan2num('千二百三十四') == "1234"


def test_kan2num_0002():
    assert kan2num('五百三十七の1') == "537の1"


def test_kan2num_0003():
    assert kan2num('五百三十七-1') == "537-1"


def test_kan2num_0004():
    assert kan2num('一千百十一兆一千百十一億一千百十一万一千百十一') == "1111111111111111"


def test_kan2num_0005():
    assert kan2num('一千百十一兆一千百十一億一千百十一万') == "1111111111110000"


def test_kan2num_0006():
    assert kan2num('一千百十一兆一千百十一億一千百十一') == "1111111100001111"


def test_kan2num_0007():
    assert kan2num('百十一') == "111"


def test_kan2num_0008():
    assert kan2num('三億八') == "300000008"


def test_kan2num_0009():
    assert kan2num('三百八') == "308"


def test_kan2num_0010():
    assert kan2num('三〇八') == "308"


def test_kan2num_0011():
    assert kan2num('二〇二〇') == "2020"


def test_kan2num_0012():
    assert kan2num('二千') == "2000"


def test_kan2num_0013():
    assert kan2num('壱万') == "10000"


def test_kan2num_0014():
    assert kan2num('弍万') == "20000"


def test_kan2num_0015():
    assert kan2num('一二三四') == "1234"


def test_kan2num_0016():
    assert kan2num('千二三四') == "1234"


def test_kan2num_0017():
    assert kan2num('千二百三四') == "1234"


def test_kan2num_0018():
    assert kan2num('千二百三十四') == "1234"


def test_kan2num_0019():
    assert kan2num('壱阡陌拾壱兆壱阡陌拾壱億壱阡陌拾壱萬壱阡陌拾壱') == "1111111111111111"


def test_kan2num_0020():
    assert kan2num('壱仟佰拾壱兆壱仟佰拾壱億壱仟佰拾壱萬壱仟佰拾壱') == "1111111111111111"


def test_find_kanji_numbers_0001():
    assert find_kanji_numbers('千二百三十四') == ['千二百三十四']


def test_find_kanji_numbers_0002():
    assert find_kanji_numbers('五百三十七の1') == ['五百三十七']
