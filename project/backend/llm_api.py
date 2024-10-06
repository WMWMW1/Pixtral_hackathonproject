# backend/llm_api.py

import os
from mistralai import Mistral

def initialize_client(api_key=None):
    if api_key is None:
        api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY not found in environment variables.")
    client = Mistral(api_key=api_key)
    return client

def get_ai_response(client, model_name, messages):
    # 调用 Mistral AI API 获取 AI 响应
    chat_response = client.chat.complete(
        model=model_name,
        messages=messages
    )
    # 提取 AI 的消息内容
    ai_message_content = chat_response.choices[0].message.content
    return ai_message_content
