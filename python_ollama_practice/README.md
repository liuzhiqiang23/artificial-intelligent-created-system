# LLM 本地部署实践（实践1~3）

> 对照课件《笔记0903.pdf》第 66-69 页，完成"访问本地 LLM → llama-index 嵌入文件 → 添加向量索引 → 自选嵌入模型"四个实践。

## 环境

- **Windows 11** + **AMD Ryzen 7 5800H** + **NVIDIA RTX 3050 Laptop (4GB)** + 16GB 内存
- **Python 3.13**（独立 venv，见下）
- **Ollama 0.33.3**（本地 LLM 服务，端口 11434）

## 已装模型（`ollama list`）

| 模型 | 用途 | 大小 |
|------|------|------|
| qwen2.5:0.5b | 生成模型（快，中文好） | 397MB |
| nomic-embed-text | 嵌入模型（向量化） | 274MB |
| llama3.2 | 生成模型（3B，实践3改进用） | 2.0GB |

## 目录结构

```
python_ollama_practice/
├── venv/                    # Python 3.13 虚拟环境
├── data/ollama_intro.txt    # 实验用本地知识文件（被检索）
├── p1_ollama_way.py         # 实践1：Ollama 方式调用本地 LLM
├── p1_openai_way.py         # 实践1：OpenAI 兼容 API 调用本地 LLM
├── p2_llama_index_embed.py  # 实践2：llama-index 嵌入文件 + 查询
├── p3_vector_index.py       # 实践3：向量索引 + 多轮问答
├── p3_improved_hf.py        # 实践3(改进)：HuggingFace 自选嵌入模型
└── README.md
```

## 运行前提：启动 Ollama

```bash
# 启动服务（默认监听 11434）
"C:\Users\Lenovo\AppData\Local\Programs\Ollama\ollama.exe" serve
```

## 运行各实践

```bash
# 激活 venv（PowerShell）
.\venv\Scripts\Activate.ps1

# 实践1：Ollama 方式
python p1_ollama_way.py

# 实践1：OpenAI 方式
python p1_openai_way.py

# 实践2：llama-index 嵌入文件
python p2_llama_index_embed.py

# 实践3：向量索引
python p3_vector_index.py

# 实践3(改进)：HuggingFace 自选嵌入(m3e-small)
python p3_improved_hf.py
```

> 注：Windows 终端显示中文可能乱码，建议先 `chcp 65001` 或设置
> `PYTHONIOENCODING=utf-8` 运行。

## 关键排障记录（坑 → 解）

1. **Ollama 用 CUDA 后端探测 GPU 崩溃**（.exe 子进程 exit=1）→ 改用 Vulkan 后端。
2. **Vulkan 后端跑 llama3.2(3B) 生成卡死**（显存 4GB 不足）→ 换小模型 qwen2.5:0.5b，
   25 层全上 GPU 正常生成。
3. **CPU 加载失败`failed to allocate buffer`** → 是残留 llama-server 占 3.5GB 内存所致，
   杀掉后释放内存即可。
4. **token 乱码** → 设 `PYTHONIOENCODING=utf-8`。
