# pickcolor

その画像に使われている色の彩度・明度情報をグラフにプロットします。
カラーサークルのどこから色をピックアップするかの参考とするために作成しました。

## 使用例

コマンドライン引数に画像のファイルパスを指定して利用します。複数指定することもできます。

```
python pickcolor.py (画像ファイルのパス) [(画像ファイルのパス) (画像ファイルのパス) ...]
```

画像が入っているディレクトリ名を指定した場合は、そのディレクトリ内の画像ファイル（現時点ではpngのみ）すべてを対象とします。

```
python pickcolor.py (ディレクトリ名)
```


## 必須ライブラリ

必要なライブラリ：

* numpy == 1.22.3
* Pillow == 9.2.0
* matplotlib == 3.6.1

(バージョンは開発環境にインストールされているライブラリのもの)
