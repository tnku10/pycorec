# 連番画像ピクセル座標取得プログラム(pycorec)
# Version 1.0.7 (2023-06-15)
# 管理者:北海道大学大学院水産科学研究院 海洋生物資源科学部門 水産工学分野・大学院環境科学院 生物圏科学専攻 海洋生物生産学コース 髙木力研究室
# Managed by TAKAGI Tsutomu's laboratory (Faculty of Fisheries Sciences, Hokkaido Univ.)
# 開発環境
# Python 3.9.4
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

# 1.PycharmやSpyderなどIDEで本スクリプトを開き，実行します。

# 2.pycorecのウィンドウが立ち上がります。まず読み込む画像についての情報を入力してください。
# 画像時空間パラメーターの指定(オプション項目)
#   1.画像の相対時刻を記録したい場合，「フレームレート(fps)」の横のテキストボックスに自然数で値を入力してください。
#     fpsは何枚の画像で1秒間の動画が構成されるかを示す値です。
#     画像の時刻情報が必要ない場合は，空欄のままで結構です。
#   2.画像座標から実空間物理座標への変換を行いたい場合「物理座標変換スケール(cm/px)」の横のテキストボックスに小数で値を入力してください。
#     画像座標(px)で出力する場合は，空欄のままで結構です。

# 画像読み込みパラメーターの指定(必須項目)
#   3.「画像の表示倍率」の横のテキストボックスに小数で表示倍率を入力してください。(初期値は0.5)
#     本来の画像サイズで表示すると画面に収まらない事が多いため，アスペクト比(縦横比)を維持したまま縮小表示を行う必要があります。
#   4.「フレームインターバル」の横のテキストボックスに自然数でフレームインターバル(表示する画像の間隔)を入力してください。
#       初期値は1が設定されており，この場合読み込み対象の全画像を読み込みます。
#       例)001-010までの連番画像について
#       読み込みたい画像が001,003,005の場合インターバル=2, 001,004,007の場合インターバル=3を指定


# 3.画像読込の方法のうち1つをボタンクリックにより選択します。
# A. 指定したフォルダ内の全画像からインターバルに従って読み込むモード「フォルダ選択(フォルダ内画像一括選択)」
# B. ファイル選択画面で指定した同一フォルダ内の連続した1つの範囲の画像からインターバルに従って読み込むモード「ファイル選択(連続範囲選択)」
# C. ファイル選択画面で画像を複数選択によって直接指定して読み込むモード「ファイル選択(複数・任意選択可能)」

# AとBについて事前に指定したフレームインターバルが適用されます。Cには適用されません。
# 例)インターバル=1でA.「フォルダ選択(フォルダ内画像一括選択)」を選択した場合，フォルダ内の全画像が読み込まれます。
# 例)インターバル=1でB.「ファイル選択(連続範囲選択)」を選択した場合，指定した全画像が読み込まれます。
# 例)インターバル=2でA.「フォルダ選択(フォルダ内画像一括選択)」を選択した場合，フォルダ内の連番の最小画像から1つおきに画像が読み込まれます。
# 例)インターバル=2でB.「ファイル選択(連続範囲選択)」を選択した場合，指定した画像のうち連番の最小画像から1つおきに画像が読み込まれます。

# 4.画像は連番の小さい順に読み込まれ，1枚ずつ表示されます。
# 画像座標系では左上が(0,0)で，右に行くほどx座標が増加し，下に行くほどy座標が増加します。
# マウスを動かすと十字で画像上の位置が示され，左上に(x,y)のピクセル座標が表示されます。
# 画像上で左クリックを行うと座標記録ができます。複数点記録することも可能です。各画像1点目は必ず記録が必要です。記録しないと遷移しません。
# 右クリックするとその回数分だけ遡って同画像の記録座標を削除します。画像を遡って削除が進行することはありません
# 次の画像に移行したいときは，右矢印キー(→)を押してください(キー入力を検知しているためどのキーを押しても同様に反応します)。
# 途中で記録処理を強制終了したい場合はマウスホイールを押し込んでください。ウィンドウを閉じても次の画像が開くため終了できません。
# 強制終了時にcsv出力保存先の選択画面が表示されます。途中経過を保存したい場合は「保存」を，破棄して終了したい場合は「キャンセル」を押してください。

# 5.全画像記録し終えると，画像ウィンドウが表示されなくなり,csvファイルの保存先選択画面が表示されます。
# 座標データを記録したcsvファイルの保存先とファイル名を指定してください。
# 「保存」を押すと出力処理は完了です。
# 誤ってキャンセルを押してしまった場合「csv保存」ボタンを押すことで再度保存を行うことができます。


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
# Version 1.0.3 (2022-02-01)
# ● 「Bkg」をファイル名に含む画像を読み込まないように変更
# ● 強制終了前にcsv保存できるように変更
# ● 全画像表示終了後にcsv保存画面が表示されるように変更
# ● インターバルの仕様を変更 例)読み込みたい画像が001,003,005の場合インターバル＞2
# Version 1.0.4 (2022-02-02)
# ● 画像クリック時に表示されるデータフレームの行数を前後3行，列数を6行(3点のx,y)のみに限定
# Version 1.0.5 (2022-02-03)
# ● フレームレート(fps)，物理座標変換スケール(cm/px)の値を入力する機能を追加し，座標(cm)と相対時刻(s)の出力機能を追加
# ● 読み込みモードをA「フォルダ選択(フォルダ内画像一括選択)」,B「ファイル選択(連続範囲選択)」,C「ファイル選択(複数・任意選択可能)」に変更。
#   フレームインターバルの指定による間隔を開けた画像の読み込みをAに加えてBのフォルダ内任意の連続範囲についても可能とした。
# Version 1.0.6 (2022-02-04)
# ● 2枚目以降の画像は1画像につき1点は必ず記録しないとキーを押しても次の画像に遷移しないように変更。

# 追加予定機能
# 画像中一点目の時系列座標グラフ出力
# 物理座標系においてy軸正の向きを反転する機能
# Cモードでの相対時刻記録
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
import win32gui  # pip install pywin32

# 画像の選択と表示(読込画像フォルダ選択(一括選択)モード)
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
    all_files = natsorted([p for p in path.glob('**/*')
                           if not re.search('Bkg', str(p)) and re.search('/*\.(jpg|jpeg|png|tif|bmp)', str(p))])
    # インターバルに応じてファイルリストを修正
    interval = int(intervaltxtbox.get())
    all_files = all_files[::interval]
    # 座標記録用に空のデータフレームを作成
    df = pd.DataFrame(index=range(len(all_files)))
    # 相対時刻の列を作成(fpsが入力されたときのみ動作)
    fps = fpstxtbox.get()
    if not fps == '':
        fps = int(fps)
        spf = 1 / fps
        timestep = interval * spf
        end = 0 + (len(all_files) - 1) * timestep
        sec = np.linspace(0, end, num=len(all_files))
        df['file name'] = ''
        df['Time(s)'] = sec
    # 物理座標用j記録
    jcheck = []
    win_left = 0
    win_top = 0
    win_right = 0
    win_bottom = 0
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

        if i == 0:
            cv2.moveWindow(file_name_, 300, 0)  # ウィンドウ初期表示位置指定
            cv2.setMouseCallback(file_name_, coordinates)
            hwnd = cv2.namedWindow(file_name_)  # ウィンドウのハンドルを取得
            win_left, win_top, win_right, win_bottom = win32gui.GetWindowRect(hwnd)  # ウィンドウ表示位置座標を取得する
            cv2.waitKey(0)

        if i > 0:
            cv2.moveWindow(file_name_, win_left, win_top)  # ウィンドウ表示位置指定
            cv2.setMouseCallback(file_name_, coordinates)
            cv2.waitKey(0)
            while pd.isna(df.at[df.index[i], 'x0(px)']):
                cv2.setMouseCallback(file_name_, coordinates)
                cv2.waitKey(0)

        jcheck.append(j)  # 物理座標用
        j = -1
        cv2.destroyAllWindows()

    # 物理座標系に変換(cm/pxが入力されたときのみ動作)
    scale = scaletxtbox.get()
    if not scale == '':
        scale = float(scale)
        jmax = max(jcheck)
        for j in range(0, jmax+1):
            df[f'x{j}(cm)'] = df[f'x{j}(px)'] * scale
            df[f'y{j}(cm)'] = df[f'y{j}(px)'] * scale
    # 実行時刻の記録
    now = datetime.datetime.now()
    current_time = now.strftime('%Y-%m-%d-%H-%M')
    # 保存ファイル名を指定
    csv_path = tk.filedialog.asksaveasfilename(title='csvファイル保存先・ファイル名指定',
                                               filetypes=[("CSV Files", ".csv")],
                                               initialfile=f'pycorec_{current_time}')
    df.to_csv(f'{csv_path}.csv', encoding='utf-8')


# 画像の選択と表示(読込画像ファイル選択(連続範囲選択)モード)
def getrange():
    global i
    global j
    global df
    global img2
    global file_name_
    # 使用する画像のファイルリストを指定
    filetyp = [('画像ファイル', '*.jpg *.JPG *.jpeg *.png *.PNG *.bmp *.BMP *.tif')]
    file_path = tk.filedialog.askopenfilenames(title='画像ファイル選択(連続範囲選択)', filetypes=filetyp)
    # 画像のファイルリストを作成
    all_files = natsorted(file_path)
    # インターバルに応じてファイルリストを修正
    interval = int(intervaltxtbox.get())
    all_files = all_files[::interval]
    # 座標記録用に空のデータフレームを作成
    df = pd.DataFrame(index=range(len(all_files)))
    # 相対時刻の列を作成
    fps = fpstxtbox.get()
    if not fps == '':
        fps = int(fpstxtbox.get())
        spf = 1 / fps
        timestep = interval * spf
        end = 0 + (len(all_files) - 1) * timestep
        sec = np.linspace(0, end, num=len(all_files))
        df['file name'] = ''
        df['Time(s)'] = sec
    # 物理座標用j記録
    jcheck = []
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
        if i > 0:
            while pd.isna(df.at[df.index[i], 'x0(px)']):
                cv2.setMouseCallback(file_name_, coordinates)
                cv2.waitKey(0)
        jcheck.append(j)  # 物理座標用
        j = -1
        cv2.destroyAllWindows()

    # 物理座標系に変換(cm/pxが入力されたときのみ動作)
    scale = scaletxtbox.get()
    if not scale == '':
        scale = float(scale)
        jmax = max(jcheck)
        for j in range(0, jmax + 1):
            df[f'x{j}(cm)'] = df[f'x{j}(px)'] * scale
            df[f'y{j}(cm)'] = df[f'y{j}(px)'] * scale
    # 実行時刻の記録
    now = datetime.datetime.now()
    current_time = now.strftime('%Y-%m-%d-%H-%M')
    # 保存ファイル名を指定
    csv_path = tk.filedialog.asksaveasfilename(title='csvファイル保存先・ファイル名指定',
                                               filetypes=[("CSV Files", ".csv")],
                                               initialfile=f'pycorec_{current_time}')
    df.to_csv(f'{csv_path}.csv', encoding='utf-8')


# 画像の選択と表示(読込画像ファイル選択(複数・任意選択可能)モード)
def getfile():
    global i
    global j
    global df
    global img2
    global file_name_
    # 使用する画像のファイルリストを指定
    filetyp = [('画像ファイル', '*.jpg *.JPG *.jpeg *.png *.PNG *.bmp *.BMP *.tif')]
    file_path = tk.filedialog.askopenfilenames(title='画像ファイル選択(複数選択可)', filetypes=filetyp)
    # 画像のファイルリストを作成
    all_files = natsorted(file_path)
    # 座標記録用に空のデータフレームを作成
    df = pd.DataFrame(index=range(len(all_files)))
    # 物理座標用j記録
    jcheck = []
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
        if i > 0:
            while pd.isna(df.at[df.index[i], 'x0(px)']):
                cv2.setMouseCallback(file_name_, coordinates)
                cv2.waitKey(0)
        jcheck.append(j)  # 物理座標用
        j = -1
        cv2.destroyAllWindows()

    # 物理座標系に変換(cm/pxが入力されたときのみ動作)
    scale = scaletxtbox.get()
    if not scale == '':
        scale = float(scale)
        jmax = max(jcheck)
        for j in range(0, jmax + 1):
            df[f'x{j}(cm)'] = df[f'x{j}(px)'] * scale
            df[f'y{j}(cm)'] = df[f'y{j}(px)'] * scale
    # 実行時刻の記録
    now = datetime.datetime.now()
    current_time = now.strftime('%Y-%m-%d-%H-%M')
    # 保存ファイル名を指定
    csv_path = tk.filedialog.asksaveasfilename(title='csvファイル保存先・ファイル名指定',
                                               filetypes=[("CSV Files", ".csv")],
                                               initialfile=f'pycorec_{current_time}')
    df.to_csv(f'{csv_path}.csv', encoding='utf-8')


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
        if j <= 1:
            print(df.loc[i - 3:i + 3, 'file name':f'y{j}(px)'])
        if j > 1:
            print(df.loc[i - 3:i + 3, f'x{j - 2}(px)':f'y{j}(px)'])

    # 右クリックで取得座標を削除(同一画像中の複数点を遡って削除)
    if event == cv2.EVENT_RBUTTONDOWN and j >= 0:
        df.at[df.index[i], f'x{j}(px)'] = np.nan
        df.at[df.index[i], f'y{j}(px)'] = np.nan
        if j <= 1:
            print(df.loc[i - 3:i + 3, 'file name':f'y{j}(px)'])
        if j > 1:
            print(df.loc[i - 3:i + 3, f'x{j - 2}(px)':f'y{j}(px)'])
        j -= 1

    # ホイールクリックで強制終了
    if event == cv2.EVENT_MBUTTONDOWN:
        # 実行時刻の記録
        now = datetime.datetime.now()
        current_time = now.strftime('%Y-%m-%d-%H-%M')
        # 強制終了までの座標の保存ファイル名を指定
        csv_path = tk.filedialog.asksaveasfilename(title='csvファイル保存先・ファイル名指定',
                                                   filetypes=[("CSV Files", ".csv")],
                                                   initialfile=f'pycorec_incomplete_{current_time}')
        df.to_csv(f'{csv_path}.csv', encoding='utf-8')
        quit()


# csvファイルを保存
def csv():
    # 実行時刻の記録
    now = datetime.datetime.now()
    current_time = now.strftime('%Y-%m-%d-%H-%M')
    # 保存ファイル名を指定
    csv_path = tk.filedialog.asksaveasfilename(title='csvファイル保存先・ファイル名指定',
                                               filetypes=[("CSV Files", ".csv")],
                                               initialfile=f'pycorec_{current_time}')
    df.to_csv(f'{csv_path}.csv', encoding='utf-8')


# 画像ごとのクリック回数記録用
j = -1
# ウインドウの作成
root = tk.Tk()
# ウインドウのタイトル
root.title('pycorec1.0.6')
# ウインドウサイズと位置指定 幅,高さ,x座標,y座標
root.geometry('300x600+0+0')
# フレームの作成
frame = tk.Frame(root, width=280, height=580, bg='#D9D9D9')
frame.place(x=10, y=10)
frame_scale = tk.Frame(frame, relief=tk.FLAT, bg='#E6E6E6', bd=2)
frame_scale.place(x=5, y=30, width=270, height=70)
frame_display = tk.Frame(frame, relief=tk.FLAT, bg='#E6E6E6', bd=2)
frame_display.place(x=5, y=145, width=270, height=70)
frame_menu = tk.Frame(frame, relief=tk.FLAT, bg='#E6E6E6', bd=2)
frame_menu.place(x=5, y=250, width=270, height=85)
frame_save = tk.Frame(frame, relief=tk.FLAT, bg='#E6E6E6', bd=2)
frame_save.place(x=5, y=380, width=270, height=30)

# 画像時空間パラメーターの入力
tsparmlabel = tk.Label(text='画像時空間パラメーターの入力(オプション項目)', bg='#D9D9D9')
tsparmlabel.place(x=15, y=15)
# fps指定用テキストボックスの作成
fpstxtbox = tk.Entry(width=7)
fpstxtbox.place(x=120, y=50)
fpslabel = tk.Label(text='フレームレート(fps)', bg='#E6E6E6')
fpslabel.place(x=25, y=50)
# 物理座標変換スケール(cm/px)指定用テキストボックスの作成
scaletxtbox = tk.Entry(width=7)
scaletxtbox.place(x=185, y=80)
scalelabel = tk.Label(text='物理座標変換スケール(cm/px)', bg='#E6E6E6')
scalelabel.place(x=25, y=80)

# 画像の読み込みに関するパラメーター入力とモード選択
dpparmlabel = tk.Label(text='画像読み込みパラメーターの指定', bg='#D9D9D9')
dpparmlabel.place(x=15, y=130)
# 表示画像サイズ縮小のための倍率指定用テキストボックスの作成
pictxtbox = tk.Entry(width=7)
pictxtbox.insert(0, '0.5')
pictxtbox.place(x=130, y=165)
piclabel = tk.Label(text='画像の表示倍率', bg='#E6E6E6')
piclabel.place(x=25, y=165)
# フレームインターバル(画像読み込み間隔)の指定用テキストボックスの作成
intervaltxtbox = tk.Entry(width=7)
intervaltxtbox.insert(0, '1')
intervaltxtbox.place(x=130, y=195)
intervallabel = tk.Label(text='フレームインターバル', bg='#E6E6E6')
intervallabel.place(x=25, y=195)
noticelabel = tk.Label(text='(1=連番読込)', bg='#E6E6E6')
noticelabel.place(x=185, y=195)
# 画像の読み込み
modelabel = tk.Label(text='画像読み込み方法の選択', bg='#D9D9D9')
modelabel.place(x=15, y=235)

# データの出力
outputlabel = tk.Label(text='データの出力', bg='#D9D9D9')
outputlabel.place(x=15, y=365)

# 操作方法の記述
guidelabel = tk.Label(text='操作方法', bg='#D9D9D9')
guidelabel.place(x=15, y=480)
leftlabel = tk.Label(text='左クリック: 座標記録(複数点記録可能)', bg='#D9D9D9')
leftlabel.place(x=15, y=500)
rightlabel = tk.Label(text='右クリック: 記録済み座標を削除(同一画像中のみ)', bg='#D9D9D9')
rightlabel.place(x=15, y=520)
keylabel = tk.Label(text='矢印右キー: 次の画像に移動', bg='#D9D9D9')
keylabel.place(x=15, y=540)
centerlabel = tk.Label(text='マウスホイール押し込み: 強制終了', bg='#D9D9D9')
centerlabel.place(x=15, y=560)

# ボタン作成
button = tk.Button(frame_menu, text='フォルダ選択(フォルダ内画像一括選択)', command=getdir)
button.grid(row=1, column=0, sticky=tk.W)
button = tk.Button(frame_menu, text='ファイル選択(連続範囲選択)', command=getrange)
button.grid(row=14, column=0, sticky=tk.W)
button = tk.Button(frame_menu, text='ファイル選択(複数・任意選択可能)', command=getfile)
button.grid(row=28, column=0, sticky=tk.W)
button_csv = tk.Button(frame_save, text='csvファイル保存', command=csv)
button_csv.grid(row=1, column=0, sticky=tk.W)
# button_png = tk.Button(frame_save, text='時系列座標グラフ保存', command=csv)
# button_png.grid(row=1, column=1, sticky=tk.W)

# イベントループ
root.mainloop()
