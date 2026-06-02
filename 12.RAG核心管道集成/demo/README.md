# 第12章 Demo 学习指南

## 学习顺序

1. **先学 Demo 1（完整 RAG 管道）** → 理解 RAG 的完整流程：加载→切分→存储→检索→生成
2. **再学 Demo 2（带来源追溯）** → 学会在回答中标注信息来源
3. **再学 Demo 3（流式输出）** → 实现打字机效果的流式回答
4. **再学 Demo 4（文本切分策略）** → 对比 4 种 Chunking 策略的效果
5. **最后学 Demo 5（多轮对话记忆）** → 理解三种对话记忆模式及 RAG 管道集成

## Demo 说明

### Demo 1: 完整 RAG 管道 (`1_demo_rag_pipeline.py`)

**作用**：一个 Python 文件实现完整的 RAG 流程，从文档加载到生成回答。

**学到什么**：
- RAG 的 6 个核心步骤：加载→切分→Embedding→存储→检索→生成
- DirectoryLoader 批量加载文档
- RecursiveCharacterTextSplitter 切分文档
- Chroma 向量数据库的使用
- Prompt 模板的构造

**是否需要 API Key**：需要（用于 Embedding 和 LLM）

**运行方式**：
```bash
# 设置 API Key
export OPENAI_API_KEY="sk-your-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"

# 运行
python 1_demo_rag_pipeline.py
```

---

### Demo 2: 带来源追溯的 RAG (`2_demo_rag_with_sources.py`)

**作用**：在 Demo 1 基础上增加来源追溯，回答中标注信息来自哪个文件。

**学到什么**：
- Document 的 metadata 设计
- similarity_search_with_score 的用法
- 在 Prompt 中要求 LLM 标注来源
- 结构化返回结果（answer + sources）

**是否需要 API Key**：需要

**运行方式**：
```bash
python 2_demo_rag_with_sources.py
```

---

### Demo 3: 流式输出 (`3_demo_streaming_output.py`)

**作用**：用 FastAPI + SSE 实现流式回答，打开浏览器可以看到打字机效果。

**学到什么**：
- SSE（Server-Sent Events）的原理和实现
- FastAPI 的 StreamingResponse
- LLM 的流式调用（streaming=True）
- 前端 EventSource 接收流式数据

**是否需要 API Key**：需要

**运行方式**：
```bash
# 启动服务
python 3_demo_streaming_output.py

# 打开浏览器访问
# http://localhost:8000
```

---

### Demo 4: 文本切分策略对比 (`4_demo_chunking_strategies.py`)

**作用**：对比 4 种主流的文本切分策略（固定长度、递归字符、语义切分、按文档结构切分），并演示 Chunk Size 和 Overlap 的调优效果。

**学到什么**：
- 4 种 Chunking 策略的原理和实现
- Chunk Size 和 Chunk Overlap 的调优方法
- 不同策略的适用场景对比
- Metadata 增强技巧

**是否需要 API Key**：不需要（使用本地实现，不调用外部 API）

**运行方式**：
```bash
python 4_demo_chunking_strategies.py
```

---

### Demo 5: 多轮对话记忆 (`5_demo_conversation_memory.py`)

**作用**：演示 RAG 系统中三种对话记忆模式的实现和对比。

**学到什么**：
- ConversationBufferMemory（全量保存）：适合短对话
- ConversationSummaryMemory（摘要压缩）：适合长对话
- ConversationBufferWindowMemory（滑动窗口）：适合主题切换频繁
- 对话历史如何注入到 RAG 的 Prompt 中
- 三种模式的 Token 增长对比

**是否需要 API Key**：否（模拟 LLM 调用）

**运行方式**：
```bash
python 5_demo_conversation_memory.py
```

---

## 前置依赖

```bash
pip install langchain langchain-openai langchain-community chromadb fastapi uvicorn
```

---

## 学完本章你应该能回答

1. 完整的 RAG 管道包括哪些步骤？
2. 如何在回答中标注信息来源？
3. 什么是 SSE？如何用 FastAPI 实现流式输出？
4. LLM 的流式调用和普通调用有什么区别？
5. 如何设计 Document 的 metadata 来支持来源追溯？
6. RAG 系统有哪三种对话记忆模式？各自适合什么场景？
7. 如何将对话历史注入到 RAG 的 Prompt 中？
8. RAG 系统中有哪 4 种主流的文本切分策略？各自的优缺点是什么？
9. 如何调优 Chunk Size 和 Chunk Overlap？
10. 什么是递归字符切分？为什么它是大多数场景的首选？
