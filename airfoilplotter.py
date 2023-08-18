# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 15:09:57 2021

@author: ko-ko
"""

import os
import sys
import numpy as np
import openpyxl as pyxl
from scipy import interpolate as interp
import math


"""------------------------------------------------------------"""
"""                                                            """
"""    　   入出力処理：ブック名のみ入力or.pyにドラッグアンドドロップ          """  
"""   　     ブック名入力はカレントディレクトリにあるもののみ対応する          """
"""　 　　　　    　　　　　　　　　　先頭の./は省くこと                       """
"""                                                            """
"""------------------------------------------------------------"""

bookpath = "airfoilplotter.xlsm"
bookname = bookpath[:-5]

"""------------------------------------------------------------"""

if not(len(sys.argv) == 1):
    if (sys.argv[1][-4:] == "xlsm") or (sys.argv[1][-4:] == "xlsx"):
        bookpath = sys.argv[1]
        bookname = sys.argv[1].split("/")
        bookname = bookpath[-1]
        bookname = bookpath[:-5]

print("ブックパス")
print(bookpath)
print("出力ファイル名")
print(bookname)
#ブックを開く
strcbook = pyxl.load_workbook(bookpath,data_only=True)


if not(os.path.isdir(bookname)):
    os.makedirs(bookname)


"""主翼翼型名と諸元取得"""
maindata = strcbook["Python読み込み用データ"] #諸元のシート
main_b = maindata["B2"].value*1000 #主翼スパン[mm]
main_cr = maindata["B3"].value*1000 #主翼ルートコード[mm]
main_cm = maindata["B4"].value*1000 #主翼ミッドコード[mm]
main_ct = maindata["B5"].value*1000 #主翼チップコード[mm]
main_yt = maindata["B6"].value*1000 #テーパ変更点[mm]
main_alpha = maindata["B7"].value*np.pi/180 #迎角[rad]
xspar = maindata["B8"].value #桁位置[-]
spar_dim = maindata["B9"].value #桁径[mm]

"""主翼翼型点群取得"""
main_airfoil_name = maindata["D1"].value #主翼翼形名
main_xy_len = maindata["G4"].value #点群の組数
main_x = [maindata["D" + str(i+4)].value for i in range(main_xy_len)] #主翼の点群x
main_y = [maindata["E" + str(i+4)].value for i in range(main_xy_len)] #主翼の点群y
main_xyu_len = maindata["N4"].value #上面点群の組数
main_xyl_len = maindata["O4"].value #下面点群の組数
main_xu = [maindata["I" + str(i+4)].value for i in range(main_xyu_len)] #主翼の上面x
main_yu = [maindata["J" + str(i+4)].value for i in range(main_xyu_len)] #主翼の上面y
main_xl = [maindata["K" + str(i+4)].value for i in range(main_xyl_len)] #主翼の下面x
main_yl = [maindata["L" + str(i+4)].value for i in range(main_xyl_len)] #主翼の下面y
"""補間関数作成"""
main_yu_func = interp.interp1d(main_xu,main_yu,kind="linear",fill_value="extrapolate") #上面の高さの関数
main_yl_func = interp.interp1d(main_xl, main_yl,kind="linear",fill_value="extrapolate") #下面の高さの関数
xtmp = np.arange(0,1+0.01,0.01)
main_yu = main_yu_func(xtmp)
main_yl = main_yl_func(xtmp)
main_camber = (main_yu + main_yl)/2
main_thikness = main_yu - main_yl
main_camber_func =  interp.interp1d(xtmp, main_camber,kind="linear",fill_value="extrapolate") #キャンバラインの高さの関数
main_thikness_func =  interp.interp1d(xtmp, main_camber,kind="linear",fill_value="extrapolate") #厚みの関数

"""リブ配置取得"""
main_rib_n = maindata["Q2"].value #主翼半分のリブ数
main_riblocation = [maindata["Q" + str(i+4)].value for i in range(main_rib_n)] #主翼リブ位置[mm]
del maindata

"""リブ位置でのコード長を計算"""
if main_yt == 0:
    main_c_list = [main_cr + (main_ct - main_cr) / (main_b / 2 - 0) * y  for y in main_riblocation]
else:
    main_c_list = [main_cr + (main_cm - main_cr) / (main_yt - 0) * y if y <= main_yt else main_cm + (main_ct - main_cm) / (main_b/2 - main_yt) * (y - main_yt) for y in main_riblocation]



"""------------------------------------------------------------"""
"""                                                            """
"""                           製図                              """
"""                                                            """
"""------------------------------------------------------------"""

"""主翼リブ製図"""
#コード長ごとにファイルを作成・書き込み
with open(bookname + "/" + main_airfoil_name + "_main_rib.scr","w") as scr:
    offset = 0
    
    for c in main_c_list:
    
        main_xc = [x*c for x in main_x]
        main_yc = [y*c for y in main_y]
        
        """コード長倍をかける"""
        xtmpc = xtmp*c #コード長座標系
        main_yuc = main_yu_func(xtmp)*c
        main_yuc_func = interp.interp1d(xtmpc,main_yuc)
        main_ylc = main_yl_func(xtmpc)*c
        main_ylc_func = interp.interp1d(xtmpc,main_ylc)
        main_camberc = main_camber_func(xtmp)*c
        main_camberc_func = interp.interp1d(xtmpc,main_camberc)
        main_thiknessc = main_thikness_func(xtmp)*c
        main_thiknessc_func = interp.interp1d(xtmpc,main_thiknessc)
            
        #翼型描画
        scr.write("spline\n")
        for (xi,yi) in zip(main_xc,main_yc):
            scr.write(str(xi - c*xspar) + "," + str(yi + offset) + "\n")
        scr.write("\n")
        scr.write("\n")
        scr.write("\n")
        
        """最後を閉じる"""
        scr.write("line\n")
        scr.write(str(main_xc[0] - c*xspar) + "," + str(main_yc[0] + offset) + "\n")
        scr.write(str(main_xc[-1] - c*xspar) + "," + str(main_yc[-1] + offset) + "\n")
        scr.write("\n")
        
        """スパー穴描画"""
        scr.write("circle\n")
        scr.write(str(0.0) + "," + str(main_camberc_func(c*xspar) + offset) + "\n")
        scr.write("D\n")
        scr.write(str(spar_dim) + "\n")
        
        
        
        """後縁の窪み"""
        scr.write("line\n")
        scr.write(str(c*(1-xspar)) + "," + str(offset+0.7) + "\n")
        scr.write(str(c*(1-xspar) - 10) + "," + str(main_camberc_func(c-10) + offset + 0.7) + "\n")
        scr.write(str(c*(1-xspar) - 10) + "," + str(main_camberc_func(c-10) + offset - 0.7) + "\n")
        scr.write(str(c*(1-xspar)) + "," + str(offset-0.7) + "\n")
        scr.write(str(c*(1-xspar)) + "," + str(offset+0.7) + "\n")
        scr.write("\n")
        
        
        
        """治具用ライン"""
        
        """描画用オフセット"""
        offset += 30
        
    
"""wing平面形"""
with open(bookname + "/mainwing.scr","w") as scr:
    
    """リブ"""
    for (c, y) in zip(main_c_list,main_riblocation):
        
        scr.write("line\n")
        scr.write(str(y) + "," + str(c*xspar) + "\n")
        scr.write(str(y) + "," + str(-c*(1-xspar)) + "\n")
        scr.write("\n")
        scr.write("line\n")
        scr.write(str(-y) + "," + str(c*xspar) + "\n")
        scr.write(str(-y) + "," + str(-c*(1-xspar)) + "\n")
        scr.write("\n")
    
    """tips"""
    scr.write("line\n")
    scr.write(str(-main_b/2) + "," + str(main_ct*xspar) + "\n")
    scr.write(str(-main_yt) + "," + str(main_cm*xspar) + "\n")
    scr.write(str(0) + "," + str(main_cr*xspar) + "\n")
    scr.write(str(main_yt) + "," + str(main_cm*xspar) + "\n")
    scr.write(str(main_b/2) + "," + str(main_ct*xspar) + "\n")
    scr.write("\n")
    scr.write("line\n")
    scr.write(str(-main_b/2) + "," + str(main_ct*(xspar-1)) + "\n")
    scr.write(str(-main_yt) + "," + str(main_cm*(xspar-1)) + "\n")
    scr.write(str(0) + "," + str(main_cr*(xspar-1)) + "\n")
    scr.write(str(main_yt) + "," + str(main_cm*(xspar-1)) + "\n")
    scr.write(str(main_b/2) + "," + str(main_ct*(xspar-1)) + "\n")
    scr.write("\n")
    scr.write("line\n")
    scr.write(str(-main_b/2) + "," + str(main_ct*xspar-15) + "\n")
    scr.write(str(-main_yt) + "," + str(main_cm*xspar-15) + "\n")
    scr.write(str(0) + "," + str(main_cr*xspar-15) + "\n")
    scr.write(str(main_yt) + "," + str(main_cm*xspar-15) + "\n")
    scr.write(str(main_b/2) + "," + str(main_ct*xspar-15) + "\n")
    scr.write("\n")
    scr.write("line\n")
    scr.write(str(-main_b/2) + "," + str(main_ct*(xspar-1)+15) + "\n")
    scr.write(str(-main_yt) + "," + str(main_cm*(xspar-1)+15) + "\n")
    scr.write(str(0) + "," + str(main_cr*(xspar-1)+15) + "\n")
    scr.write(str(main_yt) + "," + str(main_cm*(xspar-1)+15) + "\n")
    scr.write(str(main_b/2) + "," + str(main_ct*(xspar-1)+15) + "\n")
    scr.write("\n")

print("Autocad script files are saved in ./airfoilprotter")
tem = input()


