# nodes/chat_node.py
import threading
import queue
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel,
    QWidget, QScrollArea, QSplitter, QTextBrowser
)
from PyQt5.QtCore import Qt, QTimer
from nodes.main_window import clear_layout

# Import backend functions
from backend.llm_api import initialize_client, get_ai_response

def create_chat_node(layout, next_node=None, button_text="Confirm", model_name="mistral-large-latest", history=None, prompt=None):
    # Clear current layout
    clear_layout(layout)

    # Initialize Mistral client
    client = initialize_client()

    # Chat history
    chat_history = history if history is not None else []

    # If an initial prompt is provided, add it to the chat history
    if prompt:
        chat_history.append({"role": "system", "content": prompt})

    # Create chat area (scrollable)
    chat_area = QScrollArea()
    chat_area.setWidgetResizable(True)
    
    chat_container = QWidget()
    chat_container_layout = QVBoxLayout()
    chat_container_layout.setAlignment(Qt.AlignTop)
    chat_container.setLayout(chat_container_layout)
    chat_area.setWidget(chat_container)
    
    # Create chat input and "Send" button
    chat_input = QTextEdit()
    send_button = QPushButton("Send")

    # Create confirmation button
    confirm_button = QPushButton(button_text if button_text else "Proceed")
    confirm_button.setVisible(True)  # Visible from the beginning to allow confirmation
    
    # Layout for input and buttons
    input_layout = QHBoxLayout()
    input_layout.addWidget(chat_input)
    input_layout.addWidget(send_button)
    input_layout.addWidget(confirm_button)
    
    # Splitter to allow resizing between chat area and input
    splitter = QSplitter(Qt.Vertical)
    splitter.addWidget(chat_area)
    
    # Container for input part
    input_container = QWidget()
    input_container.setLayout(input_layout)
    splitter.addWidget(input_container)
    
    # Set initial sizes
    splitter.setSizes([300, 100])
    
    # Add splitter to main layout
    layout.addWidget(splitter)
    
    # Queue to handle AI responses
    ai_response_queue = queue.Queue()
    
    # Flag to determine if JSON generation mode is active
    json_mode = {'active': False}

    # Handle sending messages
    def send_message():
        user_text = chat_input.toPlainText().strip()
        if user_text:
            # Clear input
            chat_input.clear()
            
            # Display user message
            add_message(chat_container_layout, user_text, alignment=Qt.AlignRight, is_user=True)

            # Append to chat history
            chat_history.append({
                "role": "user",
                "content": user_text
            })

            # Disable send button to prevent multiple clicks
            send_button.setEnabled(False)

            # Start thread to fetch AI response
            threading.Thread(target=fetch_ai_response, args=(chat_history.copy(), ai_response_queue)).start()

    # Function to fetch AI response
    def fetch_ai_response(messages, response_queue):
        try:
            # Get AI response
            ai_message_content = get_ai_response(client, model_name, messages)
            print(f"AI Response: {ai_message_content}")  # Debug print

            # Put response in queue
            response_queue.put(ai_message_content)

        except Exception as e:
            # Handle exceptions
            print(f"Error fetching AI response: {e}")
            response_queue.put(None)

    # Function to check AI response queue
    def check_ai_response():
        try:
            # Get AI response from queue
            ai_message_content = ai_response_queue.get_nowait()
        except queue.Empty:
            # If queue is empty, check again later
            pass
        else:
            if ai_message_content is not None:
                # Append to chat history
                chat_history.append({
                    "role": "assistant",
                    "content": ai_message_content
                })
                # Display AI message
                add_message(chat_container_layout, ai_message_content, alignment=Qt.AlignLeft, is_user=False)
                
            else:
                # Display error message
                add_message(chat_container_layout, "Error fetching AI response.", alignment=Qt.AlignLeft, is_user=False)

            # Re-enable send button
            send_button.setEnabled(True)

        # Continue checking the queue
        QTimer.singleShot(100, check_ai_response)

    # Start checking AI response
    check_ai_response()

    # Connect send button
    send_button.clicked.connect(send_message)

    # Function to add messages to chat
    def add_message(layout, text, alignment=Qt.AlignLeft, is_user=False):
        # Use QTextBrowser for selectable and copyable text
        message_browser = QTextBrowser()
        message_browser.setPlainText(text)
        message_browser.setReadOnly(True)  # Read-only to allow text selection and copying
        message_browser.setFixedWidth(250)  # Limit bubble width
        message_browser.setStyleSheet("""
            QTextBrowser {
                padding: 10px;
                border-radius: 10px;
                background-color: #e1ffc7;  /* Green bubble */
                border: none;
            }
        """ if is_user else """
            QTextBrowser {
                padding: 10px;
                border-radius: 10px;
                background-color: #cce5ff;  /* Blue bubble */
                border: none;
            }
        """)

        # Remove scrollbars
        message_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        message_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Layout for the message
        message_layout = QHBoxLayout()
        message_layout.addWidget(message_browser)
        message_layout.setAlignment(alignment)

        # Adjust margins between bubbles
        message_layout.setContentsMargins(5, 5, 5, 5)  # Left, Top, Right, Bottom

        # Container for the message
        container = QWidget()
        container.setLayout(message_layout)

        # Add to chat layout
        layout.addWidget(container)

        # Scroll to bottom
        chat_area.verticalScrollBar().setValue(chat_area.verticalScrollBar().maximum())

    # Handle confirmation to generate JSON
    def confirm_generation():
        if not json_mode['active']:
            json_mode['active'] = True
            # Add JSON generation prompt to chat history
            json_prompt = (
                "You have confirmed to generate the agent. "
                "Please provide a JSON definition with the following format:\n\n"
                "```json\n"
                "{\n"
                '  "initial_node": "node_name",\n'
                '  "nodes": {\n'
                '    "node_name": {\n'
                '      "type": "node_type",\n'
                '      "next_node": "next_node_name",\n'
                '      "button_text": "Button Text",\n'
                '      "prompt": "Prompt text for the node (if applicable)"\n'
                '    },\n'
                '    // ... other nodes\n'
                '  }\n'
                "}\n"
                "```\n\n"
                "The agent should contain all necessary nodes and follow the format strictly."
            )
            chat_history.append({"role": "system", "content": json_prompt})
            # Notify user about JSON generation
            add_message(chat_container_layout, "Switching to JSON generation mode. Please wait...", alignment=Qt.AlignLeft, is_user=False)
            # Trigger next step (generate JSON)
            if next_node:
                next_node()

    # Connect confirm button
    if next_node:
        confirm_button.clicked.connect(confirm_generation)
