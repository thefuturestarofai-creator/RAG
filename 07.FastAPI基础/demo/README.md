# 第7章 Demo 学习指南

## 学习顺序

建议按照以下顺序学习：

1. **先学习理论**：依次阅读 `1.路由与请求处理.md`、`2.Pydantic数据校验.md`、`3.依赖注入与异步.md`
2. **再动手实践**：按照 Demo 编号顺序运行

## Demo 列表

### Demo 1: Hello FastAPI (`1_demo_hello_fastapi.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `1.路由与请求处理.md` |
| **功能** | 10行代码启动API，访问 /docs 看自动生成的文档 |
| **是否需要API Key** | 否 |
| **核心知识点** | FastAPI 创建、路由定义、路径参数、查询参数 |

**学习要点**：
- 理解 FastAPI 应用的创建方式
- 掌握路径参数和查询参数的定义
- 体验自动生成的 Swagger UI 文档

### Demo 2: POST接口 (`2_demo_post_api.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `2.Pydantic数据校验.md` |
| **功能** | 接收JSON请求体，用Pydantic校验，返回结构化响应 |
| **是否需要API Key** | 否 |
| **核心知识点** | Pydantic BaseModel、字段验证、请求/响应模型、异常处理 |

**学习要点**：
- 理解 Pydantic 模型的定义方式
- 掌握字段验证（Field）的使用
- 理解请求模型和响应模型的作用
- 学习 HTTPException 异常处理

### Demo 3: RAG问答API (`3_demo_rag_api.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `3.依赖注入与异步.md` |
| **功能** | 把第6章的RAG管道封装成API接口 |
| **是否需要API Key** | 是 |
| **核心知识点** | 依赖注入（Depends）、生命周期管理、RAG API 封装 |

**学习要点**：
- 掌握 FastAPI 的依赖注入机制
- 理解应用生命周期管理（lifespan）
- 学会将 RAG 管道封装成 REST API
- 掌握完整的异常处理策略

## 运行前准备

```bash
# 安装依赖
pip install fastapi uvicorn pydantic

# 如果要运行 Demo 3，还需要安装 RAG 相关依赖
pip install langchain langchain-openai langchain-community langchain-chroma chromadb
```

## 运行方式

每个 Demo 都可以通过以下两种方式运行：

**方式1：直接运行 Python 文件**
```bash
python 1_demo_hello_fastapi.py
```

**方式2：使用 uvicorn 命令**
```bash
uvicorn 1_demo_hello_fastapi:app --reload --port 8000
```

启动后，访问 http://127.0.0.1:8000/docs 查看 API 文档。

## 常见问题

**Q: 报错 `uvicorn: command not found`**
A: 运行 `pip install uvicorn` 安装，或使用 `python -m uvicorn` 代替。

**Q: 端口被占用**
A: 使用 `--port` 参数指定其他端口，如 `--port 8001`。

**Q: Pydantic 验证报错 422**
A: 检查请求体格式是否符合 Pydantic 模型定义，可以在 /docs 页面查看请求体的 Schema。
