import tkinter as tk
from tkinterdnd2 import TkinterDnD
from components.text_input_window import create_text_input_window
from backend.llm_backend import llm_generate_json

def on_proceed_to_generate_flow(description):
    """
    Callback for when the user inputs their requirements and clicks 'Proceed'.
    This should communicate with LLM to generate a JSON that will be used to build the flow.
    """
    # Mock: Get generated JSON from LLM backend
    generated_json = llm_generate_json(description)
    print("Generated JSON from LLM:")
    print(generated_json)

    # TODO: Use the generated JSON to build UI nodes dynamically

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("AI App Builder")
    window_width = 500
    window_height = 400
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)

    # 强制进入第一个界面：文本输入界面
    create_text_input_window(root, on_proceed_callback=on_proceed_to_generate_flow)

    root.mainloop()
