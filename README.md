## @Taka710/normalize-japanese-addresses-py
[![PyPI](https://img.shields.io/pypi/l/normalize_japanese_addresses.svg)](https://pypi.python.org/pypi/normalize_japanese_addresses/)
[![PyPI](https://img.shields.io/pypi/v/normalize_japanese_addresses.svg)](https://pypi.python.org/pypi/normalize_japanese_addresses/)

オープンソースの住所正規化ライブラリです。

経産省の [IMI コンポーネントツール](https://info.gbiz.go.jp/tools/imi_tools/)のジオコーディングの仕組みから  
インスピレーションをうけて開発された [@geolonia/normalize-japanese-addresses](https://github.com/geolonia/normalize-japanese-addresses)を  
Pythonで利用できるように書き直したものです。

## 使い方
pypiで公開していますので、pipコマンドでインストールしてください。

```
pip install normalize-japanese-addresses
```

住所を正規化します。  

```python
from normalize_japanese_addresses import normalize
print(normalize("北海道札幌市西区24-2-2-3-3"))
# {'pref': '北海道', 'city': '札幌市西区', 'town': '二十四軒二条二丁目', 'addr': '3-3', 'lat': 43.074273, 'lng': 141.315099, 'level': 3}
```

住所の正規化結果として戻されるオブジェクトには、`level` プロパティが含まれます。`level` には、住所文字列のどこまでを判別できたかを以下の数値で格納しています。

* `0` - 都道府県も判別できなかった。
* `1` - 都道府県まで判別できた。
* `2` - 市区町村まで判別できた。
* `3` - 町丁目まで判別できた。

例えば都道府県名のみを正規化したい場合、`level` オプションで指定することで処理を早くすることができます。
```python
from normalize_japanese_addresses import normalize
print(normalize("北海道札幌市西区24-2-2-3-3", level=1))
# {'pref': '北海道', 'city': '', 'town': '', 'addr': '札幌市西区24-2-2-3-3', 'lat': 43.074273, 'lng': 141.315099, 'level': 1}
```

名寄せする住所は、[@geolonia/japanese-addresses](https://geolonia.github.io/japanese-addresses/api/ja)から都度取得しています。

`endpoint` オプションで `file://` 形式のURLを指定することで、ローカルファイルとして保存した住所を参照することができます。
```
# Geolonia 住所データのダウンロード
$ curl -sL https://github.com/geolonia/japanese-addresses/archive/refs/heads/master.tar.gz | tar xvfz -
```
※住所データを最新にしたい場合は都度上記コマンドでダウンロードしてください。

```python
from normalize_japanese_addresses import normalize
print(normalize("北海道札幌市西区24-2-2-3-3", endpoint="file:///path/to/japanese-addresses-master/api/ja"))
# {'pref': '北海道', 'city': '札幌市西区', 'town': '二十四軒二条二丁目', 'addr': '3-3', 'lat': 43.074273, 'lng': 141.315099, 'level': 3}
```


## 注意

以下の仕様は、元の [@geolonia/normalize-japanese-addresses](https://github.com/geolonia/normalize-japanese-addresses)を踏襲しています。  

* この正規化エンジンは、住所の「名寄せ」を目的としており、たとえば京都の「通り名」は削除します。
  * 郵便や宅急便などに使用される住所としては、問題ないと考えています。
* この正規化エンジンは、町丁目及び小字レベルまでは対応していますが、それ以降については対応しておりません。
* 住居表示が未整備の地域については全体的に苦手です。
* 漢数字と数字の変換については、[@geolonia/japanese-numeral](https://github.com/geolonia/japanese-numeral)をPythonに書き直して取り込んでいます。

## ライセンス、利用規約

ソースコードのライセンスは MIT ライセンスです。