# ui/text_input_node.py
from PyQt5.QtWidgets import QTextEdit, QPushButton
from nodes.main_window import clear_layout

def create_text_input_node(layout, next_node=None, button_text=None):
    # 清除当前布局
    clear_layout(layout)

    # 创建文本框和按钮
    text_input = QTextEdit()
    next_button = QPushButton(button_text if button_text else "")

    # 添加组件到布局
    layout.addWidget(text_input)
    layout.addWidget(next_button)

    # 切换到下一个节点
    if next_node:
        next_button.clicked.connect(lambda: next_node(text_input.toPlainText()))
