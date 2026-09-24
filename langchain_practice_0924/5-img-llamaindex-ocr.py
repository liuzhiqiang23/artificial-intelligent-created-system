# -*- coding: utf-8 -*-
# 图片 OCR 2：LlamaIndex 自定义 TesseractReader + 检索问答（对照《笔记0924.pdf》3-2）
# 思路同 LangChain 的 TesseractLoader，改为继承 LlamaIndex 的 BaseReader
import os
from typing import List

os.environ.setdefault('TESSDATA_PREFIX', r'D:\tesseract-data')
script_dir = os.path.dirname(__file__)

from PIL import Image
import pytesseract as pt
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document


class TesseractReader(BaseReader):
    """继承 LlamaIndex BaseReader，把图片 OCR 成 Document 列表"""

    def __init__(self, lang: str = 'chi_sim+eng', config: str = '--psm 6'):
        self.lang = lang
        self.config = config

    def load_data(self, file_paths: List[str] = None, **kwargs) -> List[Document]:
        documents = []
        for file_path in file_paths or []:
            try:
                with Image.open(file_path) as img:
                    text = pt.image_to_string(img, lang=self.lang, config=self.config)
                    cleaned_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
                    documents.append(
                        Document(text=cleaned_text,
                                 metadata={"file_name": os.path.basename(file_path)})
                    )
            except Exception as e:
                print(f"处理图片 {file_path} 时出错: {e}")
        return documents


if __name__ == "__main__":
    # 1. 初始化 Tesseract 读取器
    reader = TesseractReader()
    # 2. 指定图片所在文件夹，获取文件夹下常见格式图片的路径
    image_folder = os.path.join(script_dir, 'imgs')
    image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder)
                   if f.lower().endswith(('.png', '.jpg'))]
    # 3. 执行 OCR 操作并生成 LlamaIndex 的 Document 对象列表
    documents = reader.load_data(image_paths)
    print(f"OCR 完成，共 {len(documents)} 个文档：")
    for doc in documents:
        print(f"  [{doc.metadata['file_name']}] {doc.text[:50]!r}")

    # 4. 创建嵌入模型（BGE）+ 运行查询（参照之前课示例）
    from llama_index.core import VectorStoreIndex, Settings
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    Settings.embed_model = HuggingFaceEmbedding(
        model_name=r"C:\Users\Lenovo\.cache\huggingface\hub\models--BAAI--bge-small-zh-v1.5\snapshots\7999e1d3359715c523056ef9478215996d62a620",
        device='cpu',
    )
    index = VectorStoreIndex.from_documents(documents)
    retriever = index.as_retriever(similarity_top_k=2)
    question = "华东区销售额是多少？"
    nodes = retriever.retrieve(question)
    print(f"\n检索问题: {question}")
    for n in nodes:
        print(f"  命中[{n.metadata['file_name']}]: {n.text[:40]!r}")
