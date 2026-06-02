"""
Demo 1: 多格式文档加载

本 Demo 演示如何用 LangChain 加载不同格式的文档：
1. 加载 TXT 文件
2. 加载 Markdown 文件
3. 加载 PDF 文件（用代码模拟）

同时会创建示例数据文件供加载。

用法：
    python 1_demo_multi_format_loader.py

注意：LangChain 的 loader 本身不需要 API Key，
但如果你要对加载的文档做 Embedding，就需要 API Key。
"""

import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 第一步：创建示例数据文件
# ============================================================

def create_sample_files():
    """创建示例的 txt 和 md 文件，供后续加载。"""

    # 创建数据目录
    data_dir = os.path.join(os.path.dirname(__file__), "sample_data")
    os.makedirs(data_dir, exist_ok=True)

    # ---- 示例 TXT 文件 1：公司简介 ----
    txt_content_1 = """\
星辰科技有限公司简介

星辰科技成立于2020年，是一家专注于人工智能技术研发的高科技公司。
公司总部位于北京中关村科技园，现有员工200余人。

核心业务：
1. 自然语言处理（NLP）解决方案
2. 计算机视觉系统开发
3. 智能客服机器人
4. 企业知识库建设

公司愿景：让AI技术赋能每一个企业。
公司使命：用技术创造价值，以创新引领未来。

联系方式：
地址：北京市海淀区中关村大街1号
电话：010-12345678
邮箱：contact@startech.com
"""

    # ---- 示例 TXT 文件 2：产品说明 ----
    txt_content_2 = """\
StarChat 智能客服系统 - 产品说明书

版本：V2.0
发布日期：2024年6月

一、产品概述
StarChat 是星辰科技自主研发的智能客服系统，基于大语言模型技术，
能够理解用户的自然语言问题，并给出准确、专业的回答。

二、核心功能
1. 智能问答：支持多轮对话，理解上下文语境
2. 知识库管理：支持多种文档格式导入，自动构建知识库
3. 多渠道接入：支持网页、微信、APP等多渠道
4. 数据分析：自动生成对话统计报告

三、技术规格
- 响应时间：< 2秒
- 准确率：> 95%
- 并发支持：1000+ 同时在线
- 支持语言：中文、英文

四、定价方案
- 基础版：999元/月，支持1000次/天
- 专业版：2999元/月，支持10000次/天
- 企业版：面议，不限次数
"""

    # ---- 示例 Markdown 文件：技术文档 ----
    md_content = """\
# RAG 系统部署指南

## 环境要求

- Python 3.9+
- 内存：8GB+
- 磁盘：10GB+

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/startech/rag-system.git
cd rag-system
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件：

```
OPENAI_API_KEY=your-api-key
CHROMA_PERSIST_DIR=./data/chroma_db
```

### 4. 启动服务

```bash
python -m src.main
```

## 常见问题

### Q: 启动报错 "Module not found"
A: 请确保已安装所有依赖：`pip install -r requirements.txt`

### Q: 向量数据库连接失败
A: 检查 `CHROMA_PERSIST_DIR` 路径是否有写入权限

## 更新日志

- v1.0.0 (2024-01): 初始版本
- v1.1.0 (2024-03): 新增 PDF 支持
- v2.0.0 (2024-06): 全面重构，性能提升 50%
"""

    # 写入文件
    files = {
        "company_intro.txt": txt_content_1,
        "product_spec.txt": txt_content_2,
        "deployment_guide.md": md_content,
    }

    for filename, content in files.items():
        file_path = os.path.join(data_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ 创建文件: sample_data/{filename}")

    return data_dir


# ============================================================
# 第二步：演示各种 Loader 的用法
# ============================================================

def demo_text_loader(data_dir: str):
    """演示 TextLoader 加载 TXT 文件。"""
    print("\n" + "=" * 60)
    print("  演示 1: TextLoader 加载 TXT 文件")
    print("=" * 60)

    try:
        from langchain_community.document_loaders import TextLoader

        # 加载单个 TXT 文件
        file_path = os.path.join(data_dir, "company_intro.txt")
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()

        print(f"\n  加载文件: company_intro.txt")
        print(f"  文档数量: {len(docs)}")
        print(f"  内容长度: {len(docs[0].page_content)} 字符")
        print(f"  元数据: {docs[0].metadata}")
        print(f"\n  内容预览（前200字符）:")
        print(f"  {docs[0].page_content[:200]}...")

        return docs

    except ImportError:
        print("  langchain 未安装，展示代码示例:")
        print("""
  # TextLoader 用法
  from langchain_community.document_loaders import TextLoader

  loader = TextLoader("data.txt", encoding="utf-8")
  docs = loader.load()
  # docs[0].page_content = "文件内容..."
  # docs[0].metadata = {"source": "data.txt"}
        """)
        return []


def demo_markdown_loader(data_dir: str):
    """演示 Markdown 文件加载。"""
    print("\n" + "=" * 60)
    print("  演示 2: 加载 Markdown 文件")
    print("=" * 60)

    try:
        from langchain_community.document_loaders import UnstructuredMarkdownLoader

        file_path = os.path.join(data_dir, "deployment_guide.md")
        loader = UnstructuredMarkdownLoader(file_path)
        docs = loader.load()

        print(f"\n  加载文件: deployment_guide.md")
        print(f"  文档数量: {len(docs)}")
        print(f"  元数据: {docs[0].metadata}")
        print(f"\n  内容预览（前200字符）:")
        print(f"  {docs[0].page_content[:200]}...")

        return docs

    except ImportError:
        print("  unstructured 未安装，展示代码示例:")
        print("""
  # MarkdownLoader 用法
  from langchain_community.document_loaders import UnstructuredMarkdownLoader

  loader = UnstructuredMarkdownLoader("README.md")
  docs = loader.load()
        """)
        return []


def demo_pdf_loader():
    """演示 PDF 加载（代码模拟）。"""
    print("\n" + "=" * 60)
    print("  演示 3: PDF 加载（代码模拟）")
    print("=" * 60)

    print("""
  PDF 加载需要安装额外的库：

  # 方式一：使用 PDFPlumberLoader（推荐）
  pip install pdfplumber
  from langchain_community.document_loaders import PDFPlumberLoader

  loader = PDFPlumberLoader("report.pdf")
  docs = loader.load()
  # 每页生成一个 Document
  # docs[0].metadata = {"source": "report.pdf", "page": 0}
  # docs[1].metadata = {"source": "report.pdf", "page": 1}

  # 方式二：使用 PyPDFLoader（轻量）
  pip install pypdf
  from langchain_community.document_loaders import PyPDFLoader

  loader = PyPDFLoader("report.pdf")
  docs = loader.load_and_split()  # 加载并切分
    """)

    # 模拟 PDF 加载结果
    simulated_docs = [
        {
            "page_content": "第一章 公司概述\n星辰科技有限公司成立于2020年...",
            "metadata": {"source": "report.pdf", "page": 0}
        },
        {
            "page_content": "第二章 产品介绍\nStarChat智能客服系统...",
            "metadata": {"source": "report.pdf", "page": 1}
        },
    ]

    print("  模拟 PDF 加载结果:")
    for i, doc in enumerate(simulated_docs):
        print(f"    第 {i+1} 页: {doc['page_content'][:50]}...")
        print(f"    元数据: {doc['metadata']}")

    return []


# ============================================================
# 第三步：统一的 Document 对象
# ============================================================

def demo_unified_document():
    """演示统一的 Document 对象格式。"""
    print("\n" + "=" * 60)
    print("  统一的 Document 对象格式")
    print("=" * 60)

    try:
        from langchain.schema import Document

        # 创建 Document 对象
        doc = Document(
            page_content="这是一段文档内容，用于演示 Document 对象。",
            metadata={
                "source": "example.txt",
                "page": 1,
                "author": "张三",
            }
        )

        print(f"\n  Document 对象:")
        print(f"    page_content: {doc.page_content}")
        print(f"    metadata: {doc.metadata}")
        print(f"    来源: {doc.metadata.get('source', '未知')}")
        print(f"    页码: {doc.metadata.get('page', '未知')}")

    except ImportError:
        print("  langchain 未安装，展示 Document 结构:")
        print("""
  Document(
      page_content="文本内容",    # 必填：文档的文本内容
      metadata={                   # 可选：元数据字典
          "source": "file.txt",    # 来源文件
          "page": 1,              # 页码
          "author": "张三",        # 作者
      }
  )
        """)


# ============================================================
# 主函数
# ============================================================

def main():
    print("=" * 60)
    print("  多格式文档加载 Demo")
    print("=" * 60)

    # 1. 创建示例文件
    print("\n[第一步] 创建示例数据文件:")
    data_dir = create_sample_files()

    # 2. 演示各种 Loader
    print("\n[第二步] 演示各种文档加载器:")
    txt_docs = demo_text_loader(data_dir)
    md_docs = demo_markdown_loader(data_dir)
    pdf_docs = demo_pdf_loader()

    # 3. 统一的 Document 对象
    demo_unified_document()

    # 总结
    print("\n" + "=" * 60)
    print("  总结")
    print("=" * 60)
    print("""
  文档加载的关键点:
  1. 不同格式用不同的 Loader，但输出都是 Document 对象
  2. Document 包含 page_content（内容）和 metadata（元数据）
  3. metadata 记录来源信息，用于后续的来源追溯
  4. 中文文件注意编码问题（encoding="utf-8"）
  5. PDF 按页拆分，每页一个 Document

  常用加载器:
  ├── TextLoader           → .txt 文件
  ├── PDFPlumberLoader     → .pdf 文件
  ├── UnstructuredMarkdownLoader → .md 文件
  └── DirectoryLoader      → 批量加载目录
    """)

    print("Demo 运行完成!")


if __name__ == "__main__":
    main()
