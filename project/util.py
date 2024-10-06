# util.py

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QWidget

def make_drop_area(widget, on_file_dropped):
    """
    将拖放功能添加到指定的 QWidget 上。

    :param widget: 要添加拖放功能的 QWidget 对象。
    :param on_file_dropped: 当文件被拖入后调用的回调函数，传递文件路径。
    """
    widget.setAcceptDrops(True)
    widget.file_path = None
    widget.text = "Drag and drop a file here"

    def paintEvent(event):
        painter = QPainter(widget)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = widget.rect()

        # 绘制背景
        painter.fillRect(rect, QBrush(QColor("#f0f0f0")))

        # 绘制圆角矩形边框
        pen = QPen(QColor("#aaa"), 2, Qt.DashLine)
        painter.setPen(pen)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 15, 15)

        # 绘制文本
        painter.setPen(QColor("#555"))
        painter.drawText(rect, Qt.AlignCenter, widget.text)

    def dragEnterEvent(event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                widget.file_path = urls[0].toLocalFile()
                # 调用回调函数
                on_file_dropped(widget.file_path)
                # 更新显示的文本为文件名
                import os
                filename = os.path.basename(widget.file_path)
                widget.text = f"Selected File: {filename}"
                widget.update()
        else:
            event.ignore()

    # 将事件处理函数分配给 widget
    widget.paintEvent = paintEvent
    widget.dragEnterEvent = dragEnterEvent
    widget.dropEvent = dropEvent

    # 设置初始样式
    widget.setStyleSheet("""
        background-color: #f0f0f0;
        border: 2px dashed #aaa;
        border-radius: 15px;
    """)

    # 设置固定大小
    widget.setFixedSize(300, 200)
