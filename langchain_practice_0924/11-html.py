# -*- coding: utf-8 -*-
# 笔记1008 第4-4节：HTML 文件加载（本地文件演示；在线 WebBaseLoader 考场断网慎用）
import os
script_dir = os.path.dirname(__file__)
HTML = os.path.join(script_dir, 'file1008', 'index.html')

# ---------- A. LangChain ----------
# 在线：WebBaseLoader（见笔记；另有 RecursiveUrlLoader 递归抓取、
#       SeleniumURLLoader / PlaywrightURLLoader 应对 AJAX 动态页）
# 本地方式一：UnstructuredHTMLLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
loader = UnstructuredHTMLLoader(HTML, mode='single', strategy='fast')
docs = loader.load()
print(f"[A-1] UnstructuredHTMLLoader: {len(docs)} 个文档")
print(f"      前50字: {docs[0].page_content[:50]!r}")

# 本地方式二：BSHTMLLoader（基于 BeautifulSoup）
from langchain_community.document_loaders import BSHTMLLoader
loader = BSHTMLLoader(HTML, open_encoding='utf-8')  # 指定文件编码
docs = loader.load()
print(f"[A-2] BSHTMLLoader: {len(docs)} 个文档")

# ---------- B. LlamaIndex ----------
# SimpleWebPageReader（需 llama-index-readers-web）：html_to_text=True 去标签；支持 URL 与本地
from llama_index.core import SimpleDirectoryReader, Document
documents = SimpleDirectoryReader(input_files=[HTML]).load_data()  # 未去除 HTML 标签
# 用 BeautifulSoup 去标签
from bs4 import BeautifulSoup
documents = [Document(text=BeautifulSoup(doc.text, 'html.parser').get_text(separator='\n', strip=True)) for doc in documents]
print(f"[B-1] BeautifulSoup 清洗: {len(documents)} 个文档, 前40字 {documents[0].text[:40]!r}")

# 用 html2text 转成 Markdown 风格纯文本
import html2text
h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True
documents = SimpleDirectoryReader(input_files=[HTML]).load_data()
documents = [Document(text=h.handle(doc.text)) for doc in documents]
print(f"[B-2] html2text 转换: {len(documents)} 个文档")
print(documents[0].text[:120])
# 另有 HTMLTagReader（取指定标签）与 HTMLNodeParser（切块用），见笔记说明
