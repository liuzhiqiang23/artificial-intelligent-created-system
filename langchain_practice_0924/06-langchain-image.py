# 老师 0924.zip 原版适配 Windows：补一行把 tesseract 加入 PATH
# 说明：UnstructuredImageLoader 内部调用的是 PATH 里的 tesseract 命令，不读 tesseract_cmd
# （对应任务书 Mac 版的 os.environ['PATH'] += ':/opt/homebrew/bin'）
import os
os.environ['PATH'] += r';C:\Program Files\Tesseract-OCR'

from langchain_community.document_loaders import UnstructuredImageLoader
loader = UnstructuredImageLoader('./files/02.jpg',
    languages=["chi_sim","eng"],
    strategy="ocr_only" ##快速模式，不下载解析模型，另有hi_res，需要从Huggingface下载，一般无法下载成功
)
docs = loader.load()
print(f"加载了 {len(docs)} 个文档")
print(docs[0].page_content)
