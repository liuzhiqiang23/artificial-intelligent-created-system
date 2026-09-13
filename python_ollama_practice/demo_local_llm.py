# -*- coding: utf-8 -*-
"""
本地 LLM 连接测试 —— 用 Python 连接本机 Ollama 的 qwen2.5-coder:7b
演示三种调用方式：
  1) 单轮问答（generate）
  2) 多轮对话（chat，带上下文记忆）
  3) 流式输出（stream，逐字打印）
运行前确保：Ollama 服务在线（http://localhost:11434）
"""
import ollama

MODEL = "qwen2.5-coder:7b"
BASE_URL = "http://localhost:11434"

client = ollama.Client(host=BASE_URL)


def demo_1_单轮问答():
    print("=" * 60)
    print("【测试1】单轮问答（generate）")
    print("=" * 60)
    question = "用一句话解释什么是大语言模型。"
    print(f"问：{question}")
    resp = client.generate(model=MODEL, prompt=question)
    print(f"答：{resp['response'].strip()}")
    print()


def demo_2_多轮对话():
    print("=" * 60)
    print("【测试2】多轮对话（chat，带上下文记忆）")
    print("=" * 60)
    messages = [
        {"role": "user", "content": "我叫小刘，正在学大模型部署。"},
        {"role": "assistant", "content": "你好小刘！大模型部署是很有意思的方向。"},
        {"role": "user", "content": "我叫什么？在学什么？"},
    ]
    for m in messages:
        if m["role"] == "user":
            print(f"用户：{m['content']}")
    resp = client.chat(model=MODEL, messages=messages)
    print(f"AI：{resp['message']['content'].strip()}")
    print()


def demo_3_流式输出():
    print("=" * 60)
    print("【测试3】流式输出（stream，逐字打印）")
    print("=" * 60)
    question = "用三行话介绍 Ollama。"
    print(f"问：{question}")
    print("答：", end="", flush=True)
    stream = client.chat(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        stream=True,
    )
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)
    print("\n")


if __name__ == "__main__":
    print(f"\n本地 LLM 连接测试  模型={MODEL}  地址={BASE_URL}\n")
    demo_1_单轮问答()
    demo_2_多轮对话()
    demo_3_流式输出()
    print("=" * 60)
    print("全部测试完成 [OK]")
    print("=" * 60)
