# -*- coding: utf-8 -*-
# PDF 加载 1：LangChain PyPDFLoader（对照《笔记0924.pdf》2-1）
import os
script_dir = os.path.dirname(__file__)

# A. 直接使用 PyPDF 加载：返回 List[Document]，默认按页切分
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader(os.path.join(script_dir, 'file', '05.pdf'))
documents = loader.load()  # 返回 List[Document]
print(f"[A] PyPDFLoader 加载: {len(documents)} 个文档（按页切分）")
print(f"    第1页前40字: {documents[0].page_content[:40]!r}")

# B. 使用 DirectoryLoader 批量加载目录下的所有 PDF
from langchain_community.document_loaders import DirectoryLoader
loader2 = DirectoryLoader(
    path=script_dir,          # 从项目根目录开始
    glob="**/*.pdf",          # 递归匹配（任务书写法）
    loader_cls=PyPDFLoader,
)
documents2 = loader2.load()
print(f"[B] DirectoryLoader 批量: {len(documents2)} 个文档")
