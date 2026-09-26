# 老师 0924.zip 原版适配 Windows（代码未改，仅保留原注释；相对路径以项目根为工作目录）
from langchain_community.document_loaders import PyPDFLoader

# loader = PyPDFLoader(["./files/01.pdf","./files/05.pdf"])
# docs = loader.load()  # 返回 List[Document]

from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader(
    path="./",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)
docs = loader.load()
print(len(docs))
for doc in docs:
    print(doc.page_content[:30])
    print(doc.metadata["source"])
    print("="*30)
