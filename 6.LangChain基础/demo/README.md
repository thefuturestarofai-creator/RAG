# 第6章 Demo 学习指南

## 学习顺序

建议按照以下顺序学习：

1. **先学习理论**：依次阅读 `1.Chain与LCEL.md`、`2.文档处理.md`、`3.向量存储与检索.md`
2. **再动手实践**：按照 Demo 编号顺序运行

## Demo 列表

### Demo 1: 最简 Chain (`1_demo_simple_chain.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `1.Chain与LCEL.md` |
| **功能** | PromptTemplate 和 LLM 的 LCEL 管道 |
| **是否需要API Key** | 是 |
| **核心知识点** | LCEL 管道语法、PromptTemplate、ChatPromptTemplate、流式输出 |

**学习要点**：
- 理解 `|` 管道符的使用方式
- 掌握 PromptTemplate 和 ChatPromptTemplate 的区别
- 体验流式输出（stream）的效果

### Demo 2: 文档加载与切分 (`2_demo_document_split.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `2.文档处理.md` |
| **功能** | 读取文本文件，用 RecursiveCharacterTextSplitter 切分 |
| **是否需要API Key** | 否 |
| **核心知识点** | TextLoader、RecursiveCharacterTextSplitter、chunk_size、chunk_overlap |

**学习要点**：
- 理解文档加载和切分的流程
- 观察不同 chunk_size 对切分结果的影响
- 理解 chunk_overlap 的作用

### Demo 3: 完整 RAG 管道 (`3_demo_rag_pipeline.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `3.向量存储与检索.md` |
| **功能** | 文档加载→切分→Embedding→Chroma存储→检索→LLM回答 |
| **是否需要API Key** | 是 |
| **核心知识点** | Chroma 向量数据库、Retriever、RAG Chain 构建 |

**学习要点**：
- 掌握完整的 RAG 流程
- 理解 VectorStore 和 Retriever 的关系
- 学会用 LCEL 构建 RAG 管道
- 观察检索结果对答案质量的影响

## 运行前准备

```bash
# 安装依赖（建议使用 Python 3.9+）
pip install langchain langchain-openai langchain-community langchain-chroma langchain-text-splitters chromadb

# 配置 API Key
# 打开需要 API Key 的 .py 文件，修改顶部的 API_KEY、BASE_URL、MODEL 变量
```

## LangChain 版本说明

本教程使用的是 LangChain 新版包结构：
- `langchain`：核心包
- `langchain-openai`：OpenAI 集成
- `langchain-core`：核心抽象（Prompt、Chain 等）
- `langchain-community`：社区组件（Loader 等）
- `langchain-chroma`：Chroma 集成

旧版的 `from langchain.xxx import ...` 已被弃用，请使用新版导入方式。

## 常见问题

**Q: 报错 `ModuleNotFoundError: No module named 'langchain_chroma'`**
A: 运行 `pip install langchain-chroma` 安装 Chroma 集成包。

**Q: 报错 `Chroma requires embedding function`**
A: 确保传入了正确的 Embedding 模型，并且 API Key 可用。

**Q: 检索结果不准确**
A: 尝试调整 chunk_size（建议 200-500）和 chunk_overlap（建议 20-50），也可以增加检索的 k 值。
