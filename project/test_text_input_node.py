# test_text_input_node.py
import sys
from PyQt5.QtWidgets import QApplication
from nodes.main_window import create_main_window
from nodes.text_input_node import create_text_input_node

def main():
    app = QApplication(sys.argv)

    # Create main window and layout
    main_window, layout = create_main_window()

    def on_text_entered(text):
        print(f"Text entered: {text}")

    # Create text input node for testing
    create_text_input_node(
        layout=layout,
    )

    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
