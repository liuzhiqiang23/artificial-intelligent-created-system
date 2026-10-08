# -*- coding: utf-8 -*-
# 笔记1008 第4-3节：Markdown 文件加载（对照原文）
# 依赖：pip install "unstructured[md]"==0.18.32（本项目 unstructured 钉 0.18.32）
import os
script_dir = os.path.dirname(__file__)
MD = os.path.join(script_dir, 'file1008', 'vue.md')

# ---------- B. LangChain ----------
from langchain_community.document_loaders import UnstructuredMarkdownLoader
loader = UnstructuredMarkdownLoader(MD)
documents = loader.load()
print(f"[B] UnstructuredMarkdownLoader: {len(documents)} 个文档")
print(f"    前60字: {documents[0].page_content[:60]!r}")

# ---------- C. LlamaIndex ----------
from llama_index.readers.file.markdown import MarkdownReader
reader = MarkdownReader()
documents = reader.load_data(file=MD)
print(f"[C] MarkdownReader: {len(documents)} 个文档")

# 也可以用 SimpleDirectoryReader 直接读，无需指定读取器
from llama_index.core import SimpleDirectoryReader
documents = SimpleDirectoryReader(
    input_files=[MD]).load_data()
print(f"[C] SimpleDirectoryReader 直读: {len(documents)} 个文档, 前40字 {documents[0].text[:40]!r}")
