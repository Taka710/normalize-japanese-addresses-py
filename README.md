## @Taka710/normalize-japanese-addresses-py

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
# {'pref': '北海道', 'city': '札幌市西区', 'town': '二十四軒二条二丁目', 'addr': '3-3', 'level': 3}
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
# {'pref': '北海道', 'city': '', 'town': '', 'addr': '札幌市西区24-2-2-3-3', 'level': 1}
```

## 注意

以下の仕様は、元の [@geolonia/normalize-japanese-addresses](https://github.com/geolonia/normalize-japanese-addresses)を踏襲しています。  

* この正規化エンジンは、住所の「名寄せ」を目的としており、たとえば京都の「通り名」は削除します。
  * 郵便や宅急便などに使用される住所としては、問題ないと考えています。
* この正規化エンジンは、町丁目及び小字レベルまでは対応していますが、それ以降については対応しておりません。
* 住居表示が未整備の地域については全体的に苦手です。
* 名寄せする住所は、[@geolonia/japanese-addresses](https://geolonia.github.io/japanese-addresses/api/ja)から都度取得しています。　
* 漢数字と数字の変換については、[@geolonia/japanese-numeral](https://github.com/geolonia/japanese-numeral)をPythonに書き直して取り込んでいます。

## ライセンス、利用規約

ソースコードのライセンスは MIT ライセンスです。