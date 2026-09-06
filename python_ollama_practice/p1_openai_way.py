# -*- coding: utf-8 -*-
"""
实践1：访问本地LLM —— OpenAI 方式
安装并引入依赖：openai
连接本地Ollama：base_url 指向 http://localhost:11434/v1
创建会话：client.chat.completions.create
输出结果：print
"""
from openai import OpenAI

# 连接本地 Ollama 的 OpenAI 兼容接口
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # 本地服务不校验，随意填
)

MODEL = "qwen2.5:0.5b"  # 需要先用 ollama pull qwen2.5:0.5b 拉取

# 创建会话
resp = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "请用一句中文介绍你自己，并说明你是什么模型。"},
    ],
)

# 输出结果
print("=== OpenAI 方式输出结果 ===")
print(resp.choices[0].message.content)
