# ui/text_input_window.py

import tkinter as tk

def create_text_input_window(root, on_proceed_callback):
    # 清除根窗口中的所有小部件
    for widget in root.winfo_children():
        widget.destroy()
    
    # 创建文本输入小部件
    input_text = tk.Text(root, height=10, wrap="word", font=("Arial", 12))
    input_text.pack(expand=True, padx=20, pady=20)
    
    # 创建 "Proceed" 按钮
    proceed_button = tk.Button(root, text="Proceed", command=lambda: on_proceed_callback(input_text.get("1.0", "end").strip()))
    proceed_button.pack(pady=20)
