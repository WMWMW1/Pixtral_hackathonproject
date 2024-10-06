from nodes.chat_node import create_chat_node
from nodes.file_upload_node import create_file_upload_node
from nodes.camera_capture_node import create_camera_capture_node
from nodes.text_input_node import create_text_input_node
from nodes.text_display_node import create_text_display_node

def run_agent(layout, agent_json):
    nodes = agent_json.get("nodes", {})
    initial_node_name = agent_json.get("initial_node")

    if not initial_node_name or initial_node_name not in nodes:
        print("Invalid initial node.")
        return

    node_functions = {}

    # Define how each node should be created based on its type
    for node_name, node_info in nodes.items():
        node_type = node_info.get("type")
        next_node_name = node_info.get("next_node")
        button_text = node_info.get("button_text", "Next")
        prompt = node_info.get("prompt")

        if node_type == "text_input":
            def create_node(node_name=node_name, next_node_name=next_node_name):
                def next_node(text):
                    if next_node_name in node_functions:
                        node_functions[next_node_name](text)
                create_text_input_node(layout, on_next=next_node)
            node_functions[node_name] = create_node

        elif node_type == "display_text":
            def create_node(node_name=node_name, next_node_name=next_node_name):
                def next_node():
                    if next_node_name in node_functions:
                        node_functions[next_node_name]()
                create_text_display_node(layout, text_content=prompt, on_back=next_node)
            node_functions[node_name] = create_node

        elif node_type == "file_upload":
            def create_node(node_name=node_name, next_node_name=next_node_name):
                def next_node(file_path):
                    if next_node_name in node_functions:
                        node_functions[next_node_name](file_path)
                create_file_upload_node(layout, on_next=next_node, button_text=button_text)
            node_functions[node_name] = create_node

        elif node_type == "camera_capture":
            def create_node(node_name=node_name, next_node_name=next_node_name):
                def next_node(image_path):
                    if next_node_name in node_functions:
                        node_functions[next_node_name](image_path)
                create_camera_capture_node(layout, on_next=next_node)
            node_functions[node_name] = create_node

    # Start the initial node
    node_functions[initial_node_name]()
