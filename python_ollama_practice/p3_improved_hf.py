# -*- coding: utf-8 -*-
"""
实践3（改进）：自选嵌入模型和本地生成模型
流程（对照课件）：
1. 安装 Huggingface 依赖（sentence-transformers / transformers）
2. 导入相关的库
3. 加载本地嵌入模型（moka-ai/m3e-small，中文优化）
4. 加载数据
5. 构建索引
6. 创建问答引擎（本地生成模型用 Ollama qwen2.5-coder:7b）
7. 开始问答
"""
# ========== 2. 导入相关的库 ==========
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.memory import ChatMemoryBuffer

# ========== 1&3. 安装 HF 依赖 + 加载本地嵌入模型（自选中文嵌入） ==========
# 首次运行会自动从 HuggingFace 下载 moka-ai/m3e-small（约 100MB）
EMBED_MODEL_PATH = "moka-ai/m3e-small"   # 自选嵌入模型（中文优化）
embed_model = HuggingFaceEmbedding(
    model_name=EMBED_MODEL_PATH,
    device="cpu",               # 用 CPU 算嵌入，稳
)

# ========== 本地生成模型（Ollama qwen2.5-coder:7b） ==========
LLM_MODEL = "qwen2.5-coder:7b"
BASE_URL = "http://localhost:11434"
llm = Ollama(model=LLM_MODEL, base_url=BASE_URL, temperature=0.1, context_window=4096)

Settings.embed_model = embed_model
Settings.llm = llm

# ========== 4. 加载数据 ==========
documents = SimpleDirectoryReader("data").load_data()
print(f"已加载 {len(documents)} 个文档，嵌入模型: {EMBED_MODEL_PATH}")

# ========== 5. 构建索引（用自选中文嵌入模型） ==========
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

# ========== 6. 创建问答引擎 ==========
memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    memory=memory,
    llm=llm,
)

# ========== 7. 开始问答 ==========
questions = [
    "Ollama 支持哪些模型？",
    "使用 Ollama 下载模型的命令是什么？",
    "Ollama 在无 GPU 时会怎样？",
]
print("\n=== 开始问答（自选嵌入模型 m3e-small + 本地生成 qwen2.5-coder:7b）===")
for qa in questions:
    resp = chat_engine.chat(qa)
    print("\n问题:", qa)
    print("回答:", str(resp))
