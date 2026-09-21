# -*- coding: utf-8 -*-
# 4-llama-reader：LlamaIndex SimpleDirectoryReader（老师代码 Windows 适配版）
# 内容在 Document 的 text 属性（LangChain 是 page_content，考点）
import os
script_dir = os.path.dirname(__file__)

from llama_index.core import SimpleDirectoryReader
# dir_reader = SimpleDirectoryReader(input_dir=os.path.join(script_dir,'file'))
# dir_reader = SimpleDirectoryReader(input_dir=os.path.join(script_dir,'file'), required_exts=[".txt"])
dir_reader = SimpleDirectoryReader(
    input_files=[os.path.join(script_dir, 'file', 'wiki.txt')]
)
docs = dir_reader.load_data()
print(f"文档数：{len(docs)}")  # 输出文档总数
for doc in docs:
    print(doc.text[:100])
    print("=" * 40)
