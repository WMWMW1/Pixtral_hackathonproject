# test_text_display_node.py
import sys
from PyQt5.QtWidgets import QApplication
from nodes.main_window import create_main_window
from nodes.text_display_node import create_text_display_node

def main():
    app = QApplication(sys.argv)

    # Create main window and layout
    main_window, layout = create_main_window()

    def go_back():
        print("Back button clicked!")

    # Create text display node for testing
    create_text_display_node(
        layout=layout,
        text_content="""No specific allergens are directly mentioned on the menu; however, based on the listed items:
Fish & chips may contain allergens such as fish, gluten (from the batter or breading), and possibly dairy.

Cheese 'burger may contain dairy (cheese), gluten (from the bun), and possibly other common allergens like soy or sesame.
Please make sure to confirm the presence of any allergens according to your dietary requirements.
""",
    )

    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
