# -*- coding: utf-8 -*-
# 实践6(续)：zvec 向量数据库（对照《笔记0910.pdf》第6节4）
# 任务书允许沿用 BGE 嵌入（"可以使用之前的 BGE，也可以改为其它嵌入模型"）
import os
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"

# 准备文档数据（同 faiss 版）
docs = [
    "《黑神话：悟空》是一款动作角色扮演游戏，由游戏科学开发，2024年8月20日发售，登陆PC与PS5平台。",
    "游戏发售当日销量超过450万份，总销售额超过15亿元，创下国产单机游戏销量纪录。",
    "游戏改编自《西游记》，玩家扮演天命人，为探寻昔日传说的真相，踏上一条充满危险与惊奇的西游之路。",
    "《黑神话：悟空》的场景包括黑风山、黄风岭、小西天、盘丝洞、火焰山、花果山六大章节。",
    "游戏采用虚幻引擎5开发，画面表现出色，战斗系统以棍法为核心，有立棍、劈棍、戳棍等多种棍势。",
]

# 设置嵌入模型（本地 BGE，CPU）
from sentence_transformers import SentenceTransformer
model = SentenceTransformer(r"C:\Users\Lenovo\.cache\huggingface\hub\models--BAAI--bge-small-zh-v1.5\snapshots\7999e1d3359715c523056ef9478215996d62a620")

# 嵌入文档
doc_embeddings = model.encode(docs)
print(f"文档向量维度: {doc_embeddings.shape}")

# 使用 zvec：创建 Schema
import zvec
import numpy as np
from zvec import FieldSchema, VectorSchema, DataType
dimension = doc_embeddings.shape[1]
id_field = FieldSchema("id", DataType.INT64)
emb_field = VectorSchema("embedding", dimension=dimension, data_type=DataType.VECTOR_FP32)
schema = zvec.CollectionSchema(
    name="Wukong",          # "表名"
    fields=id_field,        # "字段"
    vectors=emb_field,      # "数据结构"
)

# 使用 zvec：根据"表"结构创建数据集合
# （重复运行时先清理上次的集合目录，create_and_open 要求路径不能已存在）
import shutil
if os.path.exists("./zvec/collection"):
    shutil.rmtree("./zvec/collection")
collection = zvec.create_and_open(
    path="./zvec/collection",
    schema=schema,
)

# 使用 zvec：将文档的向量数据存入集合
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  # 屏蔽 VectorQuery 将改名为 Query 的弃用警告
for i, emb in enumerate(doc_embeddings):
    collection.insert(
        zvec.Doc(
            id="txt_" + str(i),                 # Unique document ID
            vectors={"embedding": emb},
            fields={"id": i},
        )
    )
print(f"已存入 {len(doc_embeddings)} 条文档向量")

# 将问题转换为向量
question = "黑神话悟空的战斗系统有什么特点?"
query_embedding = model.encode([question])[0]

# 在 zvec 集合中查询结果
result = collection.query(
    zvec.VectorQuery(
        field_name="embedding",
        vector=query_embedding,
    ),
    topk=3,
)

# 将查询结果转为对应 doc 输出
context = [docs[idx.fields['id']] for idx in result]
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
