# 智能生成系统

> 基于本地大模型（Ollama + llama-index）的 LLM 部署与应用实践项目。
> 在普通 Windows 笔记本上，**不依赖联网**跑通「本地 LLM 访问 → 文档嵌入 → 向量检索问答 → 网页问答界面」完整链路。

---

## 仓库简介

本仓库包含一套**本地大模型部署与应用的完整实践**，来自课程《笔记0903.pdf》第 66-69 页要求，并在其基础上扩展了一个**可用的网页问答界面**。核心思路：**让一台只有 4GB 显存、可以断网的普通电脑，也能跑起来、用起来大模型**。

### 关键技术
- **Ollama**（本地 LLM 运行工具，端口 11434）
- **llama-index**（文档加载、嵌入、向量索引、检索问答）
- **HuggingFace**（自选中文嵌入模型）
- **Flask + HTML**（网页问答界面）

---

## 目录结构

```
智能生成系统/
├── 智能生成系统开发.pdf      # 课程资料
├── 笔记0903.pdf              # 课件（实践要求出处）
├── README.md                 # 本文件
├── python_ollama_practice/   # 实践项目主目录（实践1-3，Ollama+llama-index）
└── langchain_practice_0910/  # 实践4-6：LangChain/LangGraph/faiss/zvec（0910任务书）
    ├── data/                 # 本地知识文件（被检索的语料）
    ├── venv/                 # Python 虚拟环境（已 gitignore，不入库）
    ├── p1_ollama_way.py      # 实践1：Ollama 方式访问本地 LLM
    ├── p1_openai_way.py      # 实践1：OpenAI 兼容方式访问本地 LLM
    ├── p2_llama_index_embed.py  # 实践2：llama-index 嵌入文件 + 检索
    ├── p3_vector_index.py    # 实践3：向量索引 + 多轮问答
    ├── p3_improved_hf.py     # 实践3改进：HF 自选嵌入 + 本地生成
    ├── chat_server.py        # 网页问答后端（Flask）
    ├── chat_front.html       # 网页问答前端
    ├── start_llm_chat.bat    # 一键启动脚本
    ├── report.html           # 可视化成果汇报页
    ├── 本地LLM部署与实践教程_Ollama与llama-index.docx  # 新手教程
    └── README.md             # 实践细节说明
```

---

## 四个实践（对照课件）

| 实践 | 目标 | 关键代码 |
|------|------|---------|
| 实践1 | 访问本地 LLM | `p1_ollama_way.py`、`p1_openai_way.py` |
| 实践2 | 用 llama-index 加载文件、嵌入、检索问答 | `p2_llama_index_embed.py` |
| 实践3 | 添加向量索引，多轮问答 | `p3_vector_index.py` |
| 实践3改进 | 自选嵌入模型（HuggingFace）+ 本地生成 | `p3_improved_hf.py` |

每个实践脚本旁都有 `pX_result.txt`，保存了**真实运行输出**，可直接对照效果。

---

## 快速开始

### 1. 环境要求
- Windows 10/11，CPU 任意，**GPU 有 4GB 显存最佳**（无 GPU 也能 CPU 跑，只是慢）
- Python 3.13
- Ollama 服务（端口 11434）

### 2. 安装依赖
```bash
cd python_ollama_practice
python -m venv venv
venv\Scripts\activate            # PowerShell 用 venv\Scripts\Activate.ps1
pip install ollama openai llama-index-core llama-index-llms-ollama \
            llama-index-embeddings-ollama flask
```

### 3. 安装并启动 Ollama、拉取模型
```bash
# 安装（或直接用 Ollama 官网安装包）
winget install --id Ollama.Ollama -e

# 启动服务
"C:\Users\Lenovo\AppData\Local\Programs\Ollama\ollama.exe" serve

# 拉取模型
ollama pull qwen2.5:0.5b        # 生成模型（问答）
ollama pull nomic-embed-text    # 嵌入模型（向量化）
```

### 4. 跑某个实践
```bash
python p1_ollama_way.py         # 实践1：Ollama 方式
python p2_llama_index_embed.py  # 实践2：llama-index 嵌入
```

### 5. 启动网页问答界面
**双击 `start_llm_chat.bat`**，自动打开浏览器到 `http://127.0.0.1:5000`，即可一问一答。

---

## 网页问答界面

两模式（右上角切换）：
- **直接对话**：模型凭自身知识答题（对应实践1）
- **查本地资料**：先检索本地 `data/` 知识文件再答，答案有出处（对应实践2/3）

**断网可用**：整个链路（模型 + 嵌入 + 服务）跑在本地回环地址，不经过外网。

---

## 常见问题（排障要点）

详见 `python_ollama_practice/README.md` 与配套教程文档，几个高频坑：

1. **Ollama 认不出显卡** → 设置 `OLLAMA_LLM_LIBRARY=vulkan` 重启 serve（RTX 3050 支持 Vulkan）。
2. **3B 模型生成卡死** → 4GB 显存只能跑 0.5b~1b 小模型，用 `qwen2.5:0.5b`。
3. **llama-index 报内存不足（14GB）** → 限制 `Ollama(model=..., context_window=4096)`。
4. **中文乱码** → `set PYTHONIOENCODING=utf-8`。

---

## 环境实测

| 组件 | 配置 |
|------|------|
| 开发机 | AMD Ryzen 7 5800H + RTX 3050 (4GB) + 16GB 内存 + Windows 11 |
| Python | 3.13（venv） |
| Ollama | 0.33.3 |
| 模型 | qwen2.5:0.5b / nomic-embed-text / llama3.2 / m3e-small |

---

## 版权与说明

- 课程资料（PDF）版权归原作者，仅供学习使用。
- 实践代码为本项目独立完成，可自由参考。
- 详细实践过程与排障记录见配套文档。
