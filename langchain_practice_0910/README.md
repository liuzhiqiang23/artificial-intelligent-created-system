# LangChain / LangGraph 实践（2026-09-10 + 2026-09-17 任务书）

> 《笔记0910.pdf》第 4-6 节：**实践4 使用 LangChain → 实践5 使用 LangGraph → 实践6 无框架自选向量数据库（faiss / zvec）**。
> 《笔记0917.pdf》第三节：**数据导入（LangChain 四种加载方式 + LlamaIndex SimpleDirectoryReader）**。
> 本目录代码已在 Windows + RTX 3050 (4GB) 笔记本上**全部实测跑通**。

## 环境（已验证的版本组合）

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | **3.10.11** | 任务书指定 3.10 虚拟环境（勿用 3.13/3.14） |
| langchain-community | 0.4.1 | Web 加载、文档分割 |
| langchain-huggingface | 1.2.0 | LangChain 嵌入模型 |
| langchain-ollama | 1.0.1 | Ollama 大模型支持 |
| sentence-transformers | 5.2.3 | 依赖 transformers 4.57.6 |
| langgraph | 1.2.11 | 有状态多智能体编排 |
| langchain-classic | 1.0.8 | 提供 `langchain_classic.hub` |
| faiss-cpu | 1.15.0 | 实践6 向量库方案一 |
| zvec | 0.7.0 | 实践6 向量库方案二 |
| llama-index-core | 最新 | 0917 数据导入实践（SimpleDirectoryReader） |
| torch | 2.14.0 (CPU) | sentence-transformers 依赖 |
| Ollama 模型 | deepseek-r1:latest (7B, 5.2GB) + 本地 BGE-small-zh-v1.5 嵌入 | |

## 文件结构

```
langchain_practice_0910/
├── 01-langchain-base-demo.py      # 实践4：WebBaseLoader/TextLoader → 分块 → BGE嵌入 → InMemoryVectorStore → ChatOllama
├── 02-langchain-langgraph-demo.py # 实践5：TextLoader → 300/30分块 → hub提示词 → StateGraph(retrieve→generate)
├── 03-faiss-demo.py               # 实践6A：sentence-transformers + faiss IndexFlatL2 + 出处编号
├── 04-zvec-demo.py                # 实践6B：zvec Schema/Collection/insert/query（任务书允许沿用BGE）
├── 05-data-loading-demo.py        # 0917：TextLoader/Document/DirectoryLoader + LlamaIndex SimpleDirectoryReader/元数据
└── txt/wiki.txt                   # 黑神话：悟空本地语料（sogou 百科页）
```

## 运行

```bash
# 1. 启动 Ollama 并确认模型
ollama list        # 需有 deepseek-r1:latest

# 2. 激活 3.10 虚拟环境后，在本目录下运行
python 01-langchain-base-demo.py   # 实践4
python 02-langchain-langgraph-demo.py  # 实践5
python 03-faiss-demo.py            # 实践6 faiss+BGE
python 04-zvec-demo.py             # 实践6 zvec+BGE
python 05-data-loading-demo.py     # 0917 数据导入（秒级，不依赖大模型）
```

实测输出要点：
- 02 运行打印 `生成了 39 个文本块`（chunk 300/30）
- 03/04 运行打印 `文档向量维度: (5, 512)`（BGE-small-zh 是 512 维）
- 检索命中后由 deepseek-r1 生成带出处编号的回答；r1 会先输出 `<think>` 思考过程再给答案

## Mac 示例代码 → Windows 适配踩坑记录（重点）

1. **嵌入模型路径**：`/Users/will/.cache/huggingface/hub/models--BAAI--bge-small-zh-v1.5` 改为本机 HF 缓存快照的 Windows 绝对路径；`device` 从 `mps` 改 `cpu`。
2. **TextLoader 必须 `encoding="utf-8"`**：Windows 默认按 GBK 解码，中文 wiki 直接 UnicodeDecodeError。
3. **生成模型**：示例里的 `openbmb/minicpm5-2b` 按任务书改为 `deepseek-r1:latest`；4GB 显存装不下 7B 全量，Ollama 会自动 GPU+CPU 混合推理，纯 CPU 速度也可接受。
4. **hub.pull 被禁**：langchain-classic 1.0.8 默认禁止拉取公共 prompt（安全策略），代码用 try/except 兜底——失败时以**内容完全相同**的本地 `ChatPromptTemplate` 顶上，不影响输出。
5. **zvec 的 `VectorQuery`** 有 DeprecationWarning（未来版本将改名 `Query`），当前版本可用。
6. **zvec+MiniLM 变体**：任务书允许嵌入"使用之前的 BGE"，故 04 直接用 BGE；如需 all-MiniLM-L6-v2，改 `SentenceTransformer('all-MiniLM-L6-v2')` 首次联网下载即可。
7. **LangSmith 监控**（任务书 5.3 可选）：老师示例里的 API Key 是演示 Key，已置 `LANGSMITH_TRACING=false`；需要时在 smith.langchain.com 注册自己的账号换 Key。
8. **Windows 控制台中文**：运行前 `set PYTHONIOENCODING=utf-8`（PyCharm 运行一般不需要）。
9. **DirectoryLoader 默认报错**（0917）：默认基于 unstructured 库会 `ModuleNotFoundError`，纯文本目录用 `loader_cls=TextLoader` + `loader_kwargs={"encoding": "utf-8"}` 绕开。
10. **LlamaIndex 与 LangChain 的属性名不同**（0917 考点）：llama_index 的 Document 内容在 `text` 属性，LangChain 在 `page_content`；`os.path.dirname(__file__)` 在 Jupyter 里不可用（无 `__file__`）。

## 环境部署要点（本机）

- Python 3.10.11 装在 `D:\Python310`，虚拟环境在 `D:\pyenvs\0910-venv`（PyCharm 解释器名 "Python 3.10"）
- BGE 嵌入模型用 HuggingFace 本地缓存，路径见 01 脚本内注释
- 运行依赖 Ollama 服务（11434 端口）；`deepseek-r1` 约 5.2GB，`ollama pull deepseek-r1:latest` 获取
