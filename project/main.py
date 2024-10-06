# main.py
import sys
from PyQt5.QtWidgets import QApplication
from nodes.main_window import create_main_window
from ai_builder_agent import AIBuilderAgent
from agent_runner import run_agent
from nodes.chat_node import create_chat_node
def main():
    app = QApplication(sys.argv)

    # Create main window and layout
    main_window, layout = create_main_window()

    # Initialize the AI Builder Agent
    ai_builder = AIBuilderAgent()
    ai_builder.start_requirement_gathering()
    
    # Function to proceed to agent creation once user confirms
    def on_user_confirmed():
        agent_json = ai_builder.generate_agent_definition()
        if agent_json:
            # Clear layout before running the new agent
            layout.itemAt(0).widget().deleteLater()
            run_agent(layout, agent_json)
        else:
            print("Failed to build agent.")

    # Start chat node for gathering requirements
    create_chat_node(
        layout=layout,
        next_node=on_user_confirmed,
        button_text="Generate Agent",
        model_name="mistral-large-latest",
        history=ai_builder.get_build_agent_history()
    )

    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     builder = AIBuilderAgent()
#     builder.start_requirement_gathering()
#     builder.add_user_message("I want a text input node.")
#     # Simulate other messages...
#     agent_json = builder.generate_agent_definition()
#     print(agent_json)
