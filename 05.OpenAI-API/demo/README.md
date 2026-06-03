# 第5章 Demo 学习指南

## 学习顺序

建议按照以下顺序学习：

1. **先学习理论**：阅读 `1.Chat Completion API.md` 和 `2.Embedding API.md`
2. **再动手实践**：按照顺序运行 Demo

## Demo 列表

### Demo 1: 基础对话 (`1_demo_basic_chat.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `1.Chat Completion API.md` |
| **功能** | 5行代码让GPT回答问题，多轮对话维护history |
| **是否需要API Key** | 是 |
| **核心知识点** | client.chat.completions.create()、角色设置、Temperature参数、多轮对话 |

**学习要点**：
- 理解 `messages` 列表的结构
- 理解 `system`/`user`/`assistant` 三种角色的作用
- 掌握多轮对话中 `history` 的维护方法
- 体验不同 `temperature` 值对输出的影响

### Demo 2: Embedding (`2_demo_embedding.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `2.Embedding API.md` |
| **功能** | 把文本变成向量，计算余弦相似度找最相似的句子 |
| **是否需要API Key** | 是 |
| **核心知识点** | client.embeddings.create()、向量概念、余弦相似度、批量Embedding |

**学习要点**：
- 理解文本如何被转换为向量（1536维数字）
- 掌握用 numpy 计算余弦相似度
- 理解语义检索的基本原理
- 学会批量 Embedding 以节省 API 调用

## 运行前准备

```bash
# 安装依赖
pip install openai numpy

# 配置 API Key
# 打开每个 .py 文件，修改顶部的 API_KEY、BASE_URL、MODEL 变量
```

## 常见问题

**Q: 报错 `openai.AuthenticationError`**
A: 检查 API_KEY 是否正确填写，是否有足够的额度。

**Q: 报错 `openai.APIConnectionError`**
A: 检查网络连接，或检查 BASE_URL 是否正确（如使用代理）。

**Q: Embedding 向量维度不是 1536**
A: 不同模型维度不同，text-embedding-ada-002 是 1536 维，text-embedding-3-small 也是 1536 维，text-embedding-3-large 是 3072 维。
