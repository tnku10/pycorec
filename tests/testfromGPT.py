import customtkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import ctypes


class ImageAnnotationApp:
    def __init__(self, image_paths):
        self.image_paths = image_paths
        self.current_image_index = 0
        self.coordinates = []
        self.zoom_level = 1.0
        self.offset_x = 0
        self.offset_y = 0

        self.root = tk.CTk()
        self.root.title("Image Annotation App")

        # ウィンドウをタスクバーを除いた領域にフィットさせる
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1) - user32.GetSystemMetrics(3)
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.attributes('-topmost', True)  # メインモニタの全画面サイズで起動する

        self.frame = tk.CTkFrame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.CTkCanvas(self.frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.CTkFrame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.coordinates_label = tk.CTkLabel(self.bottom_frame, text="Coordinates: (0, 0)")
        self.coordinates_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.filename_label = tk.CTkLabel(self.bottom_frame, text="Filename: ")
        self.filename_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.image_number_label = tk.CTkLabel(self.bottom_frame, text="Image Number: ")
        self.image_number_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.image_size_label = tk.CTkLabel(self.bottom_frame, text="Image Size: ")
        self.image_size_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_frame = tk.CTkFrame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.next_image_button = tk.CTkButton(self.button_frame, text="Next Image", command=self.next_image)
        self.next_image_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.previous_image_button = tk.CTkButton(self.button_frame, text="Previous Image", command=self.previous_image)
        self.previous_image_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.move_up_button = tk.CTkButton(self.button_frame, text="Move Up", command=lambda: self.move_image(0, -10))
        self.move_up_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.move_down_button = tk.CTkButton(self.button_frame, text="Move Down", command=lambda: self.move_image(0, 10))
        self.move_down_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.move_left_button = tk.CTkButton(self.button_frame, text="Move Left", command=lambda: self.move_image(-10, 0))
        self.move_left_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.move_right_button = tk.CTkButton(self.button_frame, text="Move Right", command=lambda: self.move_image(10, 0))
        self.move_right_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.fit_image_button = tk.CTkButton(self.button_frame, text="Fit Image", command=self.fit_image_to_window)
        self.fit_image_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Motion>", self.on_canvas_motion)
        self.canvas.configure(cursor="crosshair")

        self.root.bind("<Right>", self.next_image_keyboard)
        self.root.bind("<Left>", self.previous_image_keyboard)

        self.load_image()

    def load_image(self):
        image_path = self.image_paths[self.current_image_index]
        image = Image.open(image_path)
        self.resized_image = self.resize_image(image)
        self.photo_image = ImageTk.PhotoImage(self.resized_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        self.update_labels(image_path)

    def resize_image(self, image):
        width, height = image.size
        max_width = self.root.winfo_width()
        max_height = self.root.winfo_height()

        aspect_ratio = min(max_width / width, max_height / height)
        new_width = int(width * aspect_ratio * self.zoom_level)
        new_height = int(height * aspect_ratio * self.zoom_level)
        if new_width <= 0 or new_height <= 0:
            return image

        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        return resized_image

    def zoom_image(self, zoom_in):
        if zoom_in:
            self.zoom_level *= 1.1
        else:
            self.zoom_level /= 1.1

        self.canvas.delete("all")
        self.load_image()
        self.draw_coordinates()

    def fit_image_to_window(self):
        self.zoom_level = 1.0
        self.canvas.delete("all")
        self.load_image()
        self.draw_coordinates()

    def on_canvas_click(self, event):
        x = (event.x - self.offset_x) / self.zoom_level
        y = (event.y - self.offset_y) / self.zoom_level
        self.coordinates.append((x, y))
        self.draw_coordinates()

    def draw_coordinates(self):
        self.canvas.delete("coordinates")
        for coord in self.coordinates:
            x, y = coord
            x = x * self.zoom_level + self.offset_x
            y = y * self.zoom_level + self.offset_y
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red", outline="red", tags="coordinates")

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.zoom_image(True)
        else:
            self.zoom_image(False)

    def next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        self.coordinates = []
        self.canvas.delete("all")
        self.load_image()

    def previous_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
        self.coordinates = []
        self.canvas.delete("all")
        self.load_image()

    def update_coordinates_label(self, x, y):
        self.coordinates_label.configure(text=f"Coordinates: ({x}, {y})")

    def update_labels(self, image_path):
        image_number = self.current_image_index + 1
        image_total = len(self.image_paths)
        image_size = f"{self.resized_image.width} x {self.resized_image.height}"
        self.filename_label.configure(text=f"Filename: {image_path.name}")
        self.image_number_label.configure(text=f"Image Number: {image_number}/{image_total}")
        self.image_size_label.configure(text=f"Image Size: {image_size}")

    def move_image(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy
        self.canvas.delete("all")
        self.load_image()
        self.draw_coordinates()

    def on_canvas_motion(self, event):
        x = (event.x - self.offset_x) / self.zoom_level
        y = (event.y - self.offset_y) / self.zoom_level
        self.update_coordinates_label(x, y)

    def next_image_keyboard(self, event):
        self.next_image()

    def previous_image_keyboard(self, event):
        self.previous_image()


if __name__ == "__main__":
    image_dir = Path("./")
    image_paths = list(image_dir.glob("*.jpg"))
    app = ImageAnnotationApp(image_paths)
    app.root.mainloop()
