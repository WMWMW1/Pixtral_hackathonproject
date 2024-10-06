# nodes/file_upload_node.py

from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt
from nodes.main_window import clear_layout
from util import make_drop_area

def create_file_upload_node(layout, next_node=None, button_text=None):
    """
    创建文件上传节点，允许用户通过拖拽文件，并包含一个可自定义的按钮。

    :param layout: 主布局，用于添加文件上传界面。
    :param next_node: 点击自定义按钮后的回调函数。
    :param button_text: 自定义按钮上的文本，可以不定义。
    """
    # 清除当前布局
    clear_layout(layout)

    # 创建文件拖放区域
    file_drop_area = QWidget()
    selected_file = {"path": None}

    # 定义当文件被拖入后的操作
    def on_file_dropped(file_path):
        selected_file["path"] = file_path
        custom_button.setEnabled(True)

    # 设置文件拖放区域
    make_drop_area(file_drop_area, on_file_dropped)

    # 创建自定义按钮
    custom_button = QPushButton(button_text if button_text else "")
    custom_button.setEnabled(False)  # 初始时禁用，直到用户选择了文件

    # 定义点击自定义按钮的函数
    def proceed():
        # 调用回调函数，传递选中的文件路径
        if next_node:
            next_node(selected_file["path"])

    # 连接按钮的点击事件
    custom_button.clicked.connect(proceed)

    # 创建布局并添加组件
    vbox = QVBoxLayout()
    vbox.addWidget(file_drop_area, alignment=Qt.AlignCenter)
    vbox.addWidget(custom_button, alignment=Qt.AlignCenter)

    # 将布局添加到主布局
    layout.addLayout(vbox)
