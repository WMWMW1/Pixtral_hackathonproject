# ui/main_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout

def create_main_window():
    # 创建主窗口
    main_window = QWidget()
    main_window.setWindowTitle("PyQt5 Node Switch Example")
    main_window.setGeometry(100, 100, 500, 400)
    
    # 主窗口布局
    layout = QVBoxLayout()
    main_window.setLayout(layout)

    return main_window, layout

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            clear_layout(item.layout())

