# -*- coding: utf-8 -*-
# 笔记1008 第4-2节：Office 文件加载（Word/PPT/Excel，对照原文）
# 说明：Unstructured 的 Office 加载器底层调用 LibreOffice（环境变量 UNSTRUCTURED_LIBREOFFICE_PATH
#       或 PATH 中的 soffice）。LibreOffice 未就绪时走 LlamaIndex 路线（python-docx/python-pptx 直读，无需 LibreOffice）。
import os
script_dir = os.path.dirname(__file__)
F = os.path.join(script_dir, 'file1008')

# ---------- C. LangChain：Unstructured 三 loader（需 LibreOffice）----------
libre_ok = os.environ.get('UNSTRUCTURED_LIBREOFFICE_PATH') or any(
    os.path.exists(os.path.join(p, 'soffice.exe'))
    for p in os.environ.get('PATH', '').split(os.pathsep)
)
if libre_ok:
    from langchain_community.document_loaders import (
        UnstructuredPowerPointLoader, UnstructuredWordDocumentLoader, UnstructuredExcelLoader)
    loader = UnstructuredPowerPointLoader(os.path.join(F, 'test.pptx'), mode='paged')  # 同有 single(默认)/elements
    docs = loader.load()
    print(f"[C] UnstructuredPowerPointLoader: {len(docs)} 个文档(paged)")
    loader = UnstructuredWordDocumentLoader(os.path.join(F, 'intro.docx'), mode='elements')
    docs = loader.load()
    print(f"[C] UnstructuredWordDocumentLoader: {len(docs)} 个文档(elements)")
    loader = UnstructuredExcelLoader(os.path.join(F, 'course.xls'), mode='elements')
    docs = loader.load()
    for doc in docs:
        print(doc.page_content); print(doc.metadata); print('=' * 50)
else:
    print("[C] LibreOffice 未配置，跳过 Unstructured Office 路线（用下面的 LlamaIndex 路线作答）")

# ---------- D. LlamaIndex：专用读取器（无需 LibreOffice，考试保底路线）----------
from llama_index.readers.file.docs import DocxReader
documents = DocxReader().load_data(file=os.path.join(F, 'intro.docx'))
print(f"[D] DocxReader: {len(documents)} 个文档, 前30字 {documents[0].text[:30]!r}")

from llama_index.readers.file.slides import PptxReader
documents = PptxReader().load_data(os.path.join(F, 'test.pptx'))
print(f"[D] PptxReader: {len(documents)} 个文档, 前30字 {documents[0].text[:30]!r}")

# Excel 用 DoclingReader（若 docling 未装则提示）；批量版 SimpleDirectoryReader + file_extractor
try:
    from llama_index.readers.docling import DoclingReader
    documents = DoclingReader().load_data(os.path.join(F, 'course.xlsx'))
    print(f"[D] DoclingReader(xlsx): {len(documents)} 个文档")
except Exception as e:
    print(f"[D] DoclingReader(xlsx) 不可用: {type(e).__name__}（xlsx 也可用 openpyxl 手动读）")
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(F, 'course.xlsx'))
    ws = wb.active
    print(f"    [兜底 openpyxl] 表: {ws.title}, {ws.max_row}行 x {ws.max_column}列")

# 批量加载：file_extractor 指定各格式用哪个读取器
from llama_index.core import SimpleDirectoryReader
extractor = {'.docx': DocxReader(), '.pptx': PptxReader()}
try:
    from llama_index.readers.docling import DoclingReader
    extractor['.xlsx'] = DoclingReader()
except Exception:
    pass
reader = SimpleDirectoryReader(input_dir=F, required_exts=list(extractor.keys()),
                               file_extractor=extractor)
documents = reader.load_data()
print(f"[D] SimpleDirectoryReader 批量: {len(documents)} 个文档")
