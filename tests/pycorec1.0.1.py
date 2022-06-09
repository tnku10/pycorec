# 連番画像ピクセル座標取得プログラム(pycorec)
# Version 1.0.1 (2022-01-28)
# 管理者:北海道大学大学院水産科学研究院 海洋生物資源科学部門 水産工学分野・大学院環境科学院 生物圏科学専攻 海洋生物生産学コース 髙木力研究室
# 開発者:北海道大学大学院水産科学院 田中優斗
# Managed by TAKAGI Tsutomu's laboratory (Faculty of Fisheries Sciences, Hokkaido Univ.)
# Programmed by TANAKA Yuto (Graduate school of Fisheries Sciences, Hokkaido Univ.)
# Python 3.9
# OpenCVの仕様により，読み込み対象画像のディレクトリ名に日本語が含まれるとエラーとなる。英数字のみのディレクトリ名構成が必要。

# リリース履歴
# Version 1.0.0 (2022-01-28)
# ● 初期リリース
# Version 1.0.1 (2022-01-28)
# ● ディレクトリ内の全画像を読み込むモード「画像ディレクトリ選択」に加えて，
#   任意の複数画像を指定して読み込むモード「画像ファイル指定(複数選択可)」を追加。
# ● 画像座標の単位を(px)として記載
# ● 対象画像ファイル名をデータフレームの列として追加
# ● 出力CSVファイルのファイル名を指定できるように変更。

# 追加予定機能
# リアルタイムマウス位置画像座標表示機能
# リアルタイム記録座標表示機能
# 画像の巻き戻し
# フレーム数タイムクリック数フレームインターバルフレームレートタイムインターバル表示
# 動画avi読み込み

# ライブラリのインポート (system-included)
import datetime
from pathlib import Path
import tkinter as tk
import tkinter.filedialog
# ライブラリのインポート (third-party)
import cv2
from natsort import natsorted
import numpy as np
import pandas as pd


# 画像の選択と表示
def getdir():
    global img
    global i
    global j
    global df
    text_widget.delete('1.0', 'end')
    # 連番画像のディレクトリを指定
    dir_path = tk.filedialog.askdirectory(title='画像ディレクトリ選択')
    # 連番画像のファイルリストを作成
    all_files = natsorted(Path(dir_path).glob('*'))
    # 座標記録用に空のデータフレームを作成
    df = pd.DataFrame(index=range(len(all_files)))
    print(df)
    # 1枚ずつ表示する
    for i, file_path_ in enumerate(all_files):
        file_name_ = Path(file_path_).stem
        file_path_ = str(file_path_)
        # 画像の読み込み
        img = cv2.imread(file_path_)
        # リサイズ後の長辺のサイズ
        re_length = 960
        # 縦横のサイズを取得(h:縦、ｗ：横)
        h, w = img.shape[:2]
        # 変換する倍率を計算
        re_h = re_w = re_length / max(h, w)
        # アスペクト比を固定して画像を変換
        img2 = cv2.resize(img, dsize=None, fx=re_h, fy=re_w)
        h2, w2 = img2.shape[:2]
        # 画像の表示
        cv2.imshow(file_name_, img2)
        # cv2.resizeWindow(file_name_, 960, 732)  # ウィンドウサイズ
        cv2.moveWindow(file_name_, 450, 50)  # ウィンドウ表示位置指定
        cv2.setMouseCallback(file_name_, coordinates)
        cv2.waitKey(0)
        text_widget.insert('insert', '\n')
        j = -1
        cv2.destroyAllWindows()


# 画像の選択と表示
def getfile():
    global img
    global i
    global j
    global df
    text_widget.delete('1.0', 'end')
    # 使用する画像のファイルリストを指定
    dir_path = tk.filedialog.askopenfilenames(title='画像ファイル選択(複数選択可)')
    # 画像のファイルリストを作成
    all_files = natsorted(dir_path)
    # 座標記録用に空のデータフレームを作成
    df = pd.DataFrame(index=range(len(all_files)))
    print(df)
    # 1枚ずつ表示する
    for i, file_path_ in enumerate(all_files):
        file_name_ = Path(file_path_).stem
        file_path_ = str(file_path_)
        df.at[df.index[i], 'file name'] = file_name_
        # 画像の読み込み
        img = cv2.imread(file_path_)
        # リサイズ後の長辺のサイズ
        re_length = 960
        # 縦横のサイズを取得(h:縦、ｗ：横)
        h, w = img.shape[:2]
        # 変換する倍率を計算
        re_h = re_w = re_length / max(h, w)
        # アスペクト比を固定して画像を変換
        img2 = cv2.resize(img, dsize=None, fx=re_h, fy=re_w)
        h2, w2 = img2.shape[:2]
        # 画像の表示
        cv2.imshow(file_name_, img2)
        # cv2.resizeWindow(file_name_, 960, 732)  # ウィンドウサイズ
        cv2.moveWindow(file_name_, 450, 50)  # ウィンドウ表示位置指定
        cv2.setMouseCallback(file_name_, coordinates)
        cv2.waitKey(0)
        text_widget.insert('insert', '\n')
        j = -1
        cv2.destroyAllWindows()


# マウスクリック時の動作を定義
def coordinates(event, x, y, flags, param):
    # 左クリックで座標を取得(複数点記録することも可能)
    global j
    global df
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        j += 1
        df.at[df.index[i], f'x{j}(px)'] = x
        df.at[df.index[i], f'y{j}(px)'] = y
        print(df)
        text_widget.insert('insert +1lines', str(x) + ',' + str(y) + ',')

    # 右クリックで取得座標を削除(同一画像中の複数点を遡って削除)
    if event == cv2.EVENT_RBUTTONDOWN:
        df.at[df.index[i], f'x{j}(px)'] = 'NaN'
        df.at[df.index[i], f'y{j}(px)'] = 'NaN'
        print(df)
        if j >= 1:
            j -= 1
        text_widget.delete('insert +1lines')

    # ホイールクリックで強制終了
    if event == cv2.EVENT_MBUTTONDOWN:
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

# ウインドウの作成
root = tk.Tk()
# ウインドウのタイトル
root.title('pycorec1.01')
# ウインドウサイズと位置指定 幅,高さ,x座標,y座標
root.geometry('350x470+50+50')
# フレームの作成
frame = tk.Frame(root, width=330, height=450, bg='#D9D9D9')
frame.place(x=10, y=10)
frame_menu = tk.Frame(frame, relief=tk.FLAT, bg='#E6E6E6', bd=2)
frame_menu.place(x=10, y=10, width=150, height=430)
frame_img = tk.Frame(frame, relief=tk.FLAT, bg='#E6E6E6', bd=2)
frame_img.place(x=170, y=10, width=150, height=430)

# テキストボックスの作成
text_widget = tk.Text(frame_img, height=30, width=30)
text_widget.grid(row=0, column=0, sticky=tk.W)

# ボタン作成
button = tk.Button(frame_menu, text='画像ディレクトリ指定', command=getdir)
button.grid(row=1, column=0, sticky=tk.W)
button = tk.Button(frame_menu, text='画像ファイル指定(複数可)', command=getfile)
button.grid(row=14, column=0, sticky=tk.W)
button_save = tk.Button(frame_menu, text='csvファイル保存', command=save)
button_save.grid(row=28, column=0, sticky=tk.W)

# イベントループ
root.mainloop()
