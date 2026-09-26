# 老师 0924.zip 原版适配 Windows：tesseract 路径 Mac → Windows（其余未改）
# 本脚本故意传入不能识别的 01.pdf 和不存在的 abc.jpg，演示 try/except 逐文件容错
from langchain_core.document_loaders import BaseLoader
from typing import List
from langchain_core.documents import Document
from PIL import Image
import pytesseract as pt
# Mac 原版：pt.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TesseractLoader(BaseLoader):
    def __init__(self, file_paths: List[str],
                 lang: str = "chi_sim+eng", config: str = "--psm 3"):
        self.file_paths = file_paths
        self.lang = lang
        self.config = config

    def load(self) -> List[Document]:
        docs=[]
        for file_path in self.file_paths:
            try:
                with  Image.open(file_path) as img:
                    txt=pt.image_to_string(img,lang=self.lang,config=self.config)
                    doc=Document(
                        page_content=txt,
                        metadata={"source": file_path}
                    )
                    docs.append(doc)
            except Exception as e:
                print(f"文件【{file_path}】出错了：{e}")
        return docs


if __name__ == '__main__':
    loader = TesseractLoader(
        ["./files/01.png","./files/02.jpg",
         "./files/01.pdf","./files/abc.jpg"])
    docs=loader.load()
    print(len(docs))
    for doc in docs:
        print(doc.page_content[:30])
        print(doc.metadata["source"])
        print("=" * 30)
