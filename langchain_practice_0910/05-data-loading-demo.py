# -*- coding: utf-8 -*-
# 数据导入演示（对照《笔记0917.pdf》第三节）
import os

# ===== 1) LangChain 加载文档 =====
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_core.documents import Document

# B. 通过 os 获取当前 py 文件的运行路径（适用于 PyCharm 跑 .py；Jupyter 里没有 __file__）
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'txt', 'wiki.txt')

# A. 加载单个文件：返回 Document 对象的 List，内容在 page_content 属性
loader = TextLoader(file_path, encoding="utf-8")
documents = loader.load()
print(f"[1A] TextLoader 加载单文件：{len(documents)} 个 Document，前30字：{documents[0].page_content[:30]}")

# C. 直接创建 Document 对象
docs = [
    Document(
        page_content="悟空是大师兄.",
        metadata={"source": "师徒四人.txt"},
    ),
    Document(
        page_content="八戒是二师兄.",
        metadata={"source": "师徒四人.txt"},
    ),
]
print(f"[1C] 手工创建 Document：{len(docs)} 个，第一条 = {docs[0].page_content}")

# D. DirectoryLoader 加载目录
# 说明：默认用 unstructured 库会报 ModuleNotFoundError，纯文本用 loader_cls=TextLoader 绕开
dir_loader = DirectoryLoader(
    path=os.path.join(script_dir, 'txt'),
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)
docs2 = dir_loader.load()
print(f"[1D] DirectoryLoader 加载目录：文档数 = {len(docs2)}")

# ===== 2) LlamaIndex 加载文档 =====
try:
    from llama_index.core import SimpleDirectoryReader, Document as LIDocument

    # A. SimpleDirectoryReader 加载目录：内容存在 text 属性
    dir_reader = SimpleDirectoryReader(input_dir=os.path.join(script_dir, 'txt'))
    documents_li = dir_reader.load_data()
    print(f"[2A] SimpleDirectoryReader 加载目录：文档数 = {len(documents_li)}，前30字：{documents_li[0].text[:30]}")

    # B. 直接创建 Document 对象，并添加元数据
    docs_li = [
        LIDocument(
            text="一个充满……",
            metadata={
                "filename": "火照深渊场景.md",
                "category": "游戏场景",
                "file_path": "/data/黑悟空/火照深渊场景.md",
                "author": "GameScience",
                "creation_date": "2024-11-20",
                "last_modified_date": "2024-11-21",
                "file_type": "markdown",
                "word_count": 28,
            },
        ),
        LIDocument(
            text="一片高……",
            metadata={
                "filename": "风起长空场景.md",
                "category": "游戏场景",
                "file_path": "/data/黑悟空/风起长空场景.md",
                "author": "GameScience",
                "creation_date": "2024-11-20",
                "last_modified_date": "2024-11-21",
                "file_type": "markdown",
                "word_count": 28,
            },
        ),
    ]
    # 打印每个文档的元数据
    for doc in docs_li:
        print(f"[2B] Metadata for {doc.metadata['filename']}:")
        for key, value in doc.metadata.items():
            print(f"    {key}: {value}")
        print("-" * 40)

    # C. 仅加载某一个特定文件
    r2 = SimpleDirectoryReader(input_files=[os.path.join(script_dir, 'txt', 'wiki.txt')])
    d2 = r2.load_data()
    print(f"[2C] input_files 指定单文件：文档数量 = {len(d2)}")
except ImportError:
    print("[2] 本环境未装 llama-index，LlamaIndex 部分跳过")
