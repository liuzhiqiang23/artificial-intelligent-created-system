# 数据导入实践（2026-09-17 任务书）

> 对照《笔记0917.pdf》：**faiss+BGE 检索问答 → zvec+MiniLM 存/查 → LangChain DirectoryLoader → LlamaIndex SimpleDirectoryReader**。
> Windows + RTX 3050 (4GB) 笔记本全部实测跑通（2026-09-20）。

## 文件结构

```
langchain_practice_0917/
├── 1-faiss-bge.py            # faiss IndexFlatL2 + BGE 检索 → Ollama 生成带出处答案
├── 2-zvec-minilm-save.py     # MiniLM 嵌入 9 段黑悟空语料 → zvec 建库存储（必须先跑）
├── 2-zvec-minilm-search.py   # 打开 zvec 库 + 交互问答（与 save 必须同一嵌入模型）
├── 3-langchain-load.py       # DirectoryLoader 加载目录（exclude 演示 png/pdf）
├── 4-llama-reader.py         # SimpleDirectoryReader（内容在 text 属性，考点）
└── file/                     # 语料目录（老师 zip 未带，自建：wiki.txt + 示意 png/pdf）
```

## 运行顺序

```bash
python 1-faiss-bge.py           # 检索+生成（约2-4分钟，含模型加载）
python 2-zvec-minilm-save.py    # 先建库（秒级）
python 2-zvec-minilm-search.py  # 后交互查询（输入问题，exit 退出）
python 3-langchain-load.py      # 秒级
python 4-llama-reader.py        # 秒级
```

依赖：与 `langchain_practice_0910` 共用环境（Python 3.10 + 0910-venv），另需 `pip install llama-index-core ollama`；Ollama 服务需有 deepseek-r1:latest。

## Mac 示例代码 → Windows 适配点

1. **嵌入模型路径**：老师 modelscope 缓存路径（`/Users/will/.cache/modelscope/...`）改为本机 HuggingFace 缓存快照绝对路径；MiniLM 首次下载直连 hf.co 不通时，设 `HF_ENDPOINT=https://hf-mirror.com` 走国内镜像。
2. **生成模型**：`openbmb/minicpm5-2b` 本机未拉取，按 0910 惯例改 `deepseek-r1:latest`。
3. **DirectoryLoader 默认加载器**：任务书说明①的绕法（`loader_cls=TextLoader` + `encoding`）保底可用；**本机已装 `unstructured` 0.18.32 + `pypdf` + `python-magic-bin`，老师原版（默认 unstructured 加载器）也已实测跑通**。⚠️ Windows 坑：只装 `python-magic` 缺 libmagic DLL 时 `import unstructured.partition.auto` 会**无报错挂死**，装 `python-magic-bin`（自带 DLL）即好；nltk 数据用 `punkt_tab`（已随包就位）。
4. **zvec 重跑**：`create_and_open` 要求路径不存在，save 脚本已内置清理；insert/query 的 DeprecationWarning 用调用现场 `catch_warnings` 屏蔽。
5. **存/查配对**：2-save 与 2-search 必须使用同一个嵌入模型（本机已写死同一 MiniLM 快照路径），先 save 后 search。
6. **考点差异**：LlamaIndex Document 内容在 `text` 属性（LangChain 是 `page_content`）；`os.path.dirname(__file__)` 在 Jupyter 不可用。
