# 第11章 Demo 学习指南

## 学习顺序

1. **先学 Demo 1（多格式加载）** → 理解不同格式的文件如何加载为统一的 Document 对象
2. **再学 Demo 2（批量目录加载）** → 掌握如何一次性加载整个目录的文档

## Demo 说明

### Demo 1: 多格式加载 (`1_demo_multi_format_loader.py`)

**作用**：创建示例的 TXT 和 MD 文件，演示用不同 Loader 加载各种格式的文档。

**学到什么**：
- TextLoader 加载 TXT 文件的用法
- MarkdownLoader 加载 MD 文件的用法
- PDFLoader 的代码示例（需要安装 pdfplumber）
- 统一的 Document 对象格式（page_content + metadata）

**是否需要 API Key**：不需要

**运行方式**：
```bash
# 先安装依赖
pip install langchain langchain-community unstructured

# 运行 Demo
python 1_demo_multi_format_loader.py
```

---

### Demo 2: 批量目录加载 (`2_demo_directory_loader.py`)

**作用**：创建一个多层目录结构（含多种格式文件），演示 DirectoryLoader 批量加载。

**学到什么**：
- DirectoryLoader 的基本用法（path、glob、loader_cls）
- 加载多格式文件的策略
- 加载结果的统计分析
- 不依赖 LangChain 的手动加载方式

**是否需要 API Key**：不需要

**运行方式**：
```bash
python 2_demo_directory_loader.py
```

---

## 前置依赖

```bash
pip install langchain langchain-community unstructured
```

## 学完本章你应该能回答

1. LangChain 有哪些常用的 Document Loader？
2. Document 对象包含哪些字段？metadata 有什么用？
3. DirectoryLoader 的 glob 参数怎么写？`**/*.txt` 是什么意思？
4. 如何处理中文文件的编码问题？
5. 文本预处理包括哪些步骤？为什么不能跳过？
