# 第10章 Demo 学习指南

## 学习顺序

1. **先学 Demo 1（项目骨架）** → 理解 RAG 项目的完整目录结构和各模块职责
2. **再学 Demo 2（配置管理）** → 掌握如何用 pydantic-settings 管理配置

## Demo 说明

### Demo 1: 项目骨架 (`1_demo_project_skeleton.py`)

**作用**：运行后自动创建一个完整的 RAG 项目目录结构，包含所有模块的占位代码。

**学到什么**：
- RAG 项目的标准目录组织方式
- 每个模块（文档处理、向量存储、检索、生成、API）的职责和接口
- 日志工具和自定义异常的写法
- FastAPI 应用的基本结构

**是否需要 API Key**：不需要

**运行方式**：
```bash
python 1_demo_project_skeleton.py
```

运行后会在当前目录生成 `rag_project/` 目录，可以直接作为后续开发的起点。

---

### Demo 2: 配置管理 (`2_demo_config_management.py`)

**作用**：演示如何用 pydantic-settings 管理项目配置，支持 .env 文件和环境变量。

**学到什么**：
- 为什么不能把 API Key 硬编码在代码里
- .env 文件的写法和加载方式
- pydantic-settings 的配置类定义（类型验证、默认值、范围限制）
- 环境变量的优先级机制
- 配置分组管理的高级用法

**是否需要 API Key**：不需要（演示中使用模拟的 Key）

**运行方式**：
```bash
# 先安装依赖
pip install python-dotenv pydantic-settings

# 运行 Demo
python 2_demo_config_management.py
```

---

## 前置依赖

```bash
pip install python-dotenv pydantic-settings fastapi uvicorn
```

## 学完本章你应该能回答

1. RAG 系统有哪些核心模块？各自职责是什么？
2. 为什么用 .env 文件管理配置？环境变量的优先级是怎样的？
3. 如何设计一个可扩展、可维护的 RAG 项目结构？
4. 日志级别有哪些？什么时候用 ERROR？
5. 自定义异常有什么好处？
