*******
@Taka710/normalize-japanese-addresses-py
*******

オープンソースの住所正規化ライブラリです。

| 経産省の `IMI コンポーネントツール <https://info.gbiz.go.jp/tools/imi_tools/>`_ のジオコーディングの仕組みから
| インスピレーションをうけて開発された `@geolonia/normalize-japanese-addresses <https://github.com/geolonia/normalize-japanese-addresses>`_ を
| Pythonで利用できるように書き直したものです。

****
注意
****

以下の仕様は、元のgeolonia/normalize-japanese-addressesを踏襲しています。  

* この正規化エンジンは、住所の「名寄せ」を目的としており、たとえば京都の「通り名」は削除します。

  * 郵便や宅急便などに使用される住所としては、問題ないと考えています。
  
* この正規化エンジンは、町丁目及び小字レベルまでは対応していますが、それ以降については対応しておりません。
* 住居表示が未整備の地域については全体的に苦手です。
* 名寄せする住所は、`@geolonia/japanese-addresses <https://geolonia.github.io/japanese-addresses/api/ja>`_ から都度取得しています。　
* 漢数字と数字の変換については、`@geolonia/japanese-numeral <https://github.com/geolonia/japanese-numeral>`_ をPythonに書き直して取り込んでいます。

****
ライセンス、利用規約
****

ソースコードのライセンスは MIT ライセンスです。