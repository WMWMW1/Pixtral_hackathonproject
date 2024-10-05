# ui/text_output_window.py

import tkinter as tk

def create_text_output_window(root, text_content):
    # 清除根窗口中的所有小部件
    for widget in root.winfo_children():
        widget.destroy()
    
    # 创建标签来显示文本内容
    label = tk.Label(root, text=text_content, wraplength=400, justify="left", font=("Arial", 12))
    label.pack(expand=True, padx=20, pady=20)
