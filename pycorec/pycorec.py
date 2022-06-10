# 連番画像ピクセル座標取得プログラム(pycorec)

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


class PyCorec:
    def __init__(self):
        self.i = 0
        self.j = -1
        self.df = pd.DataFrame()
        self.all_files = []
        self.img2 = np.zeros((10, 10, 3), np.uint8)
        self.interval = 0
        self.file_name_ = Path().stem

    # 画像の選択と表示(読込画像フォルダ選択(一括選択)モード)
    def getdir(self):
        # 連番画像のフォルダを指定
        dir_path = tk.filedialog.askdirectory(title='画像フォルダ選択')
        # 連番画像のファイルリストを作成
        path = Path(dir_path)
        all_files = natsorted([p for p in path.glob('**/*')
                               if not re.search('Bkg', str(p)) and re.search('/*\.(jpg|jpeg|png|tif|bmp)', str(p))])
        # インターバルに応じてファイルリストを修正
        self.interval = int(intervaltxtbox.get())
        self.all_files = all_files[::self.interval]
        # 画像の表示と座標データ保存
        self.record()

    # 画像の選択と表示(読込画像ファイル選択(連続範囲選択)モード)
    def getrange(self):
        # 使用する画像のファイルリストを指定
        filetyp = [('画像ファイル', '*.jpg *.JPG *.jpeg *.png *.PNG *.bmp *.BMP *.tif')]
        file_path = tk.filedialog.askopenfilenames(title='画像ファイル選択(連続範囲選択)', filetypes=filetyp)
        # 画像のファイルリストを作成
        all_files = natsorted(file_path)
        # インターバルに応じてファイルリストを修正
        self.interval = int(intervaltxtbox.get())
        self.all_files = all_files[::self.interval]
        # 画像の表示と座標データ保存
        self.record()

    # 画像の選択と表示(読込画像ファイル選択(複数・任意選択可能)モード)
    def getfile(self):
        # 使用する画像のファイルリストを指定
        filetyp = [('画像ファイル', '*.jpg *.JPG *.jpeg *.png *.PNG *.bmp *.BMP *.tif')]
        file_path = tk.filedialog.askopenfilenames(title='画像ファイル選択(複数選択可)', filetypes=filetyp)
        # 画像のファイルリストを作成
        self.all_files = natsorted(file_path)
        # 画像の表示と座標データ保存
        self.record()

    # 画像の表示と座標データ保存
    def record(self):
        # 座標記録用に空のデータフレームを作成
        self.df = pd.DataFrame(index=range(len(self.all_files)))
        # 相対時刻の列を作成(fpsが入力されたときのみ動作)
        fps = fpstxtbox.get()
        if not fps == '':
            fps = int(fps)
            spf = 1 / fps
            timestep = self.interval * spf
            end = 0 + (len(self.all_files) - 1) * timestep
            sec = np.linspace(0, end, num=len(self.all_files))
            self.df['file name'] = ''
            self.df['Time(s)'] = sec
        # 物理座標用j記録
        jcheck = []
        # 画像ごとのクリック回数記録用
        self.j = -1
        # 入力された表示画像倍率を読み込む
        magnification = float(pictxtbox.get())
        # 1枚ずつ表示する
        for self.i, file_path_ in enumerate(self.all_files):
            self.file_name_ = Path(file_path_).stem
            file_path_ = str(file_path_)
            self.df.at[self.df.index[self.i], 'file name'] = self.file_name_
            # 画像の読み込み
            # OpenCVは日本語パス名非対応なためimreadでは日本語含まれると読み込めない
            # NumPyで画像ファイルを開き，OpenCV(Numpyのndarray)に変換して読み込む
            buf = np.fromfile(file_path_, np.uint8)
            img = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
            # アスペクト比を固定して画像を変換
            self.img2 = cv2.resize(img, dsize=None, fx=magnification, fy=magnification)
            # 画像の表示
            cv2.imshow(self.file_name_, self.img2)
            # cv2.resizeWindow(file_name_, 960, 732)  # ウィンドウサイズ
            cv2.moveWindow(self.file_name_, 300, 0)  # ウィンドウ表示位置指定
            cv2.setMouseCallback(self.file_name_, self.coordinates)
            cv2.waitKey(0)
            if self.i > 0:
                while pd.isna(self.df.at[self.df.index[self.i], 'x0(px)']):
                    cv2.setMouseCallback(self.file_name_, self.coordinates)
                    cv2.waitKey(0)
            jcheck.append(self.j)  # 物理座標用
            self.j = -1
            cv2.destroyAllWindows()

        # cm/pxの値受け取り
        scale = scaletxtbox.get()
        # 表示倍率による変化を適用
        if scale == '':
            jmax = max(jcheck)
            for j in range(0, jmax + 1):
                self.df[f'x{j}(px)'] = self.df[f'x{j}(px)'] / magnification
                self.df[f'y{j}(px)'] = self.df[f'y{j}(px)'] / magnification

        # 物理座標系に変換(cm/pxが入力されたときのみ動作)
        if not scale == '':
            scale = float(scale)
            jmax = max(jcheck)
            for j in range(0, jmax + 1):
                self.df[f'x{j}(px)'] = self.df[f'x{j}(px)'] / magnification
                self.df[f'y{j}(px)'] = self.df[f'y{j}(px)'] / magnification
                self.df[f'x{j}(cm)'] = self.df[f'x{j}(px)'] * scale
                self.df[f'y{j}(cm)'] = self.df[f'y{j}(px)'] * scale
        # 実行時刻の記録
        now = datetime.datetime.now()
        current_time = now.strftime('%Y-%m-%d-%H-%M')
        # 保存ファイル名を指定
        csv_path = tk.filedialog.asksaveasfilename(title='csvファイル保存先・ファイル名指定',
                                                   filetypes=[("CSV Files", ".csv")],
                                                   initialfile=f'pycorec_{current_time}')
        self.df.to_csv(f'{csv_path}.csv', encoding='utf-8')

    # マウスクリック時の動作を定義
    def coordinates(self, mode, x, y):
        # マウス移動に連動して座標を表示
        if mode == cv2.EVENT_MOUSEMOVE:
            img3 = np.copy(self.img2)
            # cv2.circle(img3, center=(x, y), radius=5, color=255, thickness=-1)
            pos_str = '(' + str(x) + ',' + str(y) + ')'
            cv2.putText(img3, pos_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (248, 180, 138), 2, cv2.LINE_AA)
            cv2.imshow(self.file_name_, img3)

        # 左クリックで座標を取得(複数点記録することも可能)
        if mode == cv2.EVENT_LBUTTONDOWN:
            self.j += 1
            self.df.at[self.df.index[self.i], f'x{self.j}(px)'] = x
            self.df.at[self.df.index[self.i], f'y{self.j}(px)'] = y
            if self.j <= 1:
                print(self.df.loc[self.i - 3:self.i + 3, 'file name':f'y{self.j}(px)'])
            if self.j > 1:
                print(self.df.loc[self.i - 3:self.i + 3, f'x{self.j - 2}(px)':f'y{self.j}(px)'])

        # 右クリックで取得座標を削除(同一画像中の複数点を遡って削除)
        if mode == cv2.EVENT_RBUTTONDOWN and self.j >= 0:
            self.df.at[self.df.index[self.i], f'x{self.j}(px)'] = np.nan
            self.df.at[self.df.index[self.i], f'y{self.j}(px)'] = np.nan
            if self.j <= 1:
                print(self.df.loc[self.i - 3:self.i + 3, 'file name':f'y{self.j}(px)'])
            if self.j > 1:
                print(self.df.loc[self.i - 3:self.i + 3, f'x{self.j - 2}(px)':f'y{self.j}(px)'])
            self.j -= 1

        # ホイールクリックで強制終了
        if mode == cv2.EVENT_MBUTTONDOWN:
            # 実行時刻の記録
            now = datetime.datetime.now()
            current_time = now.strftime('%Y-%m-%d-%H-%M')
            # 強制終了までの座標の保存ファイル名を指定
            csv_path = tk.filedialog.asksaveasfilename(title='csvファイル保存先・ファイル名指定',
                                                       filetypes=[("CSV Files", ".csv")],
                                                       initialfile=f'pycorec_incomplete_{current_time}')
            self.df.to_csv(f'{csv_path}.csv', encoding='utf-8')
            quit()

    # csvファイルを保存
    def csv(self):
        # 実行時刻の記録
        now = datetime.datetime.now()
        current_time = now.strftime('%Y-%m-%d-%H-%M')
        # 保存ファイル名を指定
        csv_path = tk.filedialog.asksaveasfilename(title='csvファイル保存先・ファイル名指定',
                                                   filetypes=[("CSV Files", ".csv")],
                                                   initialfile=f'pycorec_{current_time}')
        self.df.to_csv(f'{csv_path}.csv', encoding='utf-8')


# GUI
# インスタンスの作成
PyCorec = PyCorec()
# ウインドウの作成
root = tk.Tk()
# ウインドウのタイトル
root.title('pycorec1.0.7')
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
button = tk.Button(frame_menu, text='フォルダ選択(フォルダ内画像一括選択)', command=PyCorec.getdir)
button.grid(row=1, column=0, sticky=tk.W)
button = tk.Button(frame_menu, text='ファイル選択(連続範囲選択)', command=PyCorec.getrange)
button.grid(row=14, column=0, sticky=tk.W)
button = tk.Button(frame_menu, text='ファイル選択(複数・任意選択可能)', command=PyCorec.getfile)
button.grid(row=28, column=0, sticky=tk.W)
button_csv = tk.Button(frame_save, text='csvファイル保存', command=PyCorec.csv)
button_csv.grid(row=1, column=0, sticky=tk.W)
# button_png = tk.Button(frame_save, text='時系列座標グラフ保存', command=csv)
# button_png.grid(row=1, column=1, sticky=tk.W)

# イベントループ
root.mainloop()
