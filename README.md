git # airfoilplotter
翼型を描画するAutocadスクリプトファイルを生成するプログラムです．

# 使い方
１．まずこのリポジトリをクローンします
```
git clone https://github.com/FlyingSheeps/airfoilplotter.git
```
２．クローンしたリポジトリに入ります
```
cd airfoilplotter
```
３．必要に応じてExcelファイルの中身を書き換えてから以下のコマンドで実行します．（書き換え方はexcelファイルに書いてあります．）
```
python3 airfoilplotter.py
```
４．もしエラーが出た場合，必要なモジュールなどを追加してください．素のpythonの場合，numpy,scipy,openpyxlなどを要求されると思われます．pypiやanacondaでインストールしましょう．
```
pip install numpy
pip install scipy
pip install openpyxl
```
