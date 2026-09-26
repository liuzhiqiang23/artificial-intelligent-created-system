# 老师 0924.zip 原版适配 Windows（代码未改）
from llama_index.readers.file.pymu_pdf import PyMuPDFReader
pdf_reader = PyMuPDFReader()
# docs=pdf_reader.load_data(
#     file_path="./files/05.pdf"
# )
from llama_index.core import SimpleDirectoryReader
reader = SimpleDirectoryReader(
    input_dir='./files',
    recursive=True,
    required_exts=[".pdf"],
    file_extractor={".pdf": pdf_reader}
)
docs = reader.load_data()

print(f"文档数量: {len(docs)}")
for doc in docs:
    print(doc.text[:30])
    print(doc.metadata["file_path"])
    print("=" * 30)
