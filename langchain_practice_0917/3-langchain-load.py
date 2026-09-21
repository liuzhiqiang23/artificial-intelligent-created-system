# -*- coding: utf-8 -*-
# 3-langchain-load：DirectoryLoader 加载目录（老师代码 Windows 适配版）
# 需先运行 4-llama-reader 同款 file 目录：./file/ 下有 wiki.txt（+ 示意 png/pdf 用于演示 exclude）
import os
script_dir = os.path.dirname(__file__)
file_dir = os.path.join(script_dir, 'file')

from langchain_community.document_loaders import DirectoryLoader, TextLoader
# 老师原版（默认 unstructured 加载器，环境未装会报 ModuleNotFoundError）：
# loader = DirectoryLoader(path='./file', exclude=["*.png","*.pdf"])
# 任务书说明①：纯文本用 loader_cls 指定 TextLoader，并用 glob/exclude 控制文件类型
loader = DirectoryLoader(
    path=file_dir,
    glob="*",
    exclude=["*.png", "*.pdf"],
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)
docs = loader.load()
print(f"文档数：{len(docs)}")  # 输出文档总数
print(docs[0].page_content[:30])
