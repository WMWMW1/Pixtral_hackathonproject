# backend/llm_backend.py

class LLMBackend:
    def __init__(self, chat_history):
        self.chat_history = chat_history
        # 初始化其他所需的变量或配置
    
    def generate_flow(self, description):
        # 这里应该调用实际的 LLM API 来生成流程 JSON
        # 为演示目的，我们将模拟响应
        
        # 模拟 LLM 响应
        generated_json = {
            "initnode": "file_upload_window",
            "nodes": [
                {
                    "node_name": "file_upload_window",
                    "params": {"remove_btn_text": "Remove File", "switch_btn_text": "Proceed"},
                    "nextpage": "text_output_window"
                },
                {
                    "node_name": "text_output_window",
                    "params": {"text_content": "Thank you for uploading your file."},
                    "nextpage": "end"
                }
            ]
        }
        
        # 将助手的响应添加到聊天历史
        self.chat_history.append({"role": "assistant", "content": str(generated_json)})
        
        return generated_json
