# -*- coding: utf-8 -*-
"""
本地 LLM 网页问答界面（实践1~3 配套）
- 后端：Flask，监听 5000 端口
- 前端：聊天 UI（深色终端风）
- 两种模式：
    1) plain  纯 LLM 对话（实践1）
    2) rag    先检索本地知识文件再回答（实践2/3）
- 底层调用本地 Ollama（localhost:11434）
"""
import os
from flask import Flask, request, jsonify, send_from_directory
import ollama
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

BASE = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "http://localhost:11434"
LLM_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")
EMBED_MODEL = "nomic-embed-text"

app = Flask(__name__)

# 预加载本地知识索引（实践2/3 用）
index = None
import threading
_idx_lock = threading.Lock()
def build_index():
    global index
    with _idx_lock:
        try:
            Settings.llm = Ollama(model=LLM_MODEL, base_url=BASE_URL, context_window=4096)
            Settings.embed_model = OllamaEmbedding(model_name=EMBED_MODEL, base_url=BASE_URL)
            docs = SimpleDirectoryReader(os.path.join(BASE, "data")).load_data()
            index = VectorStoreIndex.from_documents(docs)
            print(f"[RAG] 知识索引已加载，共 {len(docs)} 个文档")
            return True
        except Exception as e:
            print(f"[RAG] 索引加载失败: {e}")
            return False

@app.route("/")
def home():
    return send_from_directory(BASE, "chat_front.html")

@app.route("/api/models")
def api_models():
    try:
        resp = ollama.list()
        return jsonify([m.get("model") or m.get("name") for m in resp.get("models", [])])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    mode = data.get("mode", "plain")
    history = data.get("messages", [])   # [{role, content}...]
    query = (history[-1]["content"] if history else "")

    try:
        if mode == "rag":
            # 检索本地知识 + 让模型基于检索结果回答
            # 若后台索引线程还没建好，等待它完成（最多约30秒）
            for _ in range(30):
                if index is not None:
                    break
                import time; time.sleep(1)
            if index is None:
                return jsonify({"error": "知识索引未就绪，请检查 data/ 目录和 Ollama 服务"}), 500
            qe = index.as_query_engine()
            context = str(qe.query(query))
            answer = context  # llama-index 已用本地生成模型回答
        else:
            # 纯 LLM 对话
            resp = ollama.chat(model=LLM_MODEL, messages=history)
            answer = resp["message"]["content"]
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"调用失败: {e}"}), 500

if __name__ == "__main__":
    # 后台预加载知识索引（避免阻塞启动；首次 rag 查询前会确保 ready）
    import threading
    threading.Thread(target=build_index, daemon=True).start()
    print(f"\n  LLM 问答界面已启动: http://127.0.0.1:5000")
    print(f"  模型: {LLM_MODEL}   (可用 OLLAMA_MODEL 环境变量换)")
    print(f"  知识索引后台加载中，首次「查本地资料」可能需要等待几秒\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
