# 非文本文件加载实践（2026-09-24 任务书：PDF 与图片 OCR）

> 对照《笔记0924.pdf》第 2-3 节：**PDF 加载（LangChain PyPDF / LlamaIndex PyMuPDF / Unstructured 三种路线）+ 图片 OCR（pytesseract / UnstructuredImageLoader / 自定义 Loader/Reader）**。
> Windows + RTX 3050 笔记本全部实测跑通（2026-09-24）。

## 文件结构

```
0924/
├── 1-pdf-langchain.py          # PyPDFLoader 单文件 + DirectoryLoader 批量
├── 2-pdf-llamaindex.py         # PyMuPDFReader 单文件 + SimpleDirectoryReader(file_extractor)
├── 3-pdf-unstructured.py       # UnstructuredPDFLoader / UnstructuredLoader(lazy_load) / partition 元素统计
├── 4-img-ocr.py                # pytesseract 直用 + UnstructuredImageLoader + 自定义 TesseractLoader
├── 5-img-llamaindex-ocr.py     # 自定义 TesseractReader(BaseReader) + BGE 检索
├── file/05.pdf                 # 演示 PDF（正式素材等老师提供后替换）
└── imgs/                       # 演示图片：sales.jpg(中文) / eng.jpg(英文) / img1.png(中文)
```

## 环境依赖（本机已全部部署）

| 组件 | 位置/版本 | 说明 |
|---|---|---|
| poppler | `D:\poppler\poppler-25.12.0\Library\bin`（已加入用户 PATH） | pdftoppm/pdfinfo，Unstructured 处理 PDF 底层调用 |
| tesseract | `C:\Program Files\Tesseract-OCR`（v5.4.0，已加入用户 PATH） | OCR 引擎 |
| 语言包 | `D:\tesseract-data`（chi_sim + eng） | 经 `TESSDATA_PREFIX` 环境变量指向（免管理员方案） |
| pypdf | 已装 | LangChain PyPDFLoader 依赖 |
| pymupdf | 1.28.2 | LlamaIndex PyMuPDFReader 依赖 |
| unstructured | **0.18.32**（PDF/OCR 扩展已装） | Py3.10 不能装 0.20.x，只能 0.18.x（任务书原话） |
| langchain_unstructured / pytesseract / pdf2image / llama-index-readers-file | 已装 | 各加载器依赖 |

## 运行

```bash
python 1-pdf-langchain.py       # 4 个文档（按页）
python 2-pdf-llamaindex.py      # 4 个文档
python 3-pdf-unstructured.py    # 单文档 + 懒加载 + 70 个 elements 类型统计
python 4-img-ocr.py             # 中文 OCR 完整识别 + 英文 + 自定义类
python 5-img-llamaindex-ocr.py  # OCR 3 图 → 检索"华东区销售额"
```

## Windows 适配要点

1. **TESSDATA_PREFIX**：语言包放在 D 盘 `D:\tesseract-data`（避免写系统目录要管理员权限），脚本里 `os.environ.setdefault('TESSDATA_PREFIX', ...)` 双保险。
2. **tesseract 路径两处都要**：`pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`（给 pytesseract 用）+ `os.environ['PATH'] += r';C:\Program Files\Tesseract-OCR'`（**UnstructuredImageLoader 内部走 PATH 找 tesseract 命令**，对应任务书 Mac 版 `os.environ['PATH'] += ':/opt/homebrew/bin'` 那句，不加会报 TesseractNotFoundError）。
3. **strategy="fast"**：不下载解析模型；`hi_res` 需要从 Huggingface 下载（一般下不动），任务书原话。
4. **UnstructuredPDFLoader 的 mode**：single（1 文档）/ elements（按元素）/ paged（按页）。
5. **unstructured 版本红线**：Python 3.10 只能装 0.18.x；本项目钉在 0.18.32。
6. **`unstructured[ocr]` 扩展在 0.18.32 不存在**（pip 会提示 does not provide the extra），OCR 相关依赖（pytesseract/pdf2image）单独装齐即可。

## 备注

- `file/05.pdf` 与 `imgs/*` 暂用自制演示素材（真实素材以老师 zip 为准，到位后替换并重跑）。
- 环境变量（PATH/TESSDATA_PREFIX）改后需**重启 PyCharm** 才能被 IDE 内运行的进程继承。
