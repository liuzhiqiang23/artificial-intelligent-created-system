# -*- coding: utf-8 -*-
# 笔记1008 第4-1节：JSON 格式三路加载（对照原文，路径适配 Windows）
import os, json
script_dir = os.path.dirname(__file__)
F = os.path.join(script_dir, 'file1008', 'pages.json')

# ---------- A. 直接使用 json 库：返回 dict，适合精细化控制 ----------
with open(F, encoding='utf-8') as f:
    rt = json.load(f)
print(f"[A] json 库直读: type={type(rt).__name__}, {len(rt)} 条")
print(f"    第1条: {rt[0]}")

# ---------- B. LangChain JSONLoader（依赖 pip install jq）----------
from langchain_community.document_loaders import JSONLoader
loader = JSONLoader(
    file_path=F,
    jq_schema='.',        # 取整个文档；jq 语法可在 https://play.jqlang.org/ 测试
    text_content=False,   # 以 str 作为 page_content
)
documents = loader.load()
print(f"[B] JSONLoader: {len(documents)} 个文档")
print(f"    前60字: {documents[0].page_content[:60]!r}")

# ---------- C. LlamaIndex JSONReader（依赖 llama-index-readers-json）----------
from llama_index.readers.json import JSONReader
reader = JSONReader()
documents = reader.load_data(input_file=F)
print(f"[C-1] JSONReader 单文件: {len(documents)} 个文档")

# 目录批量：file_extractor 指定 .json 用 JSONReader（不指定则当纯文本读）
from llama_index.core import SimpleDirectoryReader
reader2 = SimpleDirectoryReader(
    input_dir=os.path.join(script_dir, 'file1008'),
    required_exts=['.json'],
    file_extractor={'.json': JSONReader()},
)
documents = reader2.load_data()
print(f"[C-2] SimpleDirectoryReader 批量: {len(documents)} 个文档")
print(f"    内容前50字: {documents[0].text[:50]!r}")
