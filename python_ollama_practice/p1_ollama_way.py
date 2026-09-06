# -*- coding: utf-8 -*-
"""
实践1：访问本地LLM —— Ollama 方式
安装并引入依赖：ollama
创建会话：ollama.chat
输出结果：print
"""
import ollama

MODEL = "qwen2.5:0.5b"  # 需要先用 ollama pull qwen2.5:0.5b 拉取

# 创建会话（单轮对话）
response = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "user", "content": "请用一句中文介绍你自己，并说明你是什么模型。"},
    ],
)

# 输出结果
print("=== Ollama 方式输出结果 ===")
print(response["message"]["content"])
