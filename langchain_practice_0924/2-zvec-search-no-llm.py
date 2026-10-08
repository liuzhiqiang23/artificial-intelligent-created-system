# -*- coding: utf-8 -*-
# 0917 检查题保底版：无框架向量存储+检索（不依赖 ollama，只打印 top3 命中）
# 用法：先跑 2-zvec-minilm-save.py 建库，再跑本脚本，输入任意问题
import os
import zvec
import numpy as np
from sentence_transformers import SentenceTransformer

script_dir = os.path.dirname(__file__)
MODEL = os.path.join(script_dir, '..', '..', 'models', 'all-MiniLM')   # 384 维，与建库同模型
coll_path = os.path.join(script_dir, 'zvec', 'coll')

texts = [
    "LangChain is a framework for developing applications powered by language models.",
    "LLamaIndex is a data framework for LLM applications to ingest, structure and access private or domain-specific data.",
    "PyPDFLoader loads a PDF file into documents, one document per page.",
    "Tesseract is an optical character recognition engine for various operating systems.",
    "FAISS is a library for efficient similarity search and clustering of dense vectors.",
    "Ollama runs large language models locally on your own machine.",
    "DeepSeek-R1 is a reasoning large language model with strong math and code abilities.",
    "A vector database stores embeddings and supports similarity search.",
    "RecursiveCharacterTextSplitter splits long text into overlapping chunks.",
]
docs = {i: t for i, t in enumerate(texts)}

model = SentenceTransformer(MODEL)
coll = zvec.open(path=coll_path)   # 打开已建好的库
print("库已打开。输入问题检索 top3（维数 384 = all-MiniLM-L6-v2）；输入 q 退出")
while True:
    q = input("问题> ").strip()
    if q in ('q', 'quit', 'exit', ''):
        break
    qv = model.encode(q)
    results = coll.query(zvec.VectorQuery(field_name="embedding", vector=qv), topk=3)
    print("\n检索结果（按相似度排序）：")
    for r in results:
        i = r.fields['id']
        print(f"  [{i}] {docs[i][:60]}")
    print()
print("bye")
