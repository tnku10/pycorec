from concurrent.futures import ThreadPoolExecutor, as_completed  # system included
import datetime  # system included
from pathlib import Path  # system included
import threading  # system included
from typing import Callable  # system included
from typing import Union  # system included
import customtkinter  # pip install customtkinter
import cv2  # pip install opencv-python
from natsort import natsorted  # pip install natsort
import numpy as np  # pip install numpy
import pandas as pd  # pip install pandas
from PIL import Image, ImageTk  # pip install pillow
from styleframe import StyleFrame, Styler  # pip install styleframe

pycorec_version = '2.0.9'


class PyCorec:
    def __init__(self):
        super().__init__()
        self.first_run = True
        self.magnification = 1
        self.photo_image = None
        self.resized_image = None
        self.image_file_name = None
        self.image_height = 1
        self.image_width = 1
        self.resized_image_height = 1
        self.resized_image_width = 1
        self.cm_per_px_x = None
        self.cm_per_px_y = None
        self.fps = None
        self.interval = 1
        self.image_paths = []
        self.current_image_index = 0
        self.coordinates = []
        self.pos = []
        self.file_list = []
        self.zoom_level = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.is_fullscreen = False

        # create window
        self.root = customtkinter.CTk()
        self.root.title(f'PyCorec {pycorec_version}')
        customtkinter.set_appearance_mode('Dark')

        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        win_w = int(screen_w)
        win_h = int(screen_h * 0.95)
        self.root.geometry(f"{win_w}x{win_h}+0+0")

        # frames
        self.frame = customtkinter.CTkFrame(self.root)
        self.frame.pack(fill=customtkinter.BOTH, expand=True)

        self.image_frame = customtkinter.CTkFrame(self.frame)
        self.image_frame.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True)

        self.canvas = customtkinter.CTkCanvas(self.image_frame, bg='white')
        self.canvas.pack(fill=customtkinter.BOTH, expand=True)

        self.bottom_frame = customtkinter.CTkFrame(self.root)
        self.bottom_frame.pack(side=customtkinter.BOTTOM, fill=customtkinter.X)

        self.label_frame = customtkinter.CTkFrame(self.bottom_frame)
        self.label_frame.pack(side=customtkinter.LEFT, fill=customtkinter.X, padx=10, pady=10)

        # labels
        self.coordinates_label = customtkinter.CTkLabel(self.label_frame, text='Coordinates (px): (0, 0)')
        self.coordinates_label.pack(side=customtkinter.LEFT)

        self.records_label = customtkinter.CTkLabel(self.label_frame, text='Record Points: 0')
        self.records_label.pack(side=customtkinter.LEFT, padx=10)

        self.image_index_label = customtkinter.CTkLabel(self.label_frame, text='[ 0 / 0 ]')
        self.image_index_label.pack(side=customtkinter.LEFT, padx=10)

        self.frame_interval_label = customtkinter.CTkLabel(self.label_frame, text='Frame Interval: 1')
        self.frame_interval_label.pack(side=customtkinter.LEFT, padx=10)

        self.image_size_label = customtkinter.CTkLabel(self.label_frame, text='Image Size: ')
        self.image_size_label.pack(side=customtkinter.LEFT, padx=10)

        self.resized_image_size_label = customtkinter.CTkLabel(self.label_frame, text='Displayed Image Size: ')
        self.resized_image_size_label.pack(side=customtkinter.LEFT, padx=10)

        self.image_magnification_label = customtkinter.CTkLabel(self.label_frame, text='Image Magnification (%): ')
        self.image_magnification_label.pack(side=customtkinter.LEFT, padx=10)

        self.fps_label = customtkinter.CTkLabel(self.label_frame, text='fps: ')
        self.fps_label.pack(side=customtkinter.LEFT, padx=10)

        self.cm_per_px_x_label = customtkinter.CTkLabel(self.label_frame, text='cm/px (x): ')
        self.cm_per_px_x_label.pack(side=customtkinter.LEFT, padx=10)

        self.cm_per_px_y_label = customtkinter.CTkLabel(self.label_frame, text='cm/px (y): ')
        self.cm_per_px_y_label.pack(side=customtkinter.LEFT, padx=10)

        self.previous_image_button = customtkinter.CTkButton(
            self.label_frame, text='◀', width=10, command=self.previous_image
        )
        self.previous_image_button.pack(side=customtkinter.LEFT, padx=5)

        self.next_image_button = customtkinter.CTkButton(
            self.label_frame, text='▶', width=10, command=self.next_image
        )
        self.next_image_button.pack(side=customtkinter.LEFT, padx=5)

        #  buttons
        self.button_frame = customtkinter.CTkFrame(self.frame)
        self.button_frame.pack(side=customtkinter.RIGHT, fill=customtkinter.Y, padx=10, pady=10)

        self.blank_button = customtkinter.CTkButton(
            self.button_frame, text='Open Images by', fg_color='transparent', hover=False
        )
        self.blank_button.pack(fill=customtkinter.X, padx=10, pady=10)

        self.open_image_mov_button = customtkinter.CTkButton(
            self.button_frame, text='Video Capture', command=self.get_mov
        )
        self.open_image_mov_button.pack(fill=customtkinter.X, padx=10, pady=10)

        self.open_image_dir_button = customtkinter.CTkButton(
            self.button_frame, text='Directory Selection', command=self.get_dir
        )
        self.open_image_dir_button.pack(fill=customtkinter.X, padx=10, pady=10)

        self.open_image_range_button = customtkinter.CTkButton(
            self.button_frame, text='Bounded Selection', command=self.get_range
        )
        self.open_image_range_button.pack(fill=customtkinter.X, padx=10, pady=10)

        self.open_image_click_button = customtkinter.CTkButton(
            self.button_frame, text='Click Selection', command=self.get_files
        )
        self.open_image_click_button.pack(fill=customtkinter.X, padx=10, pady=10)

        self.blank_button = customtkinter.CTkButton(
            self.button_frame, text='', fg_color='transparent', hover=False
        )
        self.blank_button.pack(fill=customtkinter.X, padx=10, pady=5)

        self.blank_button = customtkinter.CTkButton(
            self.button_frame, text='Move Image', fg_color='transparent', hover=False
        )
        self.blank_button.pack(fill=customtkinter.X, padx=10, pady=0)

        self.move_button = ArrowButton(self.button_frame, command=self.move_image)
        self.move_button.pack(fill=customtkinter.X, padx=70, pady=10)

        self.blank_button = customtkinter.CTkButton(
            self.button_frame, text='Image Magnification (%)', fg_color='transparent', hover=False
        )
        self.blank_button.pack(fill=customtkinter.X, padx=10, pady=10)

        self.zoom_spinbox = FloatSpinbox(self.button_frame, width=150, step_size=3)
        self.zoom_spinbox.pack(fill=customtkinter.X, padx=10, pady=0)

        self.zoom_in_button = customtkinter.CTkButton(
            self.button_frame, text='Apply', command=self.zoom_image
        )
        self.zoom_in_button.pack(fill=customtkinter.X, padx=10, pady=5)

        self.fit_image_to_window_button = customtkinter.CTkButton(
            self.button_frame, text='Reset to Window Size', command=self.fit_image_to_window
        )
        self.fit_image_to_window_button.pack(fill=customtkinter.X, padx=10, pady=10)

        self.fit_image_to_actual_size_button = customtkinter.CTkButton(
            self.button_frame, text='Actual Size', command=self.fit_image_to_actual_size
        )
        self.fit_image_to_actual_size_button.pack(fill=customtkinter.X, padx=10, pady=5)

        self.fullscreen_button = customtkinter.CTkButton(
            self.button_frame,
            text='Toggle Fullscreen (F11)',
            command=self.toggle_fullscreen
        )
        self.fullscreen_button.pack(fill=customtkinter.X, padx=10, pady=5)

        self.blank_button = customtkinter.CTkButton(
            self.button_frame, text='', fg_color='transparent', hover=False
        )
        self.blank_button.pack(fill=customtkinter.X, padx=10, pady=10)

        self.save_file_button = customtkinter.CTkButton(
            self.button_frame, text='Save as...', command=self.save_file
        )
        self.save_file_button.pack(fill=customtkinter.X, padx=10, pady=5)

        self.resume_recording_button = customtkinter.CTkButton(
            self.button_frame, text='Resume Recording', command=self.resume_recording
        )
        self.resume_recording_button.pack(fill=customtkinter.X, padx=10, pady=5)

        #  canvas
        self.canvas.bind('<Button-1>', self.on_canvas_left_click)
        self.canvas.bind('<Button-3>', self.on_canvas_right_click)
        self.canvas.bind('<Button-2>', self.on_canvas_wheel_click)
        self.canvas.bind('<Motion>', self.on_canvas_motion)
        self.canvas.configure(cursor='crosshair')

        self.root.bind('<Right>', self.next_image_keyboard)
        self.root.bind('<Left>', self.previous_image_keyboard)

        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())

    def configure_optional_parameter(self, fps_config=True):
        if fps_config:
            fps_dialog = customtkinter.CTkInputDialog(
                text='Input\n'
                     ' fps (Optional):\n'
                     '\n'
                     'If you want to add a time column to the output file, '
                     'enter a value of fps.\n'
                     '\n'
                     'To proceed without entering values, '
                     'press the Ok button.',
                title='fps (Optional)'
            )
            fps_input = fps_dialog.get_input()
            if fps_input is None or fps_input == '':
                self.fps = None
            else:
                self.fps = float(fps_input)
            self.fps_label.configure(text=f'fps: {self.fps}')

        cm_per_px_x_dialog = customtkinter.CTkInputDialog(
            text='Input\n'
                 'x cm/px (Optional):\n'
                 '\n'
                 'If you want to add physical coordinates (cm) converted '
                 'from image coordinates (px) to the output file, '
                 'enter a value of x-axis direction cm/px.\n'
                 '\n'
                 'To proceed without entering values, '
                 'press the Ok button.',
            title='x cm/px (Optional)'
        )
        cm_x_input = cm_per_px_x_dialog.get_input()
        if cm_x_input is None or cm_x_input == '':
            self.cm_per_px_x = None
        else:
            self.cm_per_px_x = float(cm_x_input)
        self.cm_per_px_x_label.configure(text=f'cm/px (x): {self.cm_per_px_x}')

        cm_per_px_y_dialog = customtkinter.CTkInputDialog(
            text='Input\n'
                 'y cm/px (Optional):\n'
                 '\n'
                 'If you want to add physical coordinates (cm) converted '
                 'from image coordinates (px) to the output file, '
                 'enter a value of y-axis direction cm/px.\n'
                 '\n'
                 'To proceed without entering values, '
                 'press the Ok button.',
            title='y cm/px (Optional)'
        )
        cm_y_input = cm_per_px_y_dialog.get_input()
        if cm_y_input is None or cm_y_input == '':
            self.cm_per_px_y = None
        else:
            self.cm_per_px_y = float(cm_y_input)
        self.cm_per_px_y_label.configure(text=f'cm/px (y): {self.cm_per_px_y}')

    def get_mov(self):
        file_type = [('Supported Files', '*.mp4 *.MP4 *.avi *.AVI')]
        video_path = customtkinter.filedialog.askopenfilename(title='Open Video File', filetypes=file_type)

        if video_path != '':
            progress_bar = customtkinter.CTkProgressBar(
                master=self.label_frame, orientation='horizontal', mode='indeterminate'
            )
            progress_bar.pack(side=customtkinter.RIGHT)
            thread = threading.Thread(target=self.process_video2frames, args=(video_path, progress_bar))
            thread.start()

    def process_video2frames(self, video_path, progress_bar):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return
        video_dir_path = Path(Path(video_path).parent, Path(video_path).stem)
        video_dir_path.mkdir(parents=True, exist_ok=True)
        base_path = Path(video_dir_path, Path(video_path).stem)

        digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        n = 0
        progress_bar.start()

        with ThreadPoolExecutor() as executor:
            futures = []
            while True:
                ret, frame = cap.read()
                if ret:
                    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    future = executor.submit(pil_image.save, f'{base_path}_{str(n).zfill(digit)}.jpg')
                    futures.append(future)
                    n += 1
                else:
                    break

            for _ in as_completed(futures):
                pass

        progress_bar.stop()
        progress_bar.destroy()
        cap.release()
        self.get_frames(video_dir_path, video_fps, frame_count)

    def get_frames(self, video_dir_path, video_fps, frame_count):
        exts = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}
        image_paths = natsorted(
            [p for p in video_dir_path.glob('**/*') if p.suffix.lower() in exts]
        )

        if len(image_paths) != 0:
            interval_dialog = customtkinter.CTkInputDialog(
                text='Input\n'
                     'Frame Interval:\n'
                     '\n'
                     'Examples\n'
                     '1: Load all frames (001.jpg, 002.jpg, 003.jpg, ...)\n'
                     '2: Load frames every one frame (001,003,005,...)\n'
                     '3: Load frames every two frames (001,004,007,...)\n'
                     '\n'
                     f'Loaded Video:\n'
                     f'{video_fps} fps, {frame_count} frames\n'
                     '\n'
                     f'Result of applying interval:\n'
                     f'{video_fps} / (Frame Interval) fps\n'
                     f'{frame_count} / (Frame Interval) frames\n',
                title='Frame Interval'
            )
            interval_str = interval_dialog.get_input()
            self.interval = int(interval_str)
            self.frame_interval_label.configure(text=f'Frame Interval: {self.interval}')
            self.fps = video_fps / self.interval
            self.fps_label.configure(text=f'fps: {self.fps}')
            self.image_paths = image_paths[::self.interval]
            self.current_image_index = 0
            self.offset_x = 0
            self.offset_y = 0
            self.first_run = True
            self.coordinates = []
            self.pos = []
            self.file_list = []
            self.configure_optional_parameter(fps_config=False)
            self.load_image()

    def get_dir(self):
        dir_path = customtkinter.filedialog.askdirectory(
            title='Open Images from Directory ( jpg, png, tif, bmp )'
        )
        path = Path(dir_path)
        exts = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}
        image_paths = natsorted(
            [p for p in path.glob('**/*')
             if "Bkg" not in str(p) and "Sub" not in str(p)
             and p.suffix.lower() in exts]
        )
        if len(image_paths) != 0:
            interval_dialog = customtkinter.CTkInputDialog(
                text='Input\n'
                     'Frame Interval:\n'
                     '\n'
                     'Examples\n'
                     '1: Load all frames (001.jpg, 002.jpg, 003.jpg, ...)\n'
                     '2: Load frames every one frame (001,003,005,...)\n'
                     '3: Load frames every two frames (001,004,007,...)\n',
                title='Frame Interval'
            )
            interval_str = interval_dialog.get_input()
            self.interval = int(interval_str)
            self.frame_interval_label.configure(text=f'Frame Interval: {self.interval}')
            self.image_paths = image_paths[::self.interval]
            self.current_image_index = 0
            self.offset_x = 0
            self.offset_y = 0
            self.first_run = True
            self.coordinates = []
            self.pos = []
            self.file_list = []
            self.configure_optional_parameter()
            self.load_image()

    def get_range(self):
        file_type = [('Supported Files', '*.jpg *.JPG *.jpeg *.png *.PNG *.bmp *.BMP *.tif')]
        image_paths = customtkinter.filedialog.askopenfilenames(
            title='Open Images by Bounded Selection', filetypes=file_type
        )
        image_paths = natsorted(image_paths)
        if len(image_paths) != 0:
            interval_dialog = customtkinter.CTkInputDialog(
                text='Input\n'
                     'Frame Interval:\n'
                     '\n'
                     'Examples\n'
                     '1: Load all frames (001.jpg, 002.jpg, 003.jpg, ...)\n'
                     '2: Load frames every one frame (001,003,005,...)\n'
                     '3: Load frames every two frames (001,004,007,...)\n',
                title='Frame Interval'
            )
            interval_str = interval_dialog.get_input()
            self.interval = int(interval_str)
            self.frame_interval_label.configure(text=f'Frame Interval: {self.interval}')
            self.image_paths = image_paths[::self.interval]
            self.current_image_index = 0
            self.offset_x = 0
            self.offset_y = 0
            self.first_run = True
            self.coordinates = []
            self.pos = []
            self.file_list = []
            self.configure_optional_parameter()
            self.load_image()

    def get_files(self):
        file_type = [('Supported Files', '*.jpg *.JPG *.jpeg *.png *.PNG *.bmp *.BMP *.tif')]
        image_paths = customtkinter.filedialog.askopenfilenames(
            title='Open Image(s) by Click', filetypes=file_type
        )
        if len(image_paths) != 0:
            self.image_paths = natsorted(image_paths)
            self.current_image_index = 0
            self.offset_x = 0
            self.offset_y = 0
            self.first_run = True
            self.coordinates = []
            self.pos = []
            self.file_list = []
            self.configure_optional_parameter()
            self.load_image()

    def load_image(self, fit_image=False):
        image_path = self.image_paths[self.current_image_index]
        image = Image.open(image_path)
        self.image_file_name = Path(image_path).name
        self.image_width, self.image_height = image.size
        self.image_size_label.configure(text=f'Image Size: {self.image_width} x {self.image_height}')
        self.resized_image = self.resize_image(image, fit_image)
        self.photo_image = ImageTk.PhotoImage(self.resized_image)
        self.canvas.delete('all')
        self.canvas.create_image(
            0 + self.offset_x, 0 + self.offset_y,
            anchor=customtkinter.NW,
            image=self.photo_image
        )
        self.update_labels(image_path)

    def resize_image(self, image, fit_image=False):
        image_width, image_height = image.size

        self.root.update_idletasks()
        win_width = self.image_frame.winfo_width()
        win_height = self.image_frame.winfo_height()
        if win_width <= 0 or win_height <= 0:
            win_width = self.root.winfo_width()
            win_height = self.root.winfo_height()

        win_fit_magnification_ratio = min(win_width / image_width, win_height / image_height)
        if self.first_run:
            self.zoom_level = win_fit_magnification_ratio
            self.first_run = False
        if fit_image:
            self.zoom_level = win_fit_magnification_ratio

        new_width = int(image_width * self.zoom_level)
        new_height = int(image_height * self.zoom_level)
        if new_width <= 0 or new_height <= 0:
            return image
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        self.resized_image_width = resized_image.width
        self.resized_image_height = resized_image.height
        self.magnification = self.resized_image_width / self.image_width
        return resized_image

    def zoom_image(self):
        zoom_value = self.zoom_spinbox.get()
        if zoom_value is None:
            return
        self.zoom_level = zoom_value * 0.01
        self.canvas.delete('all')
        self.load_image()
        self.draw_coordinates()

    def fit_image_to_window(self):
        fit_image = True
        self.offset_x = 0
        self.offset_y = 0
        self.canvas.delete('all')
        self.load_image(fit_image)
        self.draw_coordinates()

    def fit_image_to_actual_size(self):
        self.zoom_level = 1.0
        self.canvas.delete('all')
        self.load_image()
        self.draw_coordinates()

    def move_image(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy
        self.canvas.delete('all')
        self.load_image()
        self.draw_coordinates()

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        if not self.is_fullscreen:
            self.root.state('zoomed')

    def next_image_keyboard(self, _):
        self.next_image()

    def previous_image_keyboard(self, _):
        self.previous_image()

    def on_canvas_motion(self, event):
        x = (event.x - self.offset_x) / self.magnification
        y = (event.y - self.offset_y) / self.magnification
        self.update_coordinates_label(round(x), round(y))

    def on_canvas_left_click(self, event):
        if self.image_file_name is not None:
            x = (event.x - self.offset_x) / self.magnification
            y = (event.y - self.offset_y) / self.magnification
            x_int = int(round(x))
            y_int = int(round(y))
            self.coordinates.append((x_int, y_int))
            self.draw_coordinates()

    def on_canvas_right_click(self, _):
        if self.image_file_name is not None:
            if len(self.coordinates) != 0:
                del self.coordinates[-1]
                self.draw_coordinates()

    def on_canvas_wheel_click(self, _):
        if self.image_file_name is not None:
            x = float('nan')
            y = float('nan')
            self.coordinates.append((x, y))
            self.draw_coordinates()

    def draw_coordinates(self):
        self.canvas.delete('coordinates')
        for coord in self.coordinates:
            x, y = coord
            x = x * self.magnification + self.offset_x
            y = y * self.magnification + self.offset_y
            self.canvas.create_oval(
                x - 2, y - 2, x + 2, y + 2, fill='red', outline='red', tags='coordinates'
            )
        record_points_number = len(self.coordinates)
        self.update_records_label(record_points_number)

    def record_coordinates(self):
        if len(self.pos) != self.current_image_index:
            self.pos[self.current_image_index] = self.coordinates
            self.file_list[self.current_image_index] = self.image_file_name
        if len(self.pos) == self.current_image_index:
            self.pos.insert(self.current_image_index, self.coordinates)
            self.file_list.insert(self.current_image_index, self.image_file_name)

    def next_image(self):
        if self.current_image_index + 1 == len(self.image_paths):
            self.save_file()
        if self.current_image_index + 1 < len(self.image_paths):
            self.record_coordinates()
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
            self.canvas.delete('all')
            self.load_image()
            if len(self.pos) != self.current_image_index:
                self.coordinates = self.pos[self.current_image_index]
                self.draw_coordinates()
            if len(self.pos) == self.current_image_index:
                self.coordinates = []
                self.draw_coordinates()

    def previous_image(self):
        if self.current_image_index != 0:
            if self.current_image_index + 1 == len(self.image_paths):
                self.record_coordinates()
            self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
            self.coordinates = self.pos[self.current_image_index]
            self.canvas.delete('all')
            self.load_image()
            self.draw_coordinates()

    def update_coordinates_label(self, x, y):
        self.coordinates_label.configure(text=f'Coordinates (px): ({x}, {y})')

    def update_records_label(self, record_points_number):
        self.records_label.configure(text=f'Record Points: {record_points_number}')

    def update_labels(self, image_path):
        index = self.current_image_index + 1
        total = len(self.image_paths)
        filename = Path(image_path).name

        self.root.title(
            f'PyCorec {pycorec_version}      [ {index} / {total} ]  {filename}'
        )

        self.image_index_label.configure(
            text=f'[ {index} / {total} ]  {filename}'
        )

        self.resized_image_size_label.configure(
            text=f'Resized Image Size: {self.resized_image.width} x {self.resized_image.height}'
        )
        image_magnification = (self.resized_image.width / self.image_width) * 100
        self.image_magnification_label.configure(
            text=f'Image Magnification (%): {image_magnification:.1f}'
        )
        self.zoom_spinbox.set(round(image_magnification, 1))

    def save_file(self):
        self.record_coordinates()
        now = datetime.datetime.now()
        current_time = now.strftime('%Y-%m-%d-%H-%M-%S')
        save_path = customtkinter.filedialog.asksaveasfilename(
            title='Save Coordinates File (Excel Book or CSV)',
            filetypes=[('Excel Book', '.xlsx'), ('CSV', '.csv')],
            initialfile=f'PyCorec{pycorec_version}_{current_time}',
            defaultextension='.xlsx'
        )

        if not save_path:
            return

        # Time Series by Points
        df = pd.DataFrame({'Filename': self.file_list})
        df_path = pd.DataFrame({'Filepath': self.image_paths})

        if self.fps is not None:
            timestep = 1 / self.fps
            df['Time_s'] = df.index * timestep

        flat_pos = [[tpl for sublist in row for tpl in sublist] for row in self.pos]
        flat_pos_row_length = max([len(row) for row in flat_pos])

        flat_pos_np = np.array(
            [
                np.pad(
                    np.asarray(i, dtype=float),
                    (0, flat_pos_row_length - len(i)),
                    mode='constant',
                    constant_values=np.nan
                )
                for i in flat_pos
            ],
            dtype=float
        )
        columns = flat_pos_np.T

        for i in range(flat_pos_row_length // 2):
            df[f'x{i + 1}_px'] = columns[i * 2]
            df[f'y{i + 1}_px'] = columns[i * 2 + 1]

        df['xm_px'] = self.image_width
        df['ym_px'] = self.image_height

        if (self.cm_per_px_x is not None) and (self.cm_per_px_y is not None):
            for i in range(flat_pos_row_length // 2):
                df[f'x{i + 1}_cm'] = df[f'x{i + 1}_px'] * self.cm_per_px_x
                df[f'y{i + 1}_cm'] = df[f'y{i + 1}_px'] * self.cm_per_px_y * -1

            df['xm_cm'] = self.image_width * self.cm_per_px_x
            df['ym_cm'] = self.image_height * self.cm_per_px_y * -1
            df['cm_px_x'] = self.cm_per_px_x
            df['cm_px_y'] = self.cm_per_px_y

        df['zoom'] = self.zoom_level
        df['offset_x'] = self.offset_x
        df['offset_y'] = self.offset_y
        df['software'] = f'PyCorec{pycorec_version}'
        df['datetime'] = current_time

        df = pd.concat([df_path, df], axis=1)

        # Spatial Distribution per Frame
        tidy_df = pd.DataFrame()
        tidy_pos = np.array([tpl for sublist in self.pos for tpl in sublist], dtype=float)
        tidy_pos_np = np.array(tidy_pos, dtype=float)
        tidy_columns = tidy_pos_np.T
        record_point_counts = [len(row) for row in self.pos]
        filename_col_list = []
        point_index_col_list = []

        for i in range(len(self.file_list)):
            for j in range(1, record_point_counts[i] + 1):
                filename_col_list.append(self.file_list[i])
                point_index_col_list.append(j)

        tidy_df['Filename'] = filename_col_list
        if self.fps is not None:
            timestep = 1 / self.fps
            end = 0 + (len(self.image_paths) - 1) * timestep
            sec_list = [0 + i * timestep for i in range(int((end - 0) / timestep) + 1)]
            sec_col_list = []
            for i in range(len(self.file_list)):
                for j in range(1, record_point_counts[i] + 1):
                    sec_col_list.append(sec_list[i])
            tidy_df['Time_s'] = sec_col_list
        tidy_df['Point Index'] = point_index_col_list
        tidy_df['x_px'] = tidy_columns[0]
        tidy_df['y_px'] = tidy_columns[1]

        if (self.cm_per_px_x is not None) and (self.cm_per_px_y is not None):
            tidy_df['x_cm'] = tidy_df['x_px'] * self.cm_per_px_x
            tidy_df['y_cm'] = tidy_df['y_px'] * self.cm_per_px_y * -1

        if save_path.endswith('.xlsx'):
            sf: StyleFrame = StyleFrame(df)
            sf.apply_headers_style(
                Styler(font='Segoe UI', border_type={'bottom': 'medium', 'right': 'dotted', 'left': 'dotted'})
            )

            sf.apply_column_style(
                cols_to_style=sf.columns,
                styler_obj=Styler(
                    font='Segoe UI', wrap_text=False, shrink_to_fit=False, border_type='dotted'
                )
            )

            sf_tidy: StyleFrame = StyleFrame(tidy_df)
            sf_tidy.apply_headers_style(
                Styler(font='Segoe UI', border_type={'bottom': 'medium', 'right': 'dotted', 'left': 'dotted'})
            )
            sf_tidy.apply_column_style(
                cols_to_style=sf_tidy.columns,
                styler_obj=Styler(
                    font='Segoe UI', wrap_text=False, shrink_to_fit=False, border_type='dotted'
                )
            )

            with pd.ExcelWriter(save_path) as writer:
                sf.to_excel(writer, sheet_name='Time Series by Points')
                sf_tidy.to_excel(writer, sheet_name='Spatial Distribution per Frame')

        if save_path.endswith('.csv'):
            df.to_csv(save_path, index=False)

    def resume_recording(self):
        file_type = [('Supported Files', '*.xlsx *.csv')]
        recordings_path = customtkinter.filedialog.askopenfilename(
            title='Open Coordinates Recording File', filetypes=file_type
        )
        df = pd.DataFrame()

        if len(recordings_path) != 0:
            if recordings_path.endswith('.xlsx'):
                df = pd.read_excel(recordings_path, sheet_name=0)
            if recordings_path.endswith('.csv'):
                df = pd.read_csv(recordings_path)

            self.image_paths = df['Filepath'].tolist()
            file_list = df['Filename'].tolist()
            self.file_list = [item for item in file_list if isinstance(item, str)]
            self.pos = []
            self.zoom_level = df['zoom'][0]
            self.offset_x = df['offset_x'][0]
            self.offset_y = df['offset_y'][0]

            for i in range(len(self.file_list)):
                pos_list = []
                for j in range(1, 300):
                    if f'x{j}_px' in df.columns:
                        pos_list.append((df[f'x{j}_px'][i], df[f'y{j}_px'][i]))
                    else:
                        break
                self.pos.append(pos_list)

            self.frame_interval_label.configure(text=f'Frame Interval:')

            if 'Time_s' in df.columns and len(df) > 1:
                self.fps = 1 / (df['Time_s'][1] - df['Time_s'][0])
                self.fps_label.configure(text=f'fps: {self.fps}')

            if 'x1_cm' in df.columns:
                self.cm_per_px_x = df['cm_px_x'][0]
                self.cm_per_px_y = df['cm_px_y'][0]
                self.cm_per_px_x_label.configure(text=f'cm/px (x): {self.cm_per_px_x}')
                self.cm_per_px_y_label.configure(text=f'cm/px (y): {self.cm_per_px_y}')

            self.current_image_index = len(self.file_list) - 1
            self.canvas.delete('all')
            self.load_image()
            self.coordinates = self.pos[self.current_image_index]
            try:
                if np.isnan(self.coordinates).all():  # type: ignore[arg-type]
                    self.coordinates = []
            except TypeError:
                pass
            self.draw_coordinates()
            self.update_labels(self.image_paths[self.current_image_index])


class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=('gray78', 'gray28'))

        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.subtract_button = customtkinter.CTkButton(
            self, text='-', width=height - 6, height=height - 6,
            command=self.subtract_button_callback
        )
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(
            self, width=width - (2 * height), height=height - 6, border_width=0
        )
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky='ew')

        self.add_button = customtkinter.CTkButton(
            self, text='+', width=height - 6, height=height - 6,
            command=self.add_button_callback
        )
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.entry.insert(0, '')

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, 'end')
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            self.entry.delete(0, 'end')
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, 'end')
        self.entry.insert(0, str(float(value)))


class ArrowButton(customtkinter.CTkFrame):
    def __init__(self, *args,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.command = command

        self.configure(fg_color='#333333')

        self.up_button = customtkinter.CTkButton(
            self, text='↑', height=20, width=20,
            command=self.up_button_callback
        )
        self.up_button.grid(row=0, column=1, padx=1, pady=1)

        self.down_button = customtkinter.CTkButton(
            self, text='↓', height=20, width=20,
            command=self.down_button_callback
        )
        self.down_button.grid(row=2, column=1, padx=1, pady=1)

        self.left_button = customtkinter.CTkButton(
            self, text='←', height=20, width=20,
            command=self.left_button_callback
        )
        self.left_button.grid(row=1, column=0, padx=1, pady=1)

        self.right_button = customtkinter.CTkButton(
            self, text='→', height=20, width=20,
            command=self.right_button_callback
        )
        self.right_button.grid(row=1, column=2, padx=1, pady=1)

    def up_button_callback(self):
        if self.command is not None:
            self.command(dx=0, dy=-10)
            return

    def down_button_callback(self):
        if self.command is not None:
            self.command(dx=0, dy=10)
            return

    def left_button_callback(self):
        if self.command is not None:
            self.command(dx=-10, dy=0)
            return

    def right_button_callback(self):
        if self.command is not None:
            self.command(dx=10, dy=0)
            return


def main():
    app2 = PyCorec()
    app2.root.mainloop()


if __name__ == '__main__':
    app = PyCorec()
    app.root.mainloop()
