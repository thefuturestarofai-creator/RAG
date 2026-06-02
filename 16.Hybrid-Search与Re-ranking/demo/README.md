# 第16章：Hybrid Search与Re-ranking - Demo

## 学习顺序

建议按照以下顺序学习本章的 Demo：

### 1. BM25 检索 (1_demo_bm25.py)

**学习目标**：理解稀疏检索的基础

**内容**：
- BM25 算法原理和参数详解
- 中文分词和 BM25 索引构建
- FAQ 检索系统实战
- BM25 与向量检索的概念对比

**是否需要 API Key**：否

**运行方式**：
```bash
pip install rank_bm25 jieba
python 1_demo_bm25.py
```

---

### 2. 混合检索 (2_demo_hybrid_search.py)

**学习目标**：掌握 RRF 融合算法

**内容**：
- RRF（Reciprocal Rank Fusion）算法详解
- BM25 检索器实现
- 向量检索器实现（使用 OpenAI Embedding）
- 混合检索器实现和效果演示

**是否需要 API Key**：是（用于 Embedding）

**API Key 配置**：
```python
API_KEY = "your-api-key-here"
BASE_URL = "https://api.openai.com/v1"
MODEL = "text-embedding-ada-002"
```

**运行方式**：
```bash
pip install rank_bm25 jieba openai
python 2_demo_hybrid_search.py
```

**注意**：如果没有 API Key，代码会使用随机向量模拟，仍然可以学习 RRF 算法原理。

---

### 3. Re-ranking 重排序 (3_demo_reranking.py)

**学习目标**：掌握两阶段检索流程

**内容**：
- CrossEncoder 原理讲解
- 使用 sentence-transformers 加载 Rerank 模型
- 完整的两阶段检索流程（召回 + 重排）
- Reranking 效果分析和最佳实践

**是否需要 API Key**：否（使用本地模型）

**运行方式**：
```bash
pip install sentence-transformers rank_bm25 jieba
python 3_demo_reranking.py
```

**注意**：首次运行会下载模型（约 1.1GB），请确保网络通畅。

---

---

### 4. 知识图谱增强 (4_demo_graph_rag.py)

**学习目标**：理解 Graph RAG 的核心概念

**内容**：
- 知识图谱构建（实体 + 关系三元组）
- NetworkX 有向图的使用
- 多跳查询：沿着关系链走多步找到答案
- 路径查找：任意两实体之间的关系链
- Graph RAG 管道：图检索 + 向量检索融合
- 传统 RAG vs Graph RAG 对比

**是否需要 API Key**：否

**运行方式**：
```bash
pip install networkx
python 4_demo_graph_rag.py
```

---

## 依赖安装

一键安装所有依赖：
```bash
pip install rank_bm25 jieba openai sentence-transformers networkx
```

## 知识点对应关系

| Demo | 对应知识点 | 核心内容 |
|------|-----------|---------|
| 1_demo_bm25.py | 混合检索Hybrid Search | BM25 稀疏检索原理 |
| 2_demo_hybrid_search.py | 混合检索Hybrid Search | RRF 分数融合算法 |
| 3_demo_reranking.py | 重排序Re-ranking | CrossEncoder 两阶段检索 |
| 4_demo_graph_rag.py | 知识图谱增强Graph RAG | 多跳推理、图检索融合 |

## 学习建议

1. **先看理论文档**：在运行 Demo 前，先阅读对应的理论文档
2. **动手运行代码**：实际运行代码，观察输出结果
3. **修改参数实验**：尝试修改参数，观察效果变化
4. **记录笔记**：记录关键概念和面试话术

## 常见问题

### Q1: 模型下载失败怎么办？

A: 可以使用镜像源：
```bash
export HF_ENDPOINT=https://hf-mirror.com
python 3_demo_reranking.py
```

### Q2: 没有 GPU 能运行吗？

A: 可以。sentence-transformers 支持 CPU 运行，只是速度较慢。

### Q3: API Key 在哪里获取？

A: OpenAI API Key 可以在 https://platform.openai.com 获取。也可以使用其他兼容 OpenAI 格式的 API 服务。

### Q4: networkx 怎么安装？

A: 运行 `pip install networkx` 即可，这是一个纯 Python 库，不需要额外依赖。

## 面试重点

1. **BM25 原理**：TF-IDF 的改进，文档长度归一化，词频饱和
2. **RRF 算法**：公式、k 值的作用、为什么用排名而不是分数
3. **CrossEncoder vs Bi-Encoder**：交互方式、速度精度权衡
4. **两阶段检索**：为什么需要、怎么设计、参数怎么调
5. **Graph RAG**：知识图谱、多跳推理、图检索与向量检索融合
