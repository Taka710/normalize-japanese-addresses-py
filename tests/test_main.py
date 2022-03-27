from normalize_japanese_addresses import normalize


def test_normalize_0001():
    assert normalize('大阪府堺市北区新金岡町4丁1−8') == \
           {"pref": "大阪府", "city": "堺市北区", "town": "新金岡町四丁", "addr": "1-8",
            "lat": 34.568184, "lng": 135.519409, "level": 3}


def test_normalize_0002():
    assert normalize('大阪府堺市北区新金岡町４丁１ー８') == \
           {"pref": "大阪府", "city": "堺市北区", "town": "新金岡町四丁", "addr": "1-8",
            "lat": 34.568184, "lng": 135.519409, "level": 3}


def test_normalize_0003():
    assert normalize('和歌山県串本町串本1234') == \
           {"pref": "和歌山県", "city": "東牟婁郡串本町", "town": "串本", "addr": "1234",
            "lat": 33.470358, "lng": 135.779952, "level": 3}


def test_normalize_0004():
    assert normalize('和歌山県東牟婁郡串本町串本1234') == \
           {"pref": "和歌山県", "city": "東牟婁郡串本町", "town": "串本", "addr": "1234",
            "lat": 33.470358, "lng": 135.779952, "level": 3}


def test_normalize_0005():
    assert normalize('和歌山県東牟婁郡串本町串本千二百三十四') == \
           {"pref": "和歌山県", "city": "東牟婁郡串本町", "town": "串本", "addr": "1234",
            "lat": 33.470358, "lng": 135.779952, "level": 3}


def test_normalize_0006():
    assert normalize('和歌山県東牟婁郡串本町串本一千二百三十四') == \
           {"pref": "和歌山県", "city": "東牟婁郡串本町", "town": "串本", "addr": "1234",
            "lat": 33.470358, "lng": 135.779952, "level": 3}


def test_normalize_0007():
    assert normalize('和歌山県東牟婁郡串本町串本一二三四') == \
           {"pref": "和歌山県", "city": "東牟婁郡串本町", "town": "串本", "addr": "1234",
            "lat": 33.470358, "lng": 135.779952, "level": 3}


def test_normalize_0008():
    assert normalize('和歌山県東牟婁郡串本町くじ野川一二三四') == \
           {"pref": "和歌山県", "city": "東牟婁郡串本町", "town": "鬮野川", "addr": "1234",
            "lat": 33.493026, "lng": 135.784941, "level": 3}


def test_normalize_0009():
    assert normalize('京都府京都市中京区寺町通御池上る上本能寺前町488番地') == \
           {"pref": "京都府", "city": "京都市中京区", "town": "上本能寺前町", "addr": "488",
            "lat": 35.011582, "lng": 135.767914, "level": 3}


def test_normalize_0010():
    assert normalize('京都府京都市中京区上本能寺前町488') == \
           {"pref": "京都府", "city": "京都市中京区", "town": "上本能寺前町", "addr": "488",
            "lat": 35.011582, "lng": 135.767914, "level": 3}


def test_normalize_0011():
    assert normalize('大阪府大阪市中央区大手前２-１') == \
           {"pref": "大阪府", "city": "大阪市中央区", "town": "大手前二丁目", "addr": "1",
            "lat": 34.687006, "lng": 135.519317, "level": 3}


def test_normalize_0012():
    assert normalize('北海道札幌市西区24-2-2-3-3') == \
           {"pref": "北海道", "city": "札幌市西区", "town": "二十四軒二条二丁目", "addr": "3-3",
            "lat": 43.074273, "lng": 141.315099, "level": 3}


def test_normalize_0013():
    assert normalize('京都府京都市東山区大和大路2-537-1') == \
           {"pref": "京都府", "city": "京都市東山区", "town": "大和大路二丁目", "addr": "537-1",
            "lat": 34.989944, "lng": 135.770967, "level": 3}


def test_normalize_0014():
    assert normalize('京都府京都市東山区大和大路2丁目五百三十七の1') == \
           {"pref": "京都府", "city": "京都市東山区", "town": "大和大路二丁目", "addr": "537-1",
            "lat": 34.989944, "lng": 135.770967, "level": 3}


def test_normalize_0015():
    assert normalize('愛知県蒲郡市旭町17番1号') == \
           {"pref": "愛知県", "city": "蒲郡市", "town": "旭町", "addr": "17-1",
            "lat": 34.825785, "lng": 137.218621, "level": 3}


def test_normalize_0016():
    assert normalize('北海道岩見沢市栗沢町万字寿町１−２') == \
           {"pref": "北海道", "city": "岩見沢市", "town": "栗沢町万字寿町", "addr": "1-2",
            "lat": 43.135248, "lng": 141.986658, "level": 3}


def test_normalize_0017():
    assert normalize('北海道久遠郡せたな町北檜山区北檜山１９３') == \
           {"pref": "北海道", "city": "久遠郡せたな町", "town": "北檜山区北檜山", "addr": "193",
            "lat": 42.414, "lng": 139.881784, "level": 3}


def test_normalize_0018():
    assert normalize('北海道久遠郡せたな町北桧山区北桧山１９３') == \
           {"pref": "北海道", "city": "久遠郡せたな町", "town": "北檜山区北檜山", "addr": "193",
            "lat": 42.414, "lng": 139.881784, "level": 3}


def test_normalize_0019():
    assert normalize('京都府京都市中京区錦小路通大宮東入七軒町466') == \
           {"pref": "京都府", "city": "京都市中京区", "town": "七軒町", "addr": "466",
            "lat": 35.004829, "lng": 135.749797, "level": 3}


def test_normalize_0020():
    assert normalize('栃木県佐野市七軒町2201') == \
           {"pref": "栃木県", "city": "佐野市", "town": "七軒町", "addr": "2201",
            "lat": 36.305969, "lng": 139.57389, "level": 3}


def test_normalize_0021():
    assert normalize('京都府京都市東山区大和大路通三条下る東入若松町393') == \
           {"pref": "京都府", "city": "京都市東山区", "town": "若松町", "addr": "393",
            "lat": 35.007967, "lng": 135.774082, "level": 3}


def test_normalize_0022():
    assert normalize('長野県長野市長野東之門町2462') == \
           {"pref": "長野県", "city": "長野市", "town": "大字長野", "addr": "東之門町2462",
            "lat": 36.674892, "lng": 138.178449, "level": 3}


def test_normalize_0023():
    assert normalize('岩手県下閉伊郡普代村第１地割上村４３−２５') == \
           {"pref": "岩手県", "city": "下閉伊郡普代村", "town": "第一地割字上村", "addr": "43-25",
            "lat": 39.990149, "lng": 141.928282, "level": 3}


def test_normalize_0024():
    assert normalize('岩手県花巻市下北万丁目１７４−１') == \
           {"pref": "岩手県", "city": "花巻市", "town": "下北万丁目", "addr": "174-1",
            "lat": 39.394178, "lng": 141.099889, "level": 3}


def test_normalize_0025():
    assert normalize('岩手県花巻市十二丁目１１９２') == \
           {"pref": "岩手県", "city": "花巻市", "town": "十二丁目", "addr": "1192",
            "lat": 39.358268, "lng": 141.122331, "level": 3}


def test_normalize_0026():
    assert normalize('岩手県滝沢市後２６８−５６６') == \
           {"pref": "岩手県", "city": "滝沢市", "town": "後", "addr": "268-566",
            "lat": 39.839043, "lng": 141.094179, "level": 3}


def test_normalize_0027():
    assert normalize('青森県五所川原市金木町喜良市千苅６２−８') == \
           {"pref": "青森県", "city": "五所川原市", "town": "金木町喜良市", "addr": "千苅62-8",
            "lat": 40.904317, "lng": 140.486676, "level": 3}


def test_normalize_0028():
    assert normalize('岩手県盛岡市盛岡駅西通２丁目９番地１号') == \
           {"pref": "岩手県", "city": "盛岡市", "town": "盛岡駅西通二丁目", "addr": "9-1",
            "lat": 39.698721, "lng": 141.135252, "level": 3}


def test_normalize_0029():
    assert normalize('岩手県盛岡市盛岡駅西通２丁目９の１') == \
           {"pref": "岩手県", "city": "盛岡市", "town": "盛岡駅西通二丁目", "addr": "9-1",
            "lat": 39.698721, "lng": 141.135252, "level": 3}


def test_normalize_0030():
    assert normalize('岩手県盛岡市盛岡駅西通２の９の１') == \
           {"pref": "岩手県", "city": "盛岡市", "town": "盛岡駅西通二丁目", "addr": "9-1",
            "lat": 39.698721, "lng": 141.135252, "level": 3}


def test_normalize_0031():
    assert normalize('岩手県盛岡市盛岡駅西通２丁目９番地１号 マリオス10F') == \
           {"pref": "岩手県", "city": "盛岡市", "town": "盛岡駅西通二丁目", "addr": "9-1 マリオス10F",
            "lat": 39.698721, "lng": 141.135252, "level": 3}


def test_normalize_0032():
    assert normalize('東京都文京区千石4丁目15-7') == \
           {"pref": "東京都", "city": "文京区", "town": "千石四丁目", "addr": "15-7",
            "lat": 35.729052, "lng": 139.740683, "level": 3}


def test_normalize_0033():
    assert normalize('東京都文京区千石四丁目15-7') == \
           {"pref": "東京都", "city": "文京区", "town": "千石四丁目", "addr": "15-7",
            "lat": 35.729052, "lng": 139.740683, "level": 3}


def test_normalize_0034():
    assert normalize('東京都文京区千石4丁目15－7') == \
           {"pref": "東京都", "city": "文京区", "town": "千石四丁目", "addr": "15-7",
            "lat": 35.729052, "lng": 139.740683, "level": 3}


def test_normalize_0035():
    assert normalize('東京都文京区千石4丁目15－7') == \
           {"pref": "東京都", "city": "文京区", "town": "千石四丁目", "addr": "15-7",
            "lat": 35.729052, "lng": 139.740683, "level": 3}


def test_normalize_0036():
    assert normalize('東京都文京区 千石4丁目15－7') == \
           {"pref": "東京都", "city": "文京区", "town": "千石四丁目", "addr": "15-7",
            "lat": 35.729052, "lng": 139.740683, "level": 3}


def test_normalize_0037():
    assert normalize('東京都文京区千石4-15-7 ') == \
           {"pref": "東京都", "city": "文京区", "town": "千石四丁目", "addr": "15-7",
            "lat": 35.729052, "lng": 139.740683, "level": 3}


def test_normalize_0038():
    assert normalize('和歌山県東牟婁郡串本町串本 833') == \
           {"pref": "和歌山県", "city": "東牟婁郡串本町", "town": "串本", "addr": "833",
            "lat": 33.470358, "lng": 135.779952, "level": 3}


def test_normalize_0039():
    assert normalize('和歌山県東牟婁郡串本町串本　833') == \
           {"pref": "和歌山県", "city": "東牟婁郡串本町", "town": "串本", "addr": "833",
            "lat": 33.470358, "lng": 135.779952, "level": 3}


def test_normalize_0040():
    assert normalize('東京都世田谷区上北沢４の９の２') == \
           {"pref": "東京都", "city": "世田谷区", "town": "上北沢四丁目", "addr": "9-2",
            "lat": 35.669726, "lng": 139.620901, "level": 3}


def test_normalize_0041():
    assert normalize('東京都品川区東五反田２丁目５－１１') == \
           {"pref": "東京都", "city": "品川区", "town": "東五反田二丁目", "addr": "5-11",
            "lat": 35.624169, "lng": 139.72819, "level": 3}


def test_normalize_0042():
    assert normalize('東京都世田谷区上北沢四丁目2-1') == \
           {"pref": "東京都", "city": "世田谷区", "town": "上北沢四丁目", "addr": "2-1",
            "lat": 35.669726, "lng": 139.620901, "level": 3}


def test_normalize_0043():
    assert normalize('東京都世田谷区上北沢4-2-1') == \
           {"pref": "東京都", "city": "世田谷区", "town": "上北沢四丁目", "addr": "2-1",
            "lat": 35.669726, "lng": 139.620901, "level": 3}


def test_normalize_0044():
    assert normalize('東京都世田谷区上北沢４ー２ー１') == \
           {"pref": "東京都", "city": "世田谷区", "town": "上北沢四丁目", "addr": "2-1",
            "lat": 35.669726, "lng": 139.620901, "level": 3}


def test_normalize_0045():
    assert normalize('東京都世田谷区上北沢４－２－１') == \
           {"pref": "東京都", "city": "世田谷区", "town": "上北沢四丁目", "addr": "2-1",
            "lat": 35.669726, "lng": 139.620901, "level": 3}


def test_normalize_0046():
    assert normalize('東京都品川区西五反田2丁目31-6') == \
           {"pref": "東京都", "city": "品川区", "town": "西五反田二丁目", "addr": "31-6",
            "lat": 35.626368, "lng": 139.721005, "level": 3}


def test_normalize_0047():
    assert normalize('東京都品川区西五反田2-31-6') == \
           {"pref": "東京都", "city": "品川区", "town": "西五反田二丁目", "addr": "31-6",
            "lat": 35.626368, "lng": 139.721005, "level": 3}


def test_normalize_0048():
    assert normalize('大阪府大阪市此花区西九条三丁目２－１６') == \
           {"pref": "大阪府", "city": "大阪市此花区", "town": "西九条三丁目", "addr": "2-16",
            "lat": 34.684074, "lng": 135.467031, "level": 3}


def test_normalize_0049():
    assert normalize('大阪府大阪市此花区西九条三丁目2番16号') == \
           {"pref": "大阪府", "city": "大阪市此花区", "town": "西九条三丁目", "addr": "2-16",
            "lat": 34.684074, "lng": 135.467031, "level": 3}


def test_normalize_0050():
    assert normalize('大阪府大阪市此花区西九条3-2-16') == \
           {"pref": "大阪府", "city": "大阪市此花区", "town": "西九条三丁目", "addr": "2-16",
            "lat": 34.684074, "lng": 135.467031, "level": 3}


def test_normalize_0051():
    assert normalize('大阪府大阪市此花区西九条３丁目２－１６') == \
           {"pref": "大阪府", "city": "大阪市此花区", "town": "西九条三丁目", "addr": "2-16",
            "lat": 34.684074, "lng": 135.467031, "level": 3}


def test_normalize_0052():
    assert normalize('大阪府大阪市此花区西九条3-2-16') == \
           {"pref": "大阪府", "city": "大阪市此花区", "town": "西九条三丁目", "addr": "2-16",
            "lat": 34.684074, "lng": 135.467031, "level": 3}


def test_normalize_0053():
    assert normalize('千葉県鎌ケ谷市中佐津間２丁目１５－１４－９') == \
           {"pref": "千葉県", "city": "鎌ヶ谷市", "town": "中佐津間二丁目", "addr": "15-14-9",
            "lat": 35.800253, "lng": 140.002133, "level": 3}


def test_normalize_0054():
    assert normalize('岐阜県不破郡関ケ原町関ヶ原１７０１−６') == \
           {"pref": "岐阜県", "city": "不破郡関ケ原町", "town": "大字関ケ原", "addr": "1701-6",
            "lat": 35.368524, "lng": 136.464997, "level": 3}


def test_normalize_0055():
    assert normalize('岐阜県関ケ原町関ヶ原１７０１−６') == \
           {"pref": "岐阜県", "city": "不破郡関ケ原町", "town": "大字関ケ原", "addr": "1701-6",
            "lat": 35.368524, "lng": 136.464997, "level": 3}


def test_normalize_0056():
    assert normalize('東京都町田市木曽東4丁目14-イ22') == \
           {"pref": "東京都", "city": "町田市", "town": "木曽東四丁目", "addr": "14-イ22",
            "lat": 35.564817, "lng": 139.429661, "level": 3}


def test_normalize_0057():
    assert normalize('東京都町田市木曽東4丁目14ーイ22') == \
           {"pref": "東京都", "city": "町田市", "town": "木曽東四丁目", "addr": "14-イ22",
            "lat": 35.564817, "lng": 139.429661, "level": 3}


def test_normalize_0058():
    assert normalize('東京都町田市木曽東四丁目十四ーイ二十二') == \
           {"pref": "東京都", "city": "町田市", "town": "木曽東四丁目", "addr": "14-イ22",
            "lat": 35.564817, "lng": 139.429661, "level": 3}


def test_normalize_0059():
    assert normalize('東京都町田市木曽東四丁目１４ーイ２２') == \
           {"pref": "東京都", "city": "町田市", "town": "木曽東四丁目", "addr": "14-イ22",
            "lat": 35.564817, "lng": 139.429661, "level": 3}


def test_normalize_0060():
    assert normalize('東京都町田市木曽東四丁目１４のイ２２') == \
           {"pref": "東京都", "city": "町田市", "town": "木曽東四丁目", "addr": "14-イ22",
            "lat": 35.564817, "lng": 139.429661, "level": 3}


def test_normalize_0061():
    assert normalize('岩手県花巻市南万丁目127') == \
           {"pref": "岩手県", "city": "花巻市", "town": "南万丁目", "addr": "127",
            "lat": 39.387522, "lng": 141.088029, "level": 3}


def test_normalize_0062():
    assert normalize('和歌山県東牟婁郡串本町田並1512') == \
           {"pref": "和歌山県", "city": "東牟婁郡串本町", "town": "田並", "addr": "1512",
            "lat": 33.48681, "lng": 135.717844, "level": 3}


def test_normalize_0063():
    assert normalize('神奈川県川崎市多摩区東三田1-2-2') == \
           {"pref": "神奈川県", "city": "川崎市多摩区", "town": "東三田一丁目", "addr": "2-2",
            "lat": 35.612653, "lng": 139.549014, "level": 3}


def test_normalize_0064():
    assert normalize('東京都町田市木曽東４の１４のイ２２') == \
           {"pref": "東京都", "city": "町田市", "town": "木曽東四丁目", "addr": "14-イ22",
            "lat": 35.564817, "lng": 139.429661, "level": 3}


def test_normalize_0065():
    assert normalize('東京都町田市木曽東４ー１４ーイ２２') == \
           {"pref": "東京都", "city": "町田市", "town": "木曽東四丁目", "addr": "14-イ22",
            "lat": 35.564817, "lng": 139.429661, "level": 3}


def test_normalize_0066():
    assert normalize('富山県富山市三番町1番23号') == \
           {"pref": "富山県", "city": "富山市", "town": "三番町", "addr": "1-23",
            "lat": 36.688141, "lng": 137.217397, "level": 3}


def test_normalize_0067():
    assert normalize('富山県富山市3-1-23') == \
           {"pref": "富山県", "city": "富山市", "town": "三番町", "addr": "1-23",
            "lat": 36.688141, "lng": 137.217397, "level": 3}


def test_normalize_0068():
    assert normalize('富山県富山市中央通り3-1-23') == \
           {"pref": "富山県", "city": "富山市", "town": "中央通り三丁目", "addr": "1-23",
            "lat": 36.689604, "lng": 137.222128, "level": 3}


def test_normalize_0069():
    assert normalize('埼玉県南埼玉郡宮代町大字国納３０9－１') == \
           {"pref": "埼玉県", "city": "南埼玉郡宮代町", "town": "大字国納", "addr": "309-1",
            "lat": 36.038996, "lng": 139.697478, "level": 3}


def test_normalize_0070():
    assert normalize('埼玉県南埼玉郡宮代町国納３０9－１') == \
           {"pref": "埼玉県", "city": "南埼玉郡宮代町", "town": "大字国納", "addr": "309-1",
            "lat": 36.038996, "lng": 139.697478, "level": 3}


def test_normalize_0071():
    assert normalize('大阪府高槻市奈佐原２丁目１－２ メゾンエトワール') == \
           {"pref": "大阪府", "city": "高槻市", "town": "奈佐原二丁目", "addr": "1-2 メゾンエトワール",
            "lat": 34.861189, "lng": 135.579573, "level": 3}


def test_normalize_0072():
    assert normalize('埼玉県八潮市大字大瀬１丁目１－１') == \
           {"pref": "埼玉県", "city": "八潮市", "town": "大瀬一丁目", "addr": "1-1",
            "lat": 35.808825, "lng": 139.84291, "level": 3}


def test_normalize_0073():
    assert normalize('岡山県笠岡市大宜1249－1') == \
           {"pref": "岡山県", "city": "笠岡市", "town": "大宜", "addr": "1249-1",
            "lat": 34.506729, "lng": 133.473295, "level": 3}


def test_normalize_0074():
    assert normalize('岡山県笠岡市大宜1249－1') == \
           {"pref": "岡山県", "city": "笠岡市", "town": "大宜", "addr": "1249-1",
            "lat": 34.506729, "lng": 133.473295, "level": 3}


def test_normalize_0075():
    assert normalize('岡山県笠岡市大冝1249－1') == \
           {"pref": "岡山県", "city": "笠岡市", "town": "大宜", "addr": "1249-1",
            "lat": 34.506729, "lng": 133.473295, "level": 3}


def test_normalize_0076():
    assert normalize('岡山県岡山市中区さい33-2') == \
           {"pref": "岡山県", "city": "岡山市中区", "town": "さい", "addr": "33-2",
            "lat": 34.680505, "lng": 133.948429, "level": 3}


def test_normalize_0077():
    assert normalize('岡山県岡山市中区穝33-2') == \
           {"pref": "岡山県", "city": "岡山市中区", "town": "さい", "addr": "33-2",
            "lat": 34.680505, "lng": 133.948429, "level": 3}


def test_normalize_0078():
    assert normalize('千葉県松戸市栄町３丁目１６６－５') == \
           {"pref": "千葉県", "city": "松戸市", "town": "栄町三丁目", "addr": "166-5",
            "lat": 35.803015, "lng": 139.905619, "level": 3}


def test_normalize_0079():
    assert normalize('東京都新宿区三栄町１７－１６') == \
           {"pref": "東京都", "city": "新宿区", "town": "四谷三栄町", "addr": "17-16",
            "lat": 35.688757, "lng": 139.725668, "level": 3}


def test_normalize_0080():
    assert normalize('東京都新宿区三榮町１７－１６') == \
           {"pref": "東京都", "city": "新宿区", "town": "四谷三栄町", "addr": "17-16",
            "lat": 35.688757, "lng": 139.725668, "level": 3}


def test_normalize_0081():
    assert normalize('新潟県新潟市中央区礎町通１ノ町１９６８−１') == \
           {"pref": "新潟県", "city": "新潟市中央区", "town": "礎町通一ノ町", "addr": "1968-1",
            "lat": 37.920235, "lng": 139.049572, "level": 3}


def test_normalize_0082():
    assert normalize('新潟県新潟市中央区礎町通１の町１９６８−１') == \
           {"pref": "新潟県", "city": "新潟市中央区", "town": "礎町通一ノ町", "addr": "1968-1",
            "lat": 37.920235, "lng": 139.049572, "level": 3}


def test_normalize_0083():
    assert normalize('新潟県新潟市中央区礎町通１の町１９６８の１') == \
           {"pref": "新潟県", "city": "新潟市中央区", "town": "礎町通一ノ町", "addr": "1968-1",
            "lat": 37.920235, "lng": 139.049572, "level": 3}


def test_normalize_0084():
    assert normalize('新潟県新潟市中央区礎町通1-1968-1') == \
           {"pref": "新潟県", "city": "新潟市中央区", "town": "礎町通一ノ町", "addr": "1968-1",
            "lat": 37.920235, "lng": 139.049572, "level": 3}


def test_normalize_0085():
    assert normalize('新潟県新潟市中央区上大川前通11番町1881-2') == \
           {"pref": "新潟県", "city": "新潟市中央区", "town": "上大川前通十一番町", "addr": "1881-2",
            "lat": 37.927874, "lng": 139.049152, "level": 3}


def test_normalize_0086():
    assert normalize('新潟県新潟市中央区上大川前通11-1881-2') == \
           {"pref": "新潟県", "city": "新潟市中央区", "town": "上大川前通十一番町", "addr": "1881-2",
            "lat": 37.927874, "lng": 139.049152, "level": 3}


def test_normalize_0087():
    assert normalize('新潟県新潟市中央区上大川前通十一番町1881-2') == \
           {"pref": "新潟県", "city": "新潟市中央区", "town": "上大川前通十一番町", "addr": "1881-2",
            "lat": 37.927874, "lng": 139.049152, "level": 3}


def test_normalize_0088():
    assert normalize('埼玉県上尾市壱丁目１１１') == \
           {"pref": "埼玉県", "city": "上尾市", "town": "大字壱丁目", "addr": "111",
            "lat": 35.957701, "lng": 139.570578, "level": 3}


def test_normalize_0089():
    assert normalize('埼玉県上尾市一丁目１１１') == \
           {"pref": "埼玉県", "city": "上尾市", "town": "大字壱丁目", "addr": "111",
            "lat": 35.957701, "lng": 139.570578, "level": 3}


def test_normalize_0090():
    assert normalize('埼玉県上尾市一町目１１１') == \
           {"pref": "埼玉県", "city": "上尾市", "town": "大字壱丁目", "addr": "111",
            "lat": 35.957701, "lng": 139.570578, "level": 3}


def test_normalize_0091():
    assert normalize('埼玉県上尾市壱町目１１１') == \
           {"pref": "埼玉県", "city": "上尾市", "town": "大字壱丁目", "addr": "111",
            "lat": 35.957701, "lng": 139.570578, "level": 3}


def test_normalize_0092():
    assert normalize('埼玉県上尾市1-111') == \
           {"pref": "埼玉県", "city": "上尾市", "town": "大字壱丁目", "addr": "111",
            "lat": 35.957701, "lng": 139.570578, "level": 3}


def test_normalize_0093():
    assert normalize('神奈川県横浜市港北区大豆戸町１７番地１１') == \
           {"pref": "神奈川県", "city": "横浜市港北区", "town": "大豆戸町", "addr": "17-11",
            "lat": 35.513492, "lng": 139.625651, "level": 3}


def test_normalize_0094():
    assert normalize('神奈川県横浜市港北区大豆戸町１７番地１１', level=1) == \
           {"pref": "神奈川県", "city": "", "town": "", "addr": "横浜市港北区大豆戸町17番地11",
            "lat": None, "lng": None, "level": 1}


def test_normalize_0095():
    assert normalize('神奈川県横浜市港北区大豆戸町１７番地１１', level=2) == \
           {"pref": "神奈川県", "city": "横浜市港北区", "town": "", "addr": "大豆戸町17番地11",
            "lat": None, "lng": None, "level": 2}


def test_normalize_0096():
    assert normalize('神奈川県横浜市港北区大豆戸町１７番地１１', level=3) == \
           {"pref": "神奈川県", "city": "横浜市港北区", "town": "大豆戸町", "addr": "17-11",
            "lat": 35.513492, "lng": 139.625651, "level": 3}


def test_normalize_0097():
    assert normalize('神奈川県横浜市港北区', level=3) == \
           {"pref": "神奈川県", "city": "横浜市港北区", "town": "", "addr": "",
            "lat": None, "lng": None, "level": 2}


def test_normalize_0098():
    assert normalize('神奈川県', level=3) == \
           {"pref": "神奈川県", "city": "", "town": "", "addr": "",
            "lat": None, "lng": None, "level": 1}


def test_normalize_0099():
    assert normalize('神奈川県あいうえお市') == \
           {"pref": "神奈川県", "city": "", "town": "", "addr": "あいうえお市",
            "lat": None, "lng": None, "level": 1}


def test_normalize_0100():
    assert normalize('東京都港区あいうえお') == \
           {"pref": "東京都", "city": "港区", "town": "", "addr": "あいうえお",
            "lat": None, "lng": None, "level": 2}


def test_normalize_0101():
    assert normalize('あいうえお') == \
           {"pref": "", "city": "", "town": "", "addr": "あいうえお",
            "lat": None, "lng": None, "level": 0}


def test_normalize_0102():
    assert normalize('東京都江東区豊洲1丁目2-27') == \
           {"pref": "東京都", "city": "江東区", "town": "豊洲一丁目", "addr": "2-27",
            "lat": 35.661813, "lng": 139.792044, "level": 3}


def test_normalize_0103():
    assert normalize('東京都江東区豊洲 1丁目2-27') == \
           {"pref": "東京都", "city": "江東区", "town": "豊洲一丁目", "addr": "2-27",
            "lat": 35.661813, "lng": 139.792044, "level": 3}


def test_normalize_0104():
    assert normalize('東京都江東区豊洲 1-2-27') == \
           {"pref": "東京都", "city": "江東区", "town": "豊洲一丁目", "addr": "2-27",
            "lat": 35.661813, "lng": 139.792044, "level": 3}


def test_normalize_0105():
    assert normalize('東京都 江東区 豊洲 1-2-27') == \
           {"pref": "東京都", "city": "江東区", "town": "豊洲一丁目", "addr": "2-27",
            "lat": 35.661813, "lng": 139.792044, "level": 3}


def test_normalize_0106():
    assert normalize('東京都江東区豊洲 １ー２ー２７') == \
           {"pref": "東京都", "city": "江東区", "town": "豊洲一丁目", "addr": "2-27",
            "lat": 35.661813, "lng": 139.792044, "level": 3}


def test_normalize_0107():
    assert normalize('東京都町田市木曽東四丁目１４ーイ２２ ジオロニアマンション') == \
           {"pref": "東京都", "city": "町田市", "town": "木曽東四丁目", "addr": "14-イ22 ジオロニアマンション",
            "lat": 35.564817, "lng": 139.429661, "level": 3}


def test_normalize_0108():
    assert normalize('東京都町田市木曽東四丁目１４ーＡ２２ ジオロニアマンション') == \
           {"pref": "東京都", "city": "町田市", "town": "木曽東四丁目", "addr": "14-A22 ジオロニアマンション",
            "lat": 35.564817, "lng": 139.429661, "level": 3}


def test_normalize_0109():
    assert normalize('東京都町田市木曽東四丁目一四━Ａ二二 ジオロニアマンション') == \
           {"pref": "東京都", "city": "町田市", "town": "木曽東四丁目", "addr": "14-A22 ジオロニアマンション",
            "lat": 35.564817, "lng": 139.429661, "level": 3}


def test_normalize_0110():
    assert normalize('東京都江東区豊洲 一丁目2-27') == \
           {"pref": "東京都", "city": "江東区", "town": "豊洲一丁目", "addr": "2-27",
            "lat": 35.661813, "lng": 139.792044, "level": 3}


def test_normalize_0111():
    assert normalize('東京都江東区豊洲 四-2-27') == \
           {"pref": "東京都", "city": "江東区", "town": "豊洲四丁目", "addr": "2-27",
            "lat": 35.653798, "lng": 139.800664, "level": 3}


def test_normalize_0112():
    assert normalize('石川県七尾市藤橋町亥45番地1') == \
           {"pref": "石川県", "city": "七尾市", "town": "藤橋町", "addr": "亥45-1",
            "lat": 37.041154, "lng": 136.941183, "level": 3}


def test_normalize_0113():
    assert normalize('石川県七尾市藤橋町亥四十五番地1') == \
           {"pref": "石川県", "city": "七尾市", "town": "藤橋町", "addr": "亥45-1",
            "lat": 37.041154, "lng": 136.941183, "level": 3}


def test_normalize_0114():
    assert normalize('石川県七尾市藤橋町 亥 四十五番地1') == \
           {"pref": "石川県", "city": "七尾市", "town": "藤橋町", "addr": "亥45-1",
            "lat": 37.041154, "lng": 136.941183, "level": 3}


def test_normalize_0115():
    assert normalize('石川県七尾市藤橋町 亥 45-1') == \
           {"pref": "石川県", "city": "七尾市", "town": "藤橋町", "addr": "亥45-1",
            "lat": 37.041154, "lng": 136.941183, "level": 3}


def test_normalize_0116():
    assert normalize('和歌山県和歌山市 七番丁 19') == \
           {"pref": "和歌山県", "city": "和歌山市", "town": "七番丁", "addr": "19",
            "lat": 34.230447, "lng": 135.171994, "level": 3}


def test_normalize_0117():
    assert normalize('和歌山県和歌山市7番町19') == \
           {"pref": "和歌山県", "city": "和歌山市", "town": "七番丁", "addr": "19",
            "lat": 34.230447, "lng": 135.171994, "level": 3}


def test_normalize_0118():
    assert normalize('和歌山県和歌山市十二番丁45') == \
           {"pref": "和歌山県", "city": "和歌山市", "town": "十二番丁", "addr": "45",
            "lat": 34.232035, "lng": 135.172088, "level": 3}


def test_normalize_0119():
    assert normalize('和歌山県和歌山市12番丁45') == \
           {"pref": "和歌山県", "city": "和歌山市", "town": "十二番丁", "addr": "45",
            "lat": 34.232035, "lng": 135.172088, "level": 3}


def test_normalize_0120():
    assert normalize('和歌山県和歌山市12-45') == \
           {"pref": "和歌山県", "city": "和歌山市", "town": "十二番丁", "addr": "45",
            "lat": 34.232035, "lng": 135.172088, "level": 3}


def test_normalize_0121():
    assert normalize('兵庫県宝塚市東洋町1番1号') == \
           {"pref": "兵庫県", "city": "宝塚市", "town": "東洋町", "addr": "1-1",
            "lat": 34.797971, "lng": 135.363236, "level": 3}


def test_normalize_0122():
    assert normalize('兵庫県宝塚市東洋町1番1号') == \
           {"pref": "兵庫県", "city": "宝塚市", "town": "東洋町", "addr": "1-1",
            "lat": 34.797971, "lng": 135.363236, "level": 3}


def test_normalize_0123():
    assert normalize('北海道札幌市中央区北三条西３丁目１－５６マルゲンビル３Ｆ') == \
           {"pref": "北海道", "city": "札幌市中央区", "town": "北三条西三丁目", "addr": "1-56マルゲンビル3F",
            "lat": 43.065075, "lng": 141.351683, "level": 3}


def test_normalize_0124():
    assert normalize('北海道札幌市北区北２４条西６丁目１−１') == \
           {"pref": "北海道", "city": "札幌市北区", "town": "北二十四条西六丁目", "addr": "1-1",
            "lat": 43.090538, "lng": 141.340527, "level": 3}


def test_normalize_0125():
    assert normalize('堺市北区新金岡町4丁1−8') == \
           {"pref": "大阪府", "city": "堺市北区", "town": "新金岡町四丁", "addr": "1-8",
            "lat": 34.568184, "lng": 135.519409, "level": 3}


def test_normalize_0126():
    assert normalize('串本町串本1234') == \
           {"pref": "和歌山県", "city": "東牟婁郡串本町", "town": "串本", "addr": "1234",
            "lat": 33.470358, "lng": 135.779952, "level": 3}


def test_normalize_0127():
    assert normalize('広島県府中市府川町315') == \
           {"pref": "広島県", "city": "府中市", "town": "府川町", "addr": "315",
            "lat": 34.567649, "lng": 133.236891, "level": 3}


def test_normalize_0128():
    assert normalize('府中市府川町315') == \
           {"pref": "広島県", "city": "府中市", "town": "府川町", "addr": "315",
            "lat": 34.567649, "lng": 133.236891, "level": 3}


def test_normalize_0129():
    assert normalize('府中市宮西町2丁目24番地') == \
           {"pref": "東京都", "city": "府中市", "town": "宮西町二丁目", "addr": "24",
            "lat": 35.669764, "lng": 139.477636, "level": 3}


def test_normalize_0130():
    assert normalize('三重県三重郡菰野町大字大強原2796') == \
           {"pref": "三重県", "city": "三重郡菰野町", "town": "大字大強原", "addr": "2796",
            "lat": 35.028963, "lng": 136.530668, "level": 3}


def test_normalize_0131():
    assert normalize('三重県三重郡菰野町大強原2796') == \
           {"pref": "三重県", "city": "三重郡菰野町", "town": "大字大強原", "addr": "2796",
            "lat": 35.028963, "lng": 136.530668, "level": 3}


def test_normalize_0132():
    assert normalize('福岡県北九州市小倉南区大字井手浦874') == \
           {"pref": "福岡県", "city": "北九州市小倉南区", "town": "大字井手浦", "addr": "874",
            "lat": 33.77509, "lng": 130.893088, "level": 3}


def test_normalize_0133():
    assert normalize('福岡県北九州市小倉南区井手浦874') == \
           {"pref": "福岡県", "city": "北九州市小倉南区", "town": "大字井手浦", "addr": "874",
            "lat": 33.77509, "lng": 130.893088, "level": 3}


def test_normalize_0134():
    assert normalize('沖縄県那覇市小禄１丁目５番２３号１丁目マンション３０１') == \
           {"pref": "沖縄県", "city": "那覇市", "town": "小禄一丁目", "addr": "5-23 一丁目マンション301",
            "lat": 26.192719, "lng": 127.679409, "level": 3}


def test_normalize_0135():
    assert normalize('香川県仲多度郡まんのう町勝浦字家六２０９４番地１') == \
           {"pref": "香川県", "city": "仲多度郡まんのう町", "town": "勝浦", "addr": "家六2094-1",
            "lat": 34.097457, "lng": 133.97318, "level": 3}


def test_normalize_0136():
    assert normalize('香川県仲多度郡まんのう町勝浦家六２０９４番地１') == \
           {"pref": "香川県", "city": "仲多度郡まんのう町", "town": "勝浦", "addr": "家六2094-1",
            "lat": 34.097457, "lng": 133.97318, "level": 3}


def test_normalize_0137():
    assert normalize('愛知県あま市西今宿梶村一３８番地４') == \
           {"pref": "愛知県", "city": "あま市", "town": "西今宿", "addr": "梶村一38-4",
            "lat": 35.2002, "lng": 136.831606, "level": 3}


def test_normalize_0138():
    assert normalize('香川県丸亀市原田町字東三分一１９２６番地１') == \
           {"pref": "香川県", "city": "丸亀市", "town": "原田町", "addr": "東三分一1926-1",
            "lat": 34.258954, "lng": 133.78778, "level": 3}


def test_normalize_0139():
    assert normalize('串本町串本千二百三十四') == \
           {"pref": "和歌山県", "city": "東牟婁郡串本町", "town": "串本", "addr": "1234",
            "lat": 33.470358, "lng": 135.779952, "level": 3}


def test_normalize_0140():
    assert normalize('せたな町北檜山区北檜山１９３') == \
           {"pref": "北海道", "city": "久遠郡せたな町", "town": "北檜山区北檜山", "addr": "193",
            "lat": 42.414, "lng": 139.881784, "level": 3}


def test_normalize_0141():
    assert normalize('岩手県花巻市十二丁目７０４') == \
           {"pref": "岩手県", "city": "花巻市", "town": "十二丁目", "addr": "704",
            "lat": 39.358268, "lng": 141.122331, "level": 3}


def test_normalize_0142():
    assert normalize('岩手県花巻市12丁目７０４') == \
           {"pref": "岩手県", "city": "花巻市", "town": "十二丁目", "addr": "704",
            "lat": 39.358268, "lng": 141.122331, "level": 3}


def test_normalize_0143():
    assert normalize('岩手県花巻市１２丁目７０４') == \
           {"pref": "岩手県", "city": "花巻市", "town": "十二丁目", "addr": "704",
            "lat": 39.358268, "lng": 141.122331, "level": 3}


def test_normalize_0144():
    assert normalize('京都府京都市中京区河原町二条下ル一之船入町537-50') == \
           {"pref": "京都府", "city": "京都市中京区", "town": "一之船入町", "addr": "537-50",
            "lat": 35.01217, "lng": 135.769483, "level": 3}


def test_normalize_0145():
    assert normalize('京都府宇治市莵道森本8−10') == \
           {"pref": "京都府", "city": "宇治市", "town": "莵道", "addr": "森本8-10",
            "lat": 34.904244, "lng": 135.827041, "level": 3}


def test_normalize_0146():
    assert normalize('京都府京都市中京区河原町二条下ル一之舟入町537-50') == \
           {"pref": "京都府", "city": "京都市中京区", "town": "一之船入町", "addr": "537-50",
            "lat": 35.01217, "lng": 135.769483, "level": 3}


def test_normalize_0147():
    assert normalize('京都府宇治市菟道森本8−10') == \
           {"pref": "京都府", "city": "宇治市", "town": "莵道", "addr": "森本8-10",
            "lat": 34.904244, "lng": 135.827041, "level": 3}


def test_normalize_0148():
    assert normalize('岩手花巻市１２丁目７０４') == \
           {"pref": "岩手県", "city": "花巻市", "town": "十二丁目", "addr": "704",
            "lat": 39.358268, "lng": 141.122331, "level": 3}


def test_normalize_0149():
    # 市(し、いち)と巿(ふつ)のゆらぎ
    assert normalize('千葉県巿川巿巿川1丁目') == \
           {"pref": "千葉県", "city": "市川市", "town": "市川一丁目", "addr": "",
            "lat": 35.731849, "lng": 139.909029, "level": 3}


def test_normalize_0150():
    assert normalize('京都市北区紫野東御所田町') == \
           {"pref": "京都府", "city": "京都市北区", "town": "紫野東御所田町", "addr": "",
            "lat": 35.039861, "lng": 135.753474, "level": 3}


def test_normalize_0151():
    assert normalize('鹿児島市山下町') == \
           {"pref": "鹿児島県", "city": "鹿児島市", "town": "山下町", "addr": "",
            "lat": 31.596716, "lng": 130.55643, "level": 3}


def test_normalize_0152():
    assert normalize('市川市八幡1丁目1番1号') == \
           {"pref": "千葉県", "city": "市川市", "town": "八幡一丁目", "addr": "1-1",
            "lat": 35.720285, "lng": 139.932528, "level": 3}


def test_normalize_0153():
    assert normalize('千葉市川市八幡1丁目1番1号') == \
           {"pref": "千葉県", "city": "市川市", "town": "八幡一丁目", "addr": "1-1",
            "lat": 35.720285, "lng": 139.932528, "level": 3}


def test_normalize_0154():
    assert normalize('石川郡石川町字長久保185-4') == \
           {"pref": "福島県", "city": "石川郡石川町", "town": "字長久保", "addr": "185-4",
            "lat": 37.155602, "lng": 140.446048, "level": 3}


def test_normalize_0155():
    assert normalize('福島石川郡石川町字長久保185-4') == \
           {"pref": "福島県", "city": "石川郡石川町", "town": "字長久保", "addr": "185-4",
            "lat": 37.155602, "lng": 140.446048, "level": 3}


def test_normalize_0156():
    # 町丁目に長音符(ー)が入る場合で、丁目の数字がその後に続く場合
    assert normalize('広島市西区商工センター六丁目9番39号') == \
           {"pref": "広島県", "city": "広島市西区", "town": "商工センター六丁目", "addr": "9-39",
            "lat": 34.36812, "lng": 132.388293, "level": 3}


def test_normalize_0157():
    # 町丁目に長音符(ー)が入る場合で、丁目の数字が 1 の場合
    assert normalize('新潟県新潟市西区流通センター一丁目1-1') == \
           {"pref": "新潟県", "city": "新潟市西区", "town": "流通センター一丁目", "addr": "1-1",
            "lat": 37.866158, "lng": 138.998185, "level": 3}


def test_normalize_0158():
    # 町丁目に長音符(ー)が入る場合
    assert normalize('青森県八戸市北インター工業団地4丁目1-1') == \
           {"pref": "青森県", "city": "八戸市", "town": "北インター工業団地四丁目", "addr": "1-1",
            "lat": 40.556931, "lng": 141.426763, "level": 3}


def test_normalize_0159():
    assert normalize('富山県高岡市オフィスパーク1-1') == \
           {"pref": "富山県", "city": "高岡市", "town": "オフィスパーク", "addr": "1-1",
            "lat": 36.670088, "lng": 136.998867, "level": 3}


def test_normalize_0160():
    assert normalize('福井県三方上中郡若狭町若狭テクノバレー1-1') == \
           {"pref": "福井県", "city": "三方上中郡若狭町", "town": "若狭テクノバレー", "addr": "1-1",
            "lat": 35.477349, "lng": 135.859423, "level": 3}
