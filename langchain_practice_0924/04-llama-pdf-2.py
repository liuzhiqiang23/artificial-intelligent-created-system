# 老师 0924.zip 原版适配 Windows（代码未改）
# 注：老师真素材的 05.pdf 拆分会得到 224 个文档；本机用笔记0917.pdf 顶替，数量会不同
from llama_index.readers.file.unstructured import UnstructuredReader
from pathlib import Path
# 1. 初始化加载器
loader = UnstructuredReader()
# 2. 加载整个文件为一个文档 (split_documents=False)
# doc = loader.load_data(
# 	file=Path('./files/05.pdf'), split_documents=False)
# print(f"加载了 {len(doc)} 个文档")
# 输出: 加载了 1 个文档
# 3. 将文件按逻辑结构拆分为多个文档 (split_documents=True)，适用于长文档，希望保留其内部逻辑结构进行索引。
docs = loader.load_data(
		file=Path('./files/05.pdf'), split_documents=True,
		unstructured_kwargs={"languages":["chi_sim","eng"]})
print(f"拆分后得到 {len(docs)} 个文档")
# 输出: 拆分后得到 224 个文档
# unstructured_kwarg参数用于指定文档内容的语言等参数
