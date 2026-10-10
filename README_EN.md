# AI Content Generation System

**[中文](./README.md) | English**

A local LLM deployment and application project built with Ollama and llama-index. It demonstrates the full path from local model access to document embeddings, vector retrieval, and a browser-based Q&A interface — including on a regular Windows laptop that can run offline.

## Project overview

The repository contains a set of course exercises based on pages 66–69 of the course notes, extended with a usable web Q&A interface. The goal is to make a local model practical on a machine with about 4 GB of GPU memory.

### Main technologies

- **Ollama** for local model serving (port 11434)
- **llama-index** for document loading, embeddings, vector indexing, and retrieval-augmented Q&A
- **Hugging Face** for user-selected Chinese embedding models
- **Flask + HTML** for the web interface

## Repository layout

~~~text
AI content generation system/
├── Course PDFs and notes
├── python_ollama_practice/       # Exercises 1–3: Ollama and llama-index
└── langchain_practice_0910/      # Exercises 4–6: LangChain, LangGraph, FAISS, and zvec
    ├── data/                     # Local documents used for retrieval
    ├── p1_ollama_way.py           # Access a local LLM through Ollama
    ├── p1_openai_way.py           # OpenAI-compatible local endpoint
    ├── p2_llama_index_embed.py    # Embed and retrieve local documents
    ├── p3_vector_index.py         # Vector index and multi-turn Q&A
    ├── p3_improved_hf.py          # Hugging Face embeddings and local generation
    ├── chat_server.py             # Flask backend
    ├── chat_front.html            # Web frontend
    └── start_llm_chat.bat         # One-click launcher
~~~

## Exercises

| Exercise | Goal | Main code |
|---|---|---|
| 1 | Access a local LLM | p1_ollama_way.py, p1_openai_way.py |
| 2 | Load, embed, and retrieve documents with llama-index | p2_llama_index_embed.py |
| 3 | Add vector indexing and multi-turn Q&A | p3_vector_index.py |
| Improved 3 | Choose a Hugging Face embedding model and generate locally | p3_improved_hf.py |

Each exercise includes a pX_result.txt file with actual run output for comparison.

## Quick start

### Requirements

- Windows 10 or 11; any CPU. A GPU with 4 GB of memory is helpful, but CPU-only operation is possible and slower.
- Python 3.13
- Ollama running on port 11434

### Install dependencies

~~~bash
cd python_ollama_practice
python -m venv venv
~~~

Activate the virtual environment, then install:

~~~bash
pip install ollama openai llama-index-core llama-index-llms-ollama \
  llama-index-embeddings-ollama flask
~~~

### Start Ollama and download models

~~~bash
winget install --id Ollama.Ollama -e
ollama serve
ollama pull qwen2.5:0.5b
ollama pull nomic-embed-text
~~~

### Run an exercise or start the web interface

~~~bash
python p1_ollama_way.py
python p2_llama_index_embed.py
~~~

Alternatively, double-click start_llm_chat.bat. It starts the service and opens http://127.0.0.1:5000.

## Web Q&A

Choose between two modes from the upper-right corner:

- **Direct chat:** answer from the model's own knowledge (Exercise 1).
- **Search local documents:** retrieve from data/ before answering and show the supporting source (Exercises 2–3).

The model, embeddings, and service run on the local loopback interface; the retrieval workflow does not require Internet access.

## Troubleshooting

For more detail, see python_ollama_practice/README.md and the included tutorial.

1. **Ollama does not detect the GPU:** set OLLAMA_LLM_LIBRARY=vulkan and restart the server; RTX 3050 supports Vulkan.
2. **A 3B model stalls:** 4 GB of VRAM is better suited to small models such as qwen2.5:0.5b.
3. **llama-index runs out of memory:** limit the context window, for example Ollama(model=..., context_window=4096).
4. **Chinese output is garbled:** set PYTHONIOENCODING=utf-8.

## Tested environment

| Component | Configuration |
|---|---|
| Development PC | AMD Ryzen 7 5800H, RTX 3050 (4 GB), 16 GB RAM, Windows 11 |
| Python | 3.13 in a virtual environment |
| Ollama | 0.33.3 |
| Models | qwen2.5:0.5b, nomic-embed-text, llama3.2, m3e-small |

## Copyright and use

- Course PDFs belong to their original authors and are included for study only.
- The practice code was written for this project and may be used as a reference.
- The companion documents contain the detailed exercise walkthroughs and troubleshooting notes.

---

[GitHub profile](https://github.com/liuzhiqiang23) · [Zhihu](https://www.zhihu.com/people/yi-bu-gen-jiang) · [Gitee profile](https://gitee.com/liu-zhiqiang20030520)
