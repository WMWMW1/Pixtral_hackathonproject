import tkinter as tk

def create_text_output_window(root, text_content=""):
    # 创建标签来显示文本内容
    label = tk.Label(root, text=text_content, wraplength=400, justify="left")
    label.pack(expand=True)
