# -*- coding: utf-8 -*-
# PDF 加载 3：Unstructured 三种用法（对照《笔记0924.pdf》2-3）
# 依赖：pip install langchain_unstructured + pip install "unstructured[pdf]"（本项目 unstructured 已钉 0.18.32，Py3.10 不能装 0.20.x）
# Poppler 已部署：D:\poppler\poppler-25.12.0\Library\bin（已加入用户 PATH）
import os
script_dir = os.path.dirname(__file__)
PDF = os.path.join(script_dir, 'file', '05.pdf')

# ---------- D. 示例代码1：UnstructuredPDFLoader ----------
from langchain_community.document_loaders import UnstructuredPDFLoader
loader = UnstructuredPDFLoader(
    PDF,
    mode="single",                    # 单文档，另有 "elements"（按元素）、"paged"（按页）
    languages=["chi_sim", "eng"],
    strategy="fast",                  # 快速模式不下载解析模型；hi_res 需要从 Huggingface 下载（一般下不动）
)
docs = loader.load()
print(f"[D] UnstructuredPDFLoader 加载了 {len(docs)} 个文档")

# ---------- E. 示例代码2：UnstructuredLoader（lazy_load） ----------
from langchain_unstructured import UnstructuredLoader
loader2 = UnstructuredLoader(file_path=PDF, strategy="fast")
docs2 = []
for doc in loader2.lazy_load():       # 懒加载：处理时才读，适合大文档
    docs2.append(doc)
print(f"[E] UnstructuredLoader 加载了 {len(docs2)} 个文档（lazy_load）")

# ---------- F. 示例代码3：unstructured 的 partition ----------
from unstructured.partition.auto import partition
elements = partition(filename=PDF, content_type="application/pdf", languages=["chi_sim", "eng"])
print("\n[F] PDF 解析后的前 5 个 Elements 类型:")
for i, element in enumerate(elements[:5]):
    print(f"\nElement {i+1}:")
    print(f"类型: {type(element).__name__}")
    print(f"内容: {str(element)[:60]}")
    print("-" * 50)
element_types = {}
for element in elements:
    element_type = type(element).__name__
    element_types[element_type] = element_types.get(element_type, 0) + 1
print("Elements 类型统计:")
for element_type, count in element_types.items():
    print(f"{element_type}: {count}个")
