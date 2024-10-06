from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

def main():
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("PyQt Example")
    
    layout = QVBoxLayout()
    button = QPushButton('Click Me')
    layout.addWidget(button)
    
    window.setLayout(layout)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
