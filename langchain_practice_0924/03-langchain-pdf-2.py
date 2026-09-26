# 老师 0924.zip 原版适配 Windows（代码未改；unstructured 已钉 0.18.32，Py3.10 不能装 0.20.x）
# Poppler 已部署：D:\poppler\poppler-25.12.0\Library\bin（已加入用户 PATH）
from langchain_community.document_loaders import UnstructuredPDFLoader
loader = UnstructuredPDFLoader('./files/05.pdf',
    mode="elements",  # 单文档single，另有"elements"（按元素）、"paged"（按页）
    languages=["chi_sim","eng"],
    strategy="fast" ##快速模式，不下载解析模型，另有hi_res，需要从Huggingface下载，一般无法下载成功
)
docs = loader.load()
print(f"加载了 {len(docs)} 个文档")
for doc in docs[:10]:
    print(doc.page_content[:30])
    print(doc.metadata)
    print("="*30)
