# -*- coding: utf-8 -*-
"""
实践2：使用 llama-index 嵌入文件
流程（对照课件）：
1. 导入相关依赖
2. 设置本地模型（Ollama 生成模型 + Ollama 嵌入模型）
3. 加载本地文件（SimpleDirectoryReader）
4. 建立索引（不使用外部向量数据库，用内存 VectorStoreIndex）
5. 创建查询引擎
6. 执行查询
7. 打印响应信息
"""
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# ========== 2. 设置本地模型 ==========
LLM_MODEL = "qwen2.5:0.5b"        # 生成模型（需 ollama pull qwen2.5:0.5b）
EMBED_MODEL = "nomic-embed-text"  # 嵌入模型（需 ollama pull nomic-embed-text）
BASE_URL = "http://localhost:11434"  # Ollama 服务地址

Settings.llm = Ollama(model=LLM_MODEL, base_url=BASE_URL)
Settings.embed_model = OllamaEmbedding(
    model_name=EMBED_MODEL, base_url=BASE_URL
)

# ========== 3. 加载本地文件 ==========
documents = SimpleDirectoryReader("data").load_data()
print(f"已加载 {len(documents)} 个文档")

# ========== 4. 建立索引（不使用外部向量数据库） ==========
index = VectorStoreIndex.from_documents(documents)

# ========== 5. 创建查询引擎 ==========
query_engine = index.as_query_engine()

# ========== 6. 执行查询 ==========
query = "Ollama 支持哪些模型？常用命令有哪些？"
response = query_engine.query(query)

# ========== 7. 打印响应信息 ==========
print("\n=== 查询问题 ===")
print(query)
print("\n=== 回答 ===")
print(str(response))
