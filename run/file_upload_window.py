import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES
from rounded_rectangle import create_rounded_rectangle
import os

def create_file_upload_window(root, on_process_content=None, remove_btn_text="Remove File", switch_btn_text="Proceed"):
    current_file_path = None

    def initialize_dnd():
        # 延迟初始化拖放功能
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
        file_path = event.data.strip("{}")  # Strip curly braces around file path if present
        if file_path.endswith(".txt"):
            upload_file(file_path)
        else:
            drop_area.itemconfig(drop_text, text="Only .txt files are allowed")

    def proceed_to_next_window():
        # 读取文件内容
        if current_file_path:
            try:
                with open(current_file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except Exception as e:
                content = f"Error reading file: {e}"

            # 调用可选的处理函数（如 LLM）
            if on_process_content:
                on_process_content(content)
            else:
                print("File content:")
                print(content)

    def enable_buttons():
        remove_button.config(state="normal")
        switch_button.config(state="normal")

    def disable_buttons():
        remove_button.config(state="disabled")
        switch_button.config(state="disabled")

    # 创建 Canvas 作为背景
    drop_area = tk.Canvas(root, width=350, height=200, bg="#f0f0f0", bd=0, highlightthickness=0)
    drop_area.pack(expand=True, pady=20)
    
    # 创建圆角灰色区域
    create_rounded_rectangle(drop_area, 10, 10, 340, 190, radius=20, fill="#d3d3d3")
    
    # 在圆角框中显示文字
    drop_text = drop_area.create_text(175, 100, text="Drag and Drop .txt File Here", fill="black")

    # 移除文件按钮
    remove_button = tk.Button(root, text=remove_btn_text, command=remove_file, state="disabled")
    remove_button.pack()

    # 切换到下一个窗口的按钮
    switch_button = tk.Button(root, text=switch_btn_text, command=proceed_to_next_window, state="disabled")
    switch_button.pack()

    # 延迟初始化拖放功能
    root.after(100, initialize_dnd)
