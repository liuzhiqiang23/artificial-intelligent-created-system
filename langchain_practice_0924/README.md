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
├── 01~07-*.py                  # ★ 老师 0924.zip 官方 7 脚本（Windows 适配版，老师文件名不变）
├── file/05.pdf                 # 演示 PDF（笔记0917.pdf 顶替）
├── files/                      # ★ 老师官方脚本的素材目录：01.pdf(自制双页) / 05.pdf / 01.png / 02.jpg
└── imgs/                       # 演示图片：sales.jpg(中文) / eng.jpg(英文) / img1.png(中文)
```

## 老师官方 7 脚本（0924.zip，2026-09-25 收到）

| 脚本 | 内容 | 实测结果 |
|---|---|---|
| 01-langchain-pdf-1 | DirectoryLoader(**/*.pdf) 批量 | 10 个文档（3 份 PDF 按页合计） |
| 02-llama-pdf-1 | SimpleDirectoryReader + PyMuPDFReader | 6 个文档 |
| 03-langchain-pdf-2 | UnstructuredPDFLoader **mode="elements"** | 70 个元素（Title/ListItem 分类元数据） |
| 04-llama-pdf-2 | UnstructuredReader split_documents=True | 70 个文档（老师真素材为 224，素材未发，暂用顶替） |
| 05-tesseract-image | pytesseract 直用（chi_sim+eng） | 中文完整识别"2026年9月 华东区销售额: 128万元" |
| 06-langchain-image | UnstructuredImageLoader(ocr_only) | 仅得 "67%"——**复现任务书图 3-2：封装版 OCR 质量反而差** |
| 07-tesseract-loader | TesseractLoader 类 + 故意传坏文件 | 2 成功 + 2 个错误被逐文件捕获（容错演示） |

适配仅 3 处：05/07 的 `tesseract_cmd` Mac→Windows、06 补 `PATH += Tesseract-OCR` 一行，其余代码原样保留（原 Mac 写法以注释保留）。

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
# 自编 5 脚本（对照任务书章节）
python 1-pdf-langchain.py       # 4 个文档（按页）
python 2-pdf-llamaindex.py      # 4 个文档
python 3-pdf-unstructured.py    # 单文档 + 懒加载 + 70 个 elements 类型统计
python 4-img-ocr.py             # 中文 OCR 完整识别 + 英文 + 自定义类
python 5-img-llamaindex-ocr.py  # OCR 3 图 → 检索"华东区销售额"

# 老师官方 7 脚本（0924.zip，工作目录须在项目根）
python 01-langchain-pdf-1.py    # 10 个文档
python 02-llama-pdf-1.py        # 6 个文档
python 03-langchain-pdf-2.py    # 70 个元素
python 04-llama-pdf-2.py        # 70 个文档
python 05-tesseract-image.py    # 中文完整识别
python 06-langchain-image.py    # "67%"（对比 05 看封装损耗）
python 07-tesseract-loader.py   # 2 成功 + 2 容错
```

## Windows 适配要点

1. **TESSDATA_PREFIX**：语言包放在 D 盘 `D:\tesseract-data`（避免写系统目录要管理员权限），脚本里 `os.environ.setdefault('TESSDATA_PREFIX', ...)` 双保险。
2. **tesseract 路径两处都要**：`pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`（给 pytesseract 用）+ `os.environ['PATH'] += r';C:\Program Files\Tesseract-OCR'`（**UnstructuredImageLoader 内部走 PATH 找 tesseract 命令**，对应任务书 Mac 版 `os.environ['PATH'] += ':/opt/homebrew/bin'` 那句，不加会报 TesseractNotFoundError）。
3. **strategy="fast"**：不下载解析模型；`hi_res` 需要从 Huggingface 下载（一般下不动），任务书原话。
4. **UnstructuredPDFLoader 的 mode**：single（1 文档）/ elements（按元素）/ paged（按页）。
5. **unstructured 版本红线**：Python 3.10 只能装 0.18.x；本项目钉在 0.18.32。
6. **`unstructured[ocr]` 扩展在 0.18.32 不存在**（pip 会提示 does not provide the extra），OCR 相关依赖（pytesseract/pdf2image）单独装齐即可。

## 备注

- 老师 0924.zip（09-25 收到）**只含 7 个脚本、不带素材**：`files/` 按老师代码里的路径约定搭好——01.pdf 为 PyMuPDF 自制双页中文 PDF，05.pdf 仍用笔记0917.pdf 顶替，01.png/02.jpg 复用 imgs 素材副本。老师真素材到手后替换 `files/` 重跑即可。
- 04 号脚本老师注释"输出 224 个文档"基于其真素材；顶替素材实测 70 个，正常。
- 环境变量（PATH/TESSDATA_PREFIX）改后需**重启 PyCharm** 才能被 IDE 内运行的进程继承。
