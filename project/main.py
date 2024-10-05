# main.py

import tkinter as tk
from tkinterdnd2 import TkinterDnD
from ui.text_input_window import create_text_input_window
from ui.file_upload_window import create_file_upload_window
from ui.text_output_window import create_text_output_window
from backend.llm_backend import LLMBackend

def main():
    # 初始化主应用窗口
    root = TkinterDnD.Tk()
    root.title("AI Application Builder")
    window_width = 500
    window_height = 400
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)
    
    # 初始化聊天历史
    chat_history = []
    
    # 初始化 LLM 后端
    llm_backend = LLMBackend(chat_history)
    
    # 定义从文本输入窗口继续时的回调函数
    def on_proceed(description):
        # 将用户的描述添加到聊天历史
        chat_history.append({"role": "user", "content": description})
        
        # 从 LLM 后端获取生成的 JSON
        generated_json = llm_backend.generate_flow(description)
        
        # 根据生成的 JSON 构建 UI
        build_ui_from_json(generated_json)
    
    # 根据 JSON 数据构建 UI
    def build_ui_from_json(json_data):
        nodes = json_data.get("nodes", [])
        node_dict = {node['node_name']: node for node in nodes}
        init_node_name = json_data.get("initnode")
        
        def render_node(node_name):
            node = node_dict.get(node_name)
            if not node:
                return
            node_type = node.get("node_name")
            params = node.get("params", {})
            next_node_name = node.get("nextpage")
            
            if node_type == "file_upload_window":
                create_file_upload_window(root, on_proceed_callback=lambda: render_node(next_node_name), **params)
            elif node_type == "text_output_window":
                content = params.get("text_content", "")
                create_text_output_window(root, text_content=content)
                if next_node_name != "end":
                    # 如果有下一个节点，继续渲染
                    render_node(next_node_name)
            else:
                # 处理其他节点类型
                pass
        
        # 从初始节点开始渲染
        render_node(init_node_name)
    
    # 从文本输入窗口开始
    create_text_input_window(root, on_proceed)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()
