# -*- coding: utf-8 -*-
# PDF 加载 2：LlamaIndex PyMuPDFReader + SimpleDirectoryReader（对照《笔记0924.pdf》2-2）
# 依赖：pip install pymupdf（新版 LlamaIndex 已从 PyPDF 改用 PyMuPDF）
import os
script_dir = os.path.dirname(__file__)

# A. 直接使用 PyMuPDF 加载
from llama_index.readers.file.pymu_pdf import PyMuPDFReader
pdf_reader = PyMuPDFReader()
docs = pdf_reader.load_data(file_path=os.path.join(script_dir, 'file', '05.pdf'))
print(f"[A] PyMuPDFReader 加载: {len(docs)} 个文档")
print(f"    首文档前40字: {docs[0].text[:40]!r}")

# B. 使用 SimpleDirectoryReader 批量加载（file_extractor 指定各格式用什么读取器）
from llama_index.core import SimpleDirectoryReader
reader = SimpleDirectoryReader(
    input_dir=os.path.join(script_dir, 'file'),
    recursive=True,
    required_exts=[".pdf"],           # 任务书示例为 [".txt",".pdf"]，按需增减
    file_extractor={".pdf": pdf_reader},
)
documents = reader.load_data()
print(f"[B] SimpleDirectoryReader 批量: {len(documents)} 个文档")
