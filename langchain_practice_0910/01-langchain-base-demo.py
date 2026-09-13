# -*- coding: utf-8 -*-
# 实践4：使用 LangChain（对照《笔记0910.pdf》第4节）
# 如果使用WebBaseLoader加载网页数据，需配置下列浏览器代理
import os
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"

# 引入依赖
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# 创建嵌入模型，使用本地bge（Windows 路径，本机 HF 缓存已有）
embed_model = HuggingFaceEmbeddings(
    model_name=r"C:\Users\Lenovo\.cache\huggingface\hub\models--BAAI--bge-small-zh-v1.5\snapshots\7999e1d3359715c523056ef9478215996d62a620",
    model_kwargs={'device': 'cpu'},  # cuda-nvidia显卡  mps-苹果M系列  cpu-其它
    encode_kwargs={'normalize_embeddings': True}
)
# 创建本地生成模型
llm = ChatOllama(
    model="deepseek-r1:latest",  # Ollama使用的模型名称
    temperature=0.7,             # 控制输出的随机性
    max_tokens=2048              # 最大输出长度
)

# 网站爬取方式：如果网站反爬机制导致无法获取，使用后面的TextLoader替代
# loader = WebBaseLoader(
#     web_paths=("https://baike.sogou.com/v192487187.htm?ch=frombaikevr&fromTitle=黑神话：悟空",)
# )
# docs = loader.load()
# 本地文本文件加载方式（Windows 下必须显式 utf-8，否则按 GBK 解码报错）
loader = TextLoader(file_path="./txt/wiki.txt", encoding="utf-8")
docs = loader.load()
print(f"文档加载成功，字符数: {len(docs[0].page_content)}")

# 文件分块，采用1000作为块大小，并设置重复数据为200（一般在10%-20%之间）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)
print(f"切分为 {len(all_splits)} 个文本块")

# 向量存储：使用内存方式，无持久化
vector_store = InMemoryVectorStore(embed_model)
vector_store.add_documents(all_splits)

# 提问，并根据问题查询内存向量中最相关的3个数据块
question = "详细介绍一下黑神话：悟空"
retrieved_docs = vector_store.similarity_search(
    question, k=3)
docs_content = "\n\n".join(
    doc.page_content for doc in retrieved_docs)

# 构建提示词模板
prompt = ChatPromptTemplate.from_template("""
                基于以下上下文，回答问题。如果上下文中没有相关信息，
                请说"我无法从提供的上下文中找到相关信息"。
                上下文: {context}
                问题: {question}
                回答:""")

# 将问题、上下文传入提示词模板对象，并交给LLM生成回答
answer = llm.invoke(prompt.format(
    question=question, context=docs_content))
print(answer.content)
