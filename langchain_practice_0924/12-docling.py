# -*- coding: utf-8 -*-
# 笔记1008 第5节：Docling 库（Word 转换免模型；PDF 需先 docling-tools models download 1-2G，此处从简）
import os
from typing import List
script_dir = os.path.dirname(__file__)
F = os.path.join(script_dir, 'file1008')

from docling.document_converter import DocumentConverter

# ---------- 8) Word 转换：不需要配置模型路径，DocumentConverter() 裸建即可 ----------
converter = DocumentConverter()
result = converter.convert(os.path.join(F, 'intro.docx'))   # 也支持 pptx/xlsx，必须 docx/pptx 新格式
print("[8] Word 转换 export_to_text:")
print(result.document.export_to_text())
print("=" * 50)

# ---------- D. 自定义批量转换方法（笔记推荐写法，LlamaIndex Document 版） ----------
from llama_index.core import Document

def load_pdfs_with_docling(input_dir: str, docling_converter: DocumentConverter) -> List[Document]:
    """使用配置好的 Docling 转换器加载文件（逐文件 try/except 容错）"""
    documents = []
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.docx', '.pptx', '.xlsx')):
            file_path = os.path.join(input_dir, filename)
            try:
                result = docling_converter.convert(file_path)
                text = result.document.export_to_text()
                doc = Document(
                    text=text,
                    metadata={
                        "file_name": filename,
                        "file_path": file_path,
                        "pages": len(result.document.pages),
                    },
                )
                documents.append(doc)
                print(f"✅{filename}")
            except Exception as e:
                print(f"❌{filename}: {e}")
    return documents

documents = load_pdfs_with_docling(F, converter)
print(f"成功加载 {len(documents)} 个文档")

# ---------- 7) LangChain 版：Docling 解析 → langchain Document ----------
result = converter.convert(os.path.join(F, 'intro.docx'))
txt = result.document.export_to_text()
from langchain_core.documents import Document as LCDocument
doc = LCDocument(page_content=txt)
print(f"[7] LangChain 版: page_content 前40字 {doc.page_content[:40]!r}")
print()
print("""
PDF 版笔记要点（考场口答）：
  converter = DocumentConverter(format_options={InputFormat.PDF:
      PdfFormatOption(pipeline_options=pipeline_options)})
  pipeline_options = PdfPipelineOptions()
  pipeline_options.artifacts_path = 本地模型路径   # docling-tools models download 下载(1-2G)
  doc = converter.convert("file/05.pdf").document
  print(doc.export_to_markdown())   # 另有 export_to_text / export_to_html
LlamaIndex 集成：DoclingReader(pipeline_options=...) 或 DoclingReader(converter=...)
图片识别：TesseractOcrOptions(lang=["chi_sim","eng"])，但效果不如直接 tesseract 命令（笔记原话）
""")
