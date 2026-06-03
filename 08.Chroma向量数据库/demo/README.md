# 第8章 Demo 学习指南

## 学习顺序

建议按照以下顺序学习：

1. **先学习理论**：阅读 `1.Chroma核心操作.md` 和 `2.向量检索原理.md`
2. **再动手实践**：按照 Demo 编号顺序运行

## Demo 列表

### Demo 1: Chroma 基础 (`1_demo_chroma_basic.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `1.Chroma核心操作.md` |
| **功能** | 创建Collection、添加文档、查询、元数据过滤 |
| **是否需要API Key** | 否（使用 Chroma 内置 Embedding） |
| **核心知识点** | Collection、add/query/delete、元数据过滤、持久化存储 |

**学习要点**：
- 理解 Chroma 的基本操作流程
- 掌握元数据过滤的使用方法
- 理解持久化存储的概念
- 观察相似度检索的结果

### Demo 2: Chroma + LangChain 集成 (`2_demo_chroma_langchain.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `1.Chroma核心操作.md` + `2.向量检索原理.md` |
| **功能** | 用 LangChain 的 Chroma 封装实现向量存储和检索 |
| **是否需要API Key** | 是 |
| **核心知识点** | LangChain Chroma 封装、Document 对象、带分数检索、元数据过滤 |

**学习要点**：
- 理解 LangChain 与 Chroma 的集成方式
- 掌握 Document 对象的结构
- 学会使用带相似度分数的检索
- 理解向量检索的实际效果

## 运行前准备

```bash
# 安装依赖
pip install chromadb

# 如果要运行 Demo 2，还需要安装 LangChain 相关依赖
pip install langchain langchain-openai langchain-community langchain-chroma
```

## 常见问题

**Q: 报错 `No module named 'chromadb'`**
A: 运行 `pip install chromadb` 安装。

**Q: Chroma 的内置 Embedding 支持中文吗？**
A: Chroma 默认使用 all-MiniLM-L6-v2 模型，主要针对英文优化。中文场景建议使用 OpenAI 的 text-embedding-ada-002 或其他支持中文的模型。

**Q: 持久化目录在哪里？**
A: Demo 1 使用 `./chroma_demo_db`，Demo 2 使用 `./chroma_langchain_db`。程序结束后会自动清理，也可以手动删除。

**Q: 检索结果不准确怎么办？**
A: 尝试：1）增加检索数量（n_results/k）；2）使用更好的 Embedding 模型；3）调整文档切分策略；4）添加元数据过滤缩小范围。
