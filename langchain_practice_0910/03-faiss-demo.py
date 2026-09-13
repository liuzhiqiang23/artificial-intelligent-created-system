# -*- coding: utf-8 -*-
# 实践6：无框架自选向量数据库 faiss + BGE（对照《笔记0910.pdf》第6节）
import os
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"

# 准备文档数据（摘自 txt/wiki.txt 的黑神话：悟空资料）
docs = [
    "《黑神话：悟空》是一款动作角色扮演游戏，由游戏科学开发，2024年8月20日发售，登陆PC与PS5平台。",
    "游戏发售当日销量超过450万份，总销售额超过15亿元，创下国产单机游戏销量纪录。",
    "游戏改编自《西游记》，玩家扮演天命人，为探寻昔日传说的真相，踏上一条充满危险与惊奇的西游之路。",
    "《黑神话：悟空》的场景包括黑风山、黄风岭、小西天、盘丝洞、火焰山、花果山六大章节。",
    "游戏采用虚幻引擎5开发，画面表现出色，战斗系统以棍法为核心，有立棍、劈棍、戳棍等多种棍势。",
]

# 设置嵌入模型（使用本地 BGE，CPU 运算）
from sentence_transformers import SentenceTransformer
model = SentenceTransformer(r"C:\Users\Lenovo\.cache\huggingface\hub\models--BAAI--bge-small-zh-v1.5\snapshots\7999e1d3359715c523056ef9478215996d62a620")

# 嵌入文档
doc_embeddings = model.encode(docs)
print(f"文档向量维度: {doc_embeddings.shape}")

# 创建向量存储
import faiss
import numpy as np
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(doc_embeddings.astype('float32'))
print(f"向量数据库中的文档数量: {index.ntotal}")

# 执行相似度检索
question = "黑神话悟空的战斗系统有什么特点?"
query_embedding = model.encode([question])[0]
distances, indices = index.search(
    np.array([query_embedding]).astype('float32'),
    k=3
)
context = [docs[idx] for idx in indices[0]]
print("\n检索到的相关文档:")
for i, doc in enumerate(context, 1):
    print(f"[{i}] {doc}")

# 构建提示词
prompt = f"""根据以下参考信息回答问题，并给出信息源编号。
如果无法从参考信息中找到答案，请说明无法回答。
参考信息:
{chr(10).join(f"[{i+1}] {doc}" for i, doc in enumerate(context))}
问题: {question}
答案:"""

# 使用 Ollama 生成答案
from ollama import chat
response = chat(
    model="deepseek-r1:latest",
    messages=[{
        "role": "user",
        "content": prompt
    }],
)
print(f"\n生成的答案: {response.message.content}")
