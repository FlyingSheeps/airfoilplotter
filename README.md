# airfoilplotter
翼型を描画するAutocadスクリプトファイルを生成するプログラムです．

# 使い方 (airfoilplotter.py)
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
５．実行結果はairfoilplotterディレクトリ内に.scrファイルとして出力されます．

# 使い方 (plot_foil_chord.py)
１．翼型のデータをnaca0018.datと同じ形にします．  
２．以下のコマンドを実行します．
```
python3 plot_foil_chord.py (翼型のファイル名) (コード長[mm]) > (書き出したいファイル名.scr)
```
３．実行結果は(書き出したいファイル名.scr)に出力されます．
