# -*- coding: utf-8 -*-
# 图片 OCR 1：LangChain 三路 OCR（对照《笔记0924.pdf》3-1）
# 依赖：pip install pytesseract pillow；OCR 引擎 tesseract 已系统安装（v5.4.0，含 chi_sim/eng 语言包）
import os
from typing import List

# 语言包目录（本机语言包在 D 盘，不设此项时 tesseract 只认自带英文字包）
os.environ.setdefault('TESSDATA_PREFIX', r'D:\tesseract-data')

script_dir = os.path.dirname(__file__)
SALES = os.path.join(script_dir, 'imgs', 'sales.jpg')
ENG = os.path.join(script_dir, 'imgs', 'eng.jpg')

# ---------- D. 代码：直接使用 tesseract ----------
import pytesseract as pt
from PIL import Image
# 指定 tesseract 的完整路径（Windows 已配置 PATH 时此行可省，写全最稳）
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Windows 用户：把 tesseract 所在目录加入 PATH（对应任务书 Mac 版的 os.environ['PATH'] += ':/opt/homebrew/bin'）
# 说明：UnstructuredImageLoader 内部调用的是 PATH 里的 tesseract 命令，不读上面的 tesseract_cmd
os.environ['PATH'] += r';C:\Program Files\Tesseract-OCR'
image = Image.open(SALES)
text = pt.image_to_string(image, lang='chi_sim+eng')  # 识别中文+英文
print("[D] pytesseract 直接识别结果:")
print(text.strip())
print("=" * 50)

# ---------- E. 代码：使用 UnstructuredImageLoader ----------
from langchain_community.document_loaders import UnstructuredImageLoader
loader = UnstructuredImageLoader(
    file_path=ENG,
    strategy="ocr_only",              # 关键参数：仅 OCR，不下载模型
    languages=["chi_sim", "eng"],     # 指定 OCR 语言
)
docs = loader.load()
print(f"[E] UnstructuredImageLoader 加载了 {len(docs)} 个文档")
print(f"    识别前60字: {docs[0].page_content[:60]!r}")
print("=" * 50)

# ---------- G. 自定义 TesseractLoader（任务书完整版） ----------
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class TesseractLoader(BaseLoader):
    def __init__(self, file_paths: List[str] = None, lang: str = 'chi_sim+eng', config: str = '--psm 6'):
        self.lang = lang
        self.config = config
        self.file_paths = file_paths

    def load(self) -> List[Document]:
        if self.file_paths is None or len(self.file_paths) == 0:
            raise ValueError("请提供图片文件路径列表。")
        for file_path in self.file_paths:
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                raise ValueError(f"图片文件[{file_path}]不存在。")
            if not (file_path.endswith('.jpg') or file_path.endswith('.png')):
                raise ValueError(f"文件[{file_path}]格式不支持。")
        documents = []
        for file_path in self.file_paths:
            try:
                with Image.open(file_path) as img:
                    text = pt.image_to_string(img, lang=self.lang, config=self.config)
                    cleaned_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
                    doc = Document(
                        page_content=cleaned_text,
                        metadata={"file_name": os.path.basename(file_path)},
                    )
                    documents.append(doc)
            except Exception as e:
                print(f"处理图片 {file_path} 时出错: {e}")
        return documents


if __name__ == "__main__":
    loader = TesseractLoader([os.path.join(script_dir, 'imgs', 'img1.png')])
    documents = loader.load()
    for doc in documents:
        print("[G] TesseractLoader 自定义类结果:")
        print(doc.page_content)
        print(doc.metadata)
        print("= " * 50)
