# ui/text_display_node.py
from PyQt5.QtWidgets import QLabel, QPushButton
from nodes.main_window import clear_layout

def create_text_display_node(layout, text_content, next_node=None, button_text=None):
    # 清除当前布局
    clear_layout(layout)

    # 创建标签和按钮
    label = QLabel(f"You entered: {text_content}")
    back_button = QPushButton(button_text if button_text else "")

    # 添加组件到布局
    layout.addWidget(label)
    layout.addWidget(back_button)

    # 切换回文本输入节点
    if next_node:
        back_button.clicked.connect(next_node)
