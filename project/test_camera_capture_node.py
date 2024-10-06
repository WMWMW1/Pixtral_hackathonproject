# test_camera_capture_node.py
import sys
from PyQt5.QtWidgets import QApplication
from nodes.main_window import create_main_window
from nodes.camera_capture_node import create_camera_capture_node

def main():
    app = QApplication(sys.argv)

    # Create main window and layout
    main_window, layout = create_main_window()

    def on_image_captured(image_path):
        print(f"Image captured: {image_path}")

    # Create camera capture node for testing
    create_camera_capture_node(
        layout=layout,
    )

    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
