# -*- coding: utf-8 -*-
# 实践5：使用 LangGraph（对照《笔记0910.pdf》第5节）
import os
import warnings
# 屏蔽 hub.pull 的弃用警告（新版 LangChain 提示该写法将迁移到 LangSmith SDK，不影响功能）
try:
    from langchain_core._api.deprecation import LangChainDeprecationWarning
    warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
except Exception:
    warnings.filterwarnings("ignore", category=DeprecationWarning)
# LangSmith 监控（可选）：老师示例里的 key 是演示用的，本地运行不需要联网监控，
# 需要启用时在 https://smith.langchain.com 注册自己的账号并换成自己的 API Key
os.environ["LANGSMITH_TRACING"] = "false"
# os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
# os.environ["LANGSMITH_API_KEY"] = "你的API Key"
# os.environ["LANGSMITH_PROJECT"] = "0910LangChain"

# 引入依赖
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import ChatOllama

# 创建嵌入模型，使用本地bge（Windows 路径，本机 HF 缓存已有）
embed_model = HuggingFaceEmbeddings(
    model_name=r"C:\Users\Lenovo\.cache\huggingface\hub\models--BAAI--bge-small-zh-v1.5\snapshots\7999e1d3359715c523056ef9478215996d62a620",
    model_kwargs={'device': 'cpu'},  # cuda  mps  cpu
    encode_kwargs={'normalize_embeddings': True}
)
# 创建本地生成模型
llm = ChatOllama(
    model="deepseek-r1:latest",
    temperature=0.7,
    max_tokens=2048
)

# 加载文件（本地文件）
loader = TextLoader('./txt/wiki.txt', encoding="utf-8")
docs = loader.load()

# 分割文件（与实践4相同，分块参数不同）
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
chunks = splitter.split_documents(docs)
print(f"生成了 {len(chunks)} 个文本块")

# 创建向量存储
vector_store = InMemoryVectorStore(embed_model)
vector_store.add_documents(chunks)

# 定义RAG提示词（采用新方式）
try:
    from langchain_classic import hub
    prompt = hub.pull("rlm/rag-prompt")
except Exception as e:
    # 拉取 LangChain Hub 失败（网络原因）时，使用与 rlm/rag-prompt 完全相同的模板内容
    print(f"[提示] hub.pull 失败({e})，使用本地相同模板")
    from langchain_core.prompts import ChatPromptTemplate
    prompt = ChatPromptTemplate.from_template(
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, just say that you don't know. "
        "Use three sentences maximum and keep the answer concise.\n"
        "Question: {question}\n"
        "Context: {context}\n"
        "Answer:"
    )

# 自定义应用状态类
from typing import List
from typing_extensions import TypedDict
from langchain_core.documents import Document

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

# 定义检索步骤
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

# 定义生成步骤
def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

# 构建和编译应用
from langgraph.graph import START, StateGraph
graph = (
    StateGraph(State)
    .add_sequence([retrieve, generate])
    .add_edge(START, "retrieve")
    .compile()
)

# 运行查询
question = "黑悟空有哪些游戏场景？"
response = graph.invoke({"question": question})
print(f"问题: {question}")
print(f"答案: {response['answer']}")
