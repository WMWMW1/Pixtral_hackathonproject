# ui/file_upload_window.py

import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES
import os

def create_file_upload_window(root, on_proceed_callback, remove_btn_text="Remove File", switch_btn_text="Proceed"):
    current_file_path = None

    def initialize_dnd():
        # 初始化拖放功能
        drop_area.drop_target_register(DND_FILES)
        drop_area.dnd_bind('<<Drop>>', on_drop)
    
    def upload_file(file_path=None):
        nonlocal current_file_path
        if file_path and file_path.endswith(".txt"):
            file_name = os.path.basename(file_path)
            drop_area.itemconfig(drop_text, text=f"File: {file_name}")
            current_file_path = file_path
            enable_buttons()
        else:
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if file_path:
                file_name = os.path.basename(file_path)
                drop_area.itemconfig(drop_text, text=f"File: {file_name}")
                current_file_path = file_path
                enable_buttons()
    
    def remove_file():
        nonlocal current_file_path
        drop_area.itemconfig(drop_text, text="Drag and Drop .txt File Here")
        current_file_path = None
        disable_buttons()
    
    def on_drop(event):
        file_path = event.data.strip("{}")
        if file_path.endswith(".txt"):
            upload_file(file_path)
        else:
            drop_area.itemconfig(drop_text, text="Only .txt files are allowed")
    
    def proceed_to_next_window():
        if current_file_path:
            # 您可以在此处处理文件
            on_proceed_callback()
    
    def enable_buttons():
        remove_button.config(state="normal")
        switch_button.config(state="normal")
    
    def disable_buttons():
        remove_button.config(state="disabled")
        switch_button.config(state="disabled")
    
    # 清除根窗口中的所有小部件
    for widget in root.winfo_children():
        widget.destroy()
    
    # 创建拖放区域
    drop_area = tk.Canvas(root, width=350, height=200, bg="#f0f0f0", bd=0, highlightthickness=0)
    drop_area.pack(expand=True, pady=20)
    
    # 创建圆角矩形
    create_rounded_rectangle(drop_area, 10, 10, 340, 190, radius=20, fill="#d3d3d3")
    drop_text = drop_area.create_text(175, 100, text="Drag and Drop .txt File Here", fill="black")
    
    # 创建 "Remove File" 按钮
    remove_button = tk.Button(root, text=remove_btn_text, command=remove_file, state="disabled")
    remove_button.pack()
    
    # 创建 "Proceed" 按钮
    switch_button = tk.Button(root, text=switch_btn_text, command=proceed_to_next_window, state="disabled")
    switch_button.pack()
    
    # 初始化拖放功能
    root.after(100, initialize_dnd)

# 定义在 Canvas 上创建圆角矩形的函数
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1+radius, y1,
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
        x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)
