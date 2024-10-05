import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import os

class FileUploadWindow:
    def __init__(self, root, next_window_callback=None, upload_btn_text="Upload File", remove_btn_text="Remove File", switch_btn_text="Proceed"):
        self.root = root
        self.upload_btn_text = upload_btn_text
        self.remove_btn_text = remove_btn_text
        self.switch_btn_text = switch_btn_text
        self.current_file_path = None
        self.next_window_callback = next_window_callback
        
        self.create_file_upload_window()

    def initialize_dnd(self):
        # 延迟初始化拖放功能
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_drop)

    def create_file_upload_window(self):
        # 创建 Canvas 作为背景
        self.drop_area = tk.Canvas(self.root, width=350, height=200, bg="#f0f0f0", bd=0, highlightthickness=0)
        self.drop_area.pack(expand=True, pady=20)
        
        # 创建圆角灰色区域
        self.create_rounded_rectangle(self.drop_area, 10, 10, 340, 190, radius=20, fill="#d3d3d3")
        
        # 在圆角框中显示文字
        self.drop_text = self.drop_area.create_text(175, 100, text="Drag and Drop .txt File Here", fill="black")

        # 移除文件按钮
        self.remove_button = tk.Button(self.root, text=self.remove_btn_text, command=self.remove_file, state="disabled")
        self.remove_button.pack()

        # 上传文件按钮
        self.upload_button = tk.Button(self.root, text=self.upload_btn_text, command=self.upload_file)
        self.upload_button.pack()

        # 切换到下一个窗口的按钮
        self.switch_button = tk.Button(self.root, text=self.switch_btn_text, command=self.proceed_to_next_window, state="disabled")
        self.switch_button.pack()

        # 延迟初始化拖放功能
        self.root.after(100, self.initialize_dnd)

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def upload_file(self, file_path=None):
        if file_path and file_path.endswith(".txt"):
            file_name = os.path.basename(file_path)
            self.drop_area.itemconfig(self.drop_text, text=f"File: {file_name}")
            self.current_file_path = file_path
            self.enable_buttons()
        else:
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if file_path:
                file_name = os.path.basename(file_path)
                self.drop_area.itemconfig(self.drop_text, text=f"File: {file_name}")
                self.current_file_path = file_path
                self.enable_buttons()

    def remove_file(self):
        self.drop_area.itemconfig(self.drop_text, text="Drag and Drop .txt File Here")
        self.current_file_path = None
        self.disable_buttons()

    def on_drop(self, event):
        file_path = event.data.strip("{}")  # Strip curly braces around file path if present
        if file_path.endswith(".txt"):
            self.upload_file(file_path)
        else:
            self.drop_area.itemconfig(self.drop_text, text="Only .txt files are allowed")

    def proceed_to_next_window(self):
        # 如果提供了下一个窗口的回调，则调用
        if self.next_window_callback:
            self.next_window_callback(self.current_file_path)

    def enable_buttons(self):
        self.remove_button.config(state="normal")
        self.switch_button.config(state="normal")

    def disable_buttons(self):
        self.remove_button.config(state="disabled")
        self.switch_button.config(state="disabled")


class TextOutputWindow:
    def __init__(self, root, text_content=""):
        self.root = root
        self.text_content = text_content
        self.create_text_output_window()

    def create_text_output_window(self):
        # 创建标签来显示文本内容
        label = tk.Label(self.root, text=self.text_content, wraplength=400, justify="left")
        label.pack(expand=True)


# 使用示例
def open_text_output_window(file_path):
    # 销毁现有窗口中的所有小部件
    for widget in root.winfo_children():
        widget.destroy()
    
    # 读取文件内容
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            content = f"Error reading file: {e}"
    else:
        content = "No file provided."
    
    # 创建 TextOutputWindow 实例
    TextOutputWindow(root, text_content=content)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("File Uploader with Drag and Drop")
    window_width = 500
    window_height = 400
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)
    
    # 创建文件上传窗口，定义下一窗口的回调
    upload_window = FileUploadWindow(root, next_window_callback=open_text_output_window,
                                     upload_btn_text="Select File", remove_btn_text="Remove", switch_btn_text="Proceed")

    root.mainloop()

