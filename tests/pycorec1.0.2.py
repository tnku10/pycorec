# 連番画像ピクセル座標取得プログラム(pycorec)
# Version 1.0.2 (2022-02-01)
# 管理者:北海道大学大学院水産科学研究院 海洋生物資源科学部門 水産工学分野・大学院環境科学院 生物圏科学専攻 海洋生物生産学コース 髙木力研究室
# 開発者:北海道大学大学院水産科学院 田中優斗
# Managed by TAKAGI Tsutomu's laboratory (Faculty of Fisheries Sciences, Hokkaido Univ.)
# Programmed by TANAKA Yuto (Graduate school of Fisheries Sciences, Hokkaido Univ.)
# 開発環境
# Python 3.9
# opencv-python 4.5.5.62
# natsort 8.0.2
# numpy 1.22.1
# pandas 1.4.0
# Pycharm Professional 2021.3.1
# CPU   Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz   2.11 GHz
# RAM   8.00 GB
# OS    Windows 11 Home 21H2


# 使い方
# 0.本ソフトウェアはファイル名に連番が付与された時系列画像ファイル(***_0001.jpg,***_0002.jpg,...等)を想定して作成されています。

# 1.Pycharmで本スクリプトを開き，スクリプト上で右クリックして，Run File in Python Consoleを選択します。

# 2.pycorecのウィンドウが立ち上がります。画像の表示倍率>の横に小数で表示倍率を入力してください。(初期値は0.6)
#   本来の画像サイズで表示すると画面に収まらない事が多いため，アスペクト比(縦横比)を維持したまま縮小表示を行う必要があります。

# 3.モード選択の画面が表示されたら，3種類の画像読込の方法のうち1つをボタンクリックにより選択します。
# A. 指定したフォルダ内の全画像を読み込むモード「フォルダ内全画像読み込み」
# B. 指定したフォルダ内の連番画像を指定間隔スキップして読み込むモード「フォルダ内画像スキップ読み込み」
#    本モードを使用する場合，ボタン横のテキストボックスにスキップ数(初期値1)を入力してからボタンを押してください。
#    例)読み込みたい画像が001,003,005の場合スキップ数＞１, 001,004,007の場合スキップ数＞2を指定
# C. 読み込みたい画像を複数選択によって直接指定するモード「画像ファイル指定(複数可)読み込み」

# 4.画像は連番の小さい順に読み込まれ，1枚ずつ表示されます。
# 画像が表示されたら左クリックで座標記録ができます。複数点記録することも可能です。
# 右クリックするとその回数分だけ遡って同画像の記録座標を削除します。画像を遡って削除が進行することはありません
# 次の画像に移行したいときは，右矢印キー(→)を押してください(キー入力を検知しているためどのキーを押しても同様に反応します)。
# 途中で記録処理を強制終了したい場合はマウスホイールを押し込んでください。ウィンドウを閉じても次の画像が開くため終了できません。

# 5.全画像記録し終えると，画像ウィンドウが表示されなくなります。
# 「csvファイル保存」のボタンを押すと，座標データを記録したcsvファイルの保存先とファイル名を指定する画面が表示されます。
# 「保存」を押すと出力処理は完了です。


# リリース履歴
# Version 1.0.0 (2022-01-28)
# ● 初期リリース
# Version 1.0.1 (2022-01-28)
# ● フォルダ内の全画像を読み込むモード「画像フォルダ選択」に加えて，
#   任意の複数画像を指定して読み込むモード「画像ファイル指定(複数選択可)」を追加。
# ● 画像座標の単位を(px)として記載
# ● 対象画像ファイル名をデータフレームの列として追加
# ● 出力CSVファイルのファイル名を指定できるように変更。
# Version 1.0.2 (2022-02-01)
# ● 日本語が含まれるファイルパスに対応(Numpyを経由して読み込むように変更)
# ● リアルタイムマウス位置画像座標表示機能の追加
# ● 画像スキップ読込モードを追加
# ● 画像の表示倍率を指定する機能を追加

# 追加予定機能
# リアルタイム記録座標表示機能(Pycharmを利用せずに実行できるように.exe化)
# フレーム数タイムクリック数フレームインターバルフレームレートタイムインターバル表示
# 動画avi読み込み


# ライブラリのインポート (system-included)
import datetime
from pathlib import Path
import re
import tkinter as tk
import tkinter.filedialog
# ライブラリのインポート (third-party)
import cv2  # pip install opencv-python
from natsort import natsorted  # pip install natsort
import numpy as np  # pip install numpy
import pandas as pd  # pip install pandas


# 画像の選択と表示(指定フォルダ内全画像読み込みモード)
def getdir():
    global i
    global j
    global df
    global img2
    global file_name_
    # 連番画像のフォルダを指定
    dir_path = tk.filedialog.askdirectory(title='画像フォルダ選択')
    # 連番画像のファイルリストを作成
    path = Path(dir_path)
    all_files = natsorted([p for p in path.glob('**/*') if re.search('/*\.(jpg|jpeg|png|tiff|bmp)', str(p))])
    # 座標記録用に空のデータフレームを作成
    df = pd.DataFrame(index=range(len(all_files)))
    # 1枚ずつ表示する
    for i, file_path_ in enumerate(all_files):
        file_name_ = Path(file_path_).stem
        file_path_ = str(file_path_)
        df.at[df.index[i], 'file name'] = file_name_
        # 画像の読み込み
        # OpenCVは日本語パス名非対応なためimreadでは日本語含まれると読み込めない
        # NumPyで画像ファイルを開き，OpenCV(Numpyのndarray)に変換して読み込む
        buf = np.fromfile(file_path_, np.uint8)
        img = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
        # 画像の縦横のサイズを取得(h:縦、ｗ：横)
        # h, w = img.shape[:2]
        # 入力された表示画像倍率を読み込む
        magnification = float(pictxtbox.get())
        # アスペクト比を固定して画像を変換
        img2 = cv2.resize(img, dsize=None, fx=magnification, fy=magnification)
        # 画像の表示
        cv2.imshow(file_name_, img2)
        # cv2.resizeWindow(file_name_, 960, 732)  # ウィンドウサイズ
        cv2.moveWindow(file_name_, 300, 0)  # ウィンドウ表示位置指定
        cv2.setMouseCallback(file_name_, coordinates)
        cv2.waitKey(0)
        j = -1
        cv2.destroyAllWindows()


# 画像の選択と表示(指定フォルダ内連番画像スキップ読み込みモード)
def getskipfile():
    global i
    global j
    global df
    global img2
    global file_name_
    # 連番画像のフォルダを指定
    dir_path = tk.filedialog.askdirectory(title='画像フォルダ選択')
    # 連番画像のファイルリストを作成
    path = Path(dir_path)
    all_files = natsorted([p for p in path.glob('**/*') if re.search('/*\.(jpg|jpeg|png|tif|bmp)', str(p))])
    # スキップ数に応じてファイルリストを修正
    skipnum = int(skiptxtbox.get()) + 1
    all_files = all_files[::skipnum]
    # 座標記録用に空のデータフレームを作成
    df = pd.DataFrame(index=range(len(all_files)))
    # 1枚ずつ表示する
    for i, file_path_ in enumerate(all_files):
        file_name_ = Path(file_path_).stem
        file_path_ = str(file_path_)
        df.at[df.index[i], 'file name'] = file_name_
        # 画像の読み込み
        # OpenCVは日本語パス名非対応なためimreadでは日本語含まれると読み込めない
        # NumPyで画像ファイルを開き，OpenCV(Numpyのndarray)に変換して読み込む
        buf = np.fromfile(file_path_, np.uint8)
        img = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
        # # 縦横のサイズを取得(h:縦、ｗ：横)
        # h, w = img.shape[:2]
        # 入力された表示画像倍率を読み込む
        magnification = float(pictxtbox.get())
        # アスペクト比を固定して画像を変換
        img2 = cv2.resize(img, dsize=None, fx=magnification, fy=magnification)
        # h2, w2 = img2.shape[:2]
        # 画像の表示
        cv2.imshow(file_name_, img2)
        # cv2.resizeWindow(file_name_, 960, 732)  # ウィンドウサイズ
        cv2.moveWindow(file_name_, 300, 0)  # ウィンドウ表示位置指定
        cv2.setMouseCallback(file_name_, coordinates)
        cv2.waitKey(0)
        j = -1
        cv2.destroyAllWindows()


# 画像の選択と表示(指定複数画像ファイル読み込みモード)
def getfile():
    global i
    global j
    global df
    global img2
    global file_name_
    # 使用する画像のファイルリストを指定
    filetyp = [('画像ファイル', '*.jpg *.JPG *.jpeg *.png *.PNG *.bmp *.BMP *.tif')]
    dir_path = tk.filedialog.askopenfilenames(title='画像ファイル選択(複数選択可)', filetypes=filetyp)
    # 画像のファイルリストを作成
    all_files = natsorted(dir_path)
    # 座標記録用に空のデータフレームを作成
    df = pd.DataFrame(index=range(len(all_files)))
    # 1枚ずつ表示する
    for i, file_path_ in enumerate(all_files):
        file_name_ = Path(file_path_).stem
        file_path_ = str(file_path_)
        df.at[df.index[i], 'file name'] = file_name_
        # 画像の読み込み
        buf = np.fromfile(file_path_, np.uint8)
        img = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
        # # 縦横のサイズを取得(h:縦、ｗ：横)
        # h, w = img.shape[:2]
        # 入力された表示画像倍率を読み込む
        magnification = float(pictxtbox.get())
        # アスペクト比を固定して画像を変換
        img2 = cv2.resize(img, dsize=None, fx=magnification, fy=magnification)
        # h2, w2 = img2.shape[:2]
        # 画像の表示
        cv2.imshow(file_name_, img2)
        # cv2.resizeWindow(file_name_, 960, 732)  # ウィンドウサイズ
        cv2.moveWindow(file_name_, 300, 0)  # ウィンドウ表示位置指定
        cv2.setMouseCallback(file_name_, coordinates)
        cv2.waitKey(0)
        j = -1
        cv2.destroyAllWindows()


# マウスクリック時の動作を定義
def coordinates(event, x, y, flags, param):
    global j
    global df
    global file_name_

    # マウス移動に連動して座標を表示
    if event == cv2.EVENT_MOUSEMOVE:
        img3 = np.copy(img2)
        # cv2.circle(img3, center=(x, y), radius=5, color=255, thickness=-1)
        pos_str = '(' + str(x) + ',' + str(y) + ')'
        cv2.putText(img3, pos_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (248, 180, 138), 2, cv2.LINE_AA)
        cv2.imshow(file_name_, img3)

    # 左クリックで座標を取得(複数点記録することも可能)
    if event == cv2.EVENT_LBUTTONDOWN:
        j += 1
        df.at[df.index[i], f'x{j}(px)'] = x
        df.at[df.index[i], f'y{j}(px)'] = y
        print(df)

    # 右クリックで取得座標を削除(同一画像中の複数点を遡って削除)
    if event == cv2.EVENT_RBUTTONDOWN:
        if j >= 0:
            df.at[df.index[i], f'x{j}(px)'] = 'NaN'
            df.at[df.index[i], f'y{j}(px)'] = 'NaN'
            print(df)
            j -= 1

    # ホイールクリックで強制終了
    if event == cv2.EVENT_MBUTTONDOWN:
        # 強制終了までの座標の保存ファイル名を指定
        csv_path = tk.filedialog.asksaveasfilename(title='csvファイル保存先・ファイル名指定',
                                                   filetypes=[("CSV Files", ".csv")],
                                                   initialfile=f'pycorec_incomplete_{current_time}')
        df.to_csv(f'{csv_path}.csv', encoding='utf-8')
        quit()


# csvファイルを保存
def save():
    # 保存ファイル名を指定
    csv_path = tk.filedialog.asksaveasfilename(title='csvファイル保存先・ファイル名指定',
                                               filetypes=[("CSV Files", ".csv")],
                                               initialfile=f'pycorec_{current_time}')
    df.to_csv(f'{csv_path}.csv', encoding='utf-8')


# 実行時刻の記録
now = datetime.datetime.now()
current_time = now.strftime('%Y-%m-%d-%H-%M')
# 画像ごとのクリック回数記録用
j = -1
# データフレームの列を省略せずに表示するように設定
pd.set_option('display.max_columns', None)
# ウインドウの作成
root = tk.Tk()
# ウインドウのタイトル
root.title('pycorec1.02')
# ウインドウサイズと位置指定 幅,高さ,x座標,y座標
root.geometry('300x200+0+0')
# フレームの作成
frame = tk.Frame(root, width=280, height=180, bg='#D9D9D9')
frame.place(x=10, y=10)
frame_menu = tk.Frame(frame, relief=tk.FLAT, bg='#E6E6E6', bd=2)
frame_menu.place(x=5, y=50, width=270, height=80)
frame_save = tk.Frame(frame, relief=tk.FLAT, bg='#D9D9D9', bd=2)
frame_save.place(x=5, y=145, width=90, height=30)

# 表示画像サイズ縮小のための倍率指定用テキストボックスの作成
pictxtbox = tk.Entry(width=5)
pictxtbox.insert(0, '0.6')
pictxtbox.place(x=110, y=15)
piclabel = tk.Label(text='画像の表示倍率', bg='#D9D9D9')
piclabel.place(x=15, y=15)

# 画像読み込みモード
modelabel = tk.Label(text='画像読み込み方法の選択', bg='#D9D9D9')
modelabel.place(x=15, y=40)

# スキップ数の指定用テキストボックスの作成
skiptxtbox = tk.Entry(width=5)
skiptxtbox.insert(0, '1')
skiptxtbox.place(x=235, y=90)
skiplabel = tk.Label(text='スキップ数', bg='#E6E6E6')
skiplabel.place(x=180, y=90)

# ボタン作成
button = tk.Button(frame_menu, text='フォルダ内全画像読み込み', command=getdir)
button.grid(row=1, column=0, sticky=tk.W)
button = tk.Button(frame_menu, text='フォルダ内画像スキップ読み込み', command=getskipfile)
button.grid(row=14, column=0, sticky=tk.W)
button = tk.Button(frame_menu, text='画像ファイル指定(複数可)読み込み', command=getfile)
button.grid(row=28, column=0, sticky=tk.W)
button_save = tk.Button(frame_save, text='csvファイル保存', command=save)
button_save.grid(row=1, column=0, sticky=tk.W)

# イベントループ
root.mainloop()
