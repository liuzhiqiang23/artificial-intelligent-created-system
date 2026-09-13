# -*- coding: utf-8 -*-
"""
实践3：在实践2中添加向量索引
流程（对照课件）：
1. 导入相关的库
2. 加载数据
3. 构建索引（向量索引 VectorStoreIndex）
4. 创建问答引擎（ChatEngine）
5. 开始问答（循环多轮对话）
"""
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# ========== 1. 导入相关的库（已导入）+ 设置本地模型 ==========
LLM_MODEL = "qwen2.5-coder:7b"
EMBED_MODEL = "nomic-embed-text"
BASE_URL = "http://localhost:11434"

Settings.llm = Ollama(model=LLM_MODEL, base_url=BASE_URL, temperature=0.1)
Settings.embed_model = OllamaEmbedding(model_name=EMBED_MODEL, base_url=BASE_URL)

# ========== 2. 加载数据 ==========
documents = SimpleDirectoryReader("data").load_data()
print(f"已加载 {len(documents)} 个文档")

# ========== 3. 构建向量索引 ==========
index = VectorStoreIndex.from_documents(documents)

# ========== 4. 创建问答引擎（带记忆的多轮对话） ==========
memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    memory=memory,
    llm=Settings.llm,
)

# ========== 5. 开始问答（连续多轮，演示向量索引问答） ==========
questions = [
    "Ollama 支持哪些模型？",
    "Ollama 默认监听在哪个端口？",
    "Ollama 如何实现 GPU 加速？",
]
print("\n=== 开始问答 ===")
for qa in questions:
    resp = chat_engine.chat(qa)
    print("\n问题:", qa)
    print("回答:", str(resp))
