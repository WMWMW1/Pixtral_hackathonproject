# test_file_upload_node.py
import sys
from PyQt5.QtWidgets import QApplication
from nodes.main_window import create_main_window
from nodes.file_upload_node import create_file_upload_node

def main():
    app = QApplication(sys.argv)

    # Create main window and layout
    main_window, layout = create_main_window()


    # Create file upload node for testing
    create_file_upload_node(
        layout=layout,
        button_text="Upload and Proceed"
    )

    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
