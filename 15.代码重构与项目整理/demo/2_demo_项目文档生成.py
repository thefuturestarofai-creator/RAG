# ============================================================
# Demo 2: 项目文档生成
# 对应理论文档: 2.项目文档.md
# ============================================================
# 这个 Demo 展示如何为 RAG 项目生成规范的文档：
# 1. README.md
# 2. CHANGELOG.md
# 3. 项目架构图（ASCII + Mermaid）
# 不需要 API Key。
# ============================================================

import os
from datetime import datetime


# ================================================================
#                    1. 生成 README.md
# ================================================================

def generate_readme(project_name: str, description: str, features: list,
                    tech_stack: list, author: str = "Your Name") -> str:
    """
    生成一个规范的 README.md 内容。

    Args:
        project_name: 项目名称
        description: 项目描述
        features: 功能特性列表
        tech_stack: 技术栈列表
        author: 作者

    Returns:
        README.md 的完整内容
    """
    features_text = "\n".join([f"- {f}" for f in features])
    tech_text = "\n".join([f"- {t}" for t in tech_stack])

    readme = f"""# {project_name}

> {description}

## 功能特性

{features_text}

## 技术栈

{tech_text}

## 快速开始

### 环境要求

- Python 3.9+
- Docker（可选）

### 安装

```bash
# 克隆项目
git clone https://github.com/{author.lower()}/{project_name.lower().replace(' ', '-')}.git
cd {project_name.lower().replace(' ', '-')}

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\\Scripts\\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env，填入你的 API Key
# OPENAI_API_KEY=sk-xxx
# OPENAI_BASE_URL=https://api.openai.com/v1
# MODEL_NAME=gpt-4o-mini
```

### 运行

```bash
# 命令行模式
python -m src.main

# API 模式
uvicorn src.api.app:app --host 0.0.0.0 --port 8000

# Docker 模式
docker-compose up -d
```

## 项目结构

```
{project_name.lower().replace(' ', '-')}/
├── src/
│   ├── document_processing/  # 文档处理模块
│   │   ├── loader.py         # 文档加载
│   │   ├── cleaner.py        # 文本清洗
│   │   └── splitter.py       # 文本切分
│   ├── vector_store/         # 向量存储模块
│   │   └── store.py          # Chroma 向量操作
│   ├── retrieval/            # 检索模块
│   │   └── retriever.py      # 混合检索
│   ├── generation/           # 生成模块
│   │   └── generator.py      # LLM 调用
│   └── api/                  # API 模块
│       └── app.py            # FastAPI 应用
├── tests/                    # 测试代码
├── data/                     # 数据目录
├── docs/                     # 文档
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 部署

```bash
# Docker 部署
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 常见问题

### Q: API Key 在哪里获取？
A: 访问 https://platform.openai.com/api-keys 创建。

### Q: 支持哪些文档格式？
A: 目前支持 TXT、PDF、Markdown、Word。

## 作者

{author}

## 许可证

MIT License
"""
    return readme


# ================================================================
#                    2. 生成 CHANGELOG.md
# ================================================================

def generate_changelog(versions: list) -> str:
    """
    生成 CHANGELOG.md 内容。

    Args:
        versions: 版本列表，每个版本是 dict:
            {
                "version": "1.0.0",
                "date": "2024-06-01",
                "added": ["功能1", "功能2"],
                "changed": ["改进1"],
                "fixed": ["修复1"]
            }

    Returns:
        CHANGELOG.md 的完整内容
    """
    changelog = "# Changelog\n\n"
    changelog += "所有重要变更都会记录在此文件。\n\n"

    for v in versions:
        changelog += f"## [{v['version']}] - {v['date']}\n\n"

        if v.get("added"):
            changelog += "### 新增\n"
            for item in v["added"]:
                changelog += f"- {item}\n"
            changelog += "\n"

        if v.get("changed"):
            changelog += "### 修改\n"
            for item in v["changed"]:
                changelog += f"- {item}\n"
            changelog += "\n"

        if v.get("fixed"):
            changelog += "### 修复\n"
            for item in v["fixed"]:
                changelog += f"- {item}\n"
            changelog += "\n"

    return changelog


# ================================================================
#                    3. 生成架构图
# ================================================================

def generate_ascii_architecture() -> str:
    """生成 ASCII 架构图"""
    return """
┌─────────────────────────────────────────────────────────┐
│                      用户界面层                          │
│              Streamlit / Gradio 聊天界面                 │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────────┐
│                      API 服务层                          │
│                 FastAPI (ASGI)                           │
│           路由 → 校验 → 业务逻辑 → 响应                  │
└───────┬──────────────────┬──────────────────────────────┘
        │                  │
        ▼                  ▼
┌───────────────┐  ┌───────────────┐
│   检索模块     │  │   生成模块     │
│  Retriever    │  │  Generator    │
│               │  │               │
│ · BM25 检索   │  │ · Prompt 构造  │
│ · 向量检索     │  │ · LLM 调用    │
│ · 混合融合     │  │ · 流式输出     │
│ · Re-ranking  │  │ · 来源引用     │
└───────┬───────┘  └───────┬───────┘
        │                  │
        ▼                  ▼
┌───────────────┐  ┌───────────────┐
│  向量数据库    │  │  OpenAI API   │
│    Chroma     │  │   GPT-4o      │
└───────────────┘  └───────────────┘
"""


def generate_mermaid_architecture() -> str:
    """生成 Mermaid 架构图"""
    return """
```mermaid
graph TD
    A[用户] -->|提问| B[前端界面<br/>Streamlit/Gradio]
    B -->|HTTP| C[FastAPI<br/>API服务层]
    C -->|检索请求| D[检索模块<br/>Retriever]
    D -->|BM25| E[关键词索引]
    D -->|向量检索| F[Chroma<br/>向量数据库]
    D -->|重排序| G[Re-ranker]
    C -->|生成请求| H[生成模块<br/>Generator]
    H -->|Prompt| I[OpenAI API<br/>GPT-4o]
    I -->|回答| H
    H -->|结果| C
    C -->|响应| B
    B -->|展示| A

    style A fill:#e1f5fe
    style C fill:#fff3e0
    style F fill:#e8f5e9
    style I fill:#fce4ec
```
"""


# ================================================================
#                    运行演示
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("RAG 项目文档生成器")
    print("=" * 60)

    # --- 1. 生成 README ---
    print("\n【1】生成 README.md")
    print("-" * 40)

    readme_content = generate_readme(
        project_name="RAG-Knowledge-Base",
        description="基于检索增强生成的知识库问答系统",
        features=[
            "多格式文档加载（PDF/TXT/MD/Word）",
            "智能文本切分与向量化",
            "混合检索（BM25 + 向量 + Re-ranking）",
            "流式回答与来源追溯",
            "Docker 一键部署",
        ],
        tech_stack=[
            "FastAPI — Web 框架",
            "LangChain — 大模型编排",
            "Chroma — 向量数据库",
            "OpenAI API — Embedding + LLM",
            "Docker — 容器化部署",
        ],
        author="YourName"
    )

    # 保存到文件
    output_dir = "generated_docs"
    os.makedirs(output_dir, exist_ok=True)

    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"  已保存到: {readme_path}")
    print(f"  文件大小: {len(readme_content)} 字符")

    # --- 2. 生成 CHANGELOG ---
    print("\n【2】生成 CHANGELOG.md")
    print("-" * 40)

    versions = [
        {
            "version": "1.0.0",
            "date": "2024-06-01",
            "added": [
                "支持 TXT、PDF、Markdown、Word 格式文档加载",
                "完整的 RAG 管道（加载→切分→存储→检索→生成）",
                "混合检索（BM25 + 向量检索 + RRF 融合）",
                "Re-ranking 重排序",
                "Streamlit 聊天界面",
                "Docker Compose 部署支持",
            ],
            "changed": [
                "优化文档切分策略，chunk_size 默认改为 500",
                "改进 Prompt 模板，回答质量提升",
            ],
            "fixed": [
                "修复中文文件编码问题",
                "修复 ChromaDB 连接超时问题",
            ],
        },
        {
            "version": "0.2.0",
            "date": "2024-05-15",
            "added": [
                "流式输出支持",
                "来源追溯功能",
            ],
            "changed": [
                "升级到 LangChain v0.2",
            ],
        },
        {
            "version": "0.1.0",
            "date": "2024-05-01",
            "added": [
                "初始版本",
                "基本的 RAG 功能",
                "命令行交互界面",
            ],
        },
    ]

    changelog_content = generate_changelog(versions)
    changelog_path = os.path.join(output_dir, "CHANGELOG.md")
    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write(changelog_content)
    print(f"  已保存到: {changelog_path}")
    print(f"  文件大小: {len(changelog_content)} 字符")

    # --- 3. 生成架构图 ---
    print("\n【3】生成架构图")
    print("-" * 40)

    print("\n  ASCII 架构图:")
    print(generate_ascii_architecture())

    print("  Mermaid 架构图（可直接粘贴到 Markdown 中渲染）:")
    print(generate_mermaid_architecture())

    # 保存架构图
    arch_path = os.path.join(output_dir, "architecture.md")
    with open(arch_path, "w", encoding="utf-8") as f:
        f.write("# 项目架构图\n\n")
        f.write("## ASCII 版本\n")
        f.write("```\n")
        f.write(generate_ascii_architecture())
        f.write("\n```\n\n")
        f.write("## Mermaid 版本\n")
        f.write(generate_mermaid_architecture())
    print(f"  架构图已保存到: {arch_path}")

    # --- 总结 ---
    print("\n" + "=" * 60)
    print("文档生成完毕！")
    print("=" * 60)
    print(f"\n生成的文件：")
    for f in os.listdir(output_dir):
        fpath = os.path.join(output_dir, f)
        size = os.path.getsize(fpath)
        print(f"  📄 {output_dir}/{f} ({size} 字节)")

    print(f"\n💡 提示：这些文件可以直接复制到你的项目根目录使用。")
    print(f"   README.md → 项目根目录")
    print(f"   CHANGELOG.md → 项目根目录")
    print(f"   architecture.md → docs/ 目录")

    # 清理
    import shutil
    shutil.rmtree(output_dir)
    print(f"\n🧹 已清理生成的示例文件（目录: {output_dir}/）")
