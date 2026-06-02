"""
Demo 2: 批量目录加载

本 Demo 演示如何用 DirectoryLoader 批量加载一个目录下的所有文档：
1. 创建包含多种格式文件的目录
2. 用 DirectoryLoader 批量加载
3. 展示加载结果的统计和分析

用法：
    python 2_demo_directory_loader.py

注意：LangChain 的 loader 本身不需要 API Key。
"""

import os
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ============================================================
# 第一步：创建模拟的文档目录
# ============================================================

def create_sample_directory():
    """创建一个包含多种格式文件的示例目录。"""

    base_dir = os.path.join(os.path.dirname(__file__), "sample_docs")
    os.makedirs(base_dir, exist_ok=True)

    # 创建子目录
    subdirs = ["技术文档", "产品手册", "常见问题"]
    for subdir in subdirs:
        os.makedirs(os.path.join(base_dir, subdir), exist_ok=True)

    # ---- 技术文档 ----
    tech_docs = {
        "RAG架构设计.txt": """\
RAG（检索增强生成）系统架构设计

一、系统概述
RAG系统通过检索外部知识库来增强大语言模型的回答能力。
核心流程：文档加载 → 切分 → 向量化 → 存储 → 检索 → 生成。

二、模块划分
1. 文档处理模块：负责加载、清洗、切分文档
2. 向量存储模块：管理向量数据库
3. 检索模块：执行相似度搜索
4. 生成模块：调用LLM生成回答

三、技术选型
- 向量数据库：Chroma / Milvus / FAISS
- Embedding模型：text-embedding-ada-002
- LLM：GPT-3.5-turbo / GPT-4
""",
        "向量数据库选型.txt": """\
向量数据库选型指南

1. Chroma
   - 优点：轻量、Python原生、易于上手
   - 缺点：性能一般，不适合大规模数据
   - 适用：原型开发、小项目

2. Milvus
   - 优点：高性能、分布式、企业级
   - 缺点：部署复杂、资源消耗大
   - 适用：生产环境、大规模数据

3. FAISS
   - 优点：Facebook开源、性能极高
   - 缺点：不支持持久化、需要自己管理
   - 适用：大规模向量搜索、研究场景
""",
    }

    # ---- 产品手册 ----
    product_docs = {
        "用户手册.txt": """\
StarChat 用户手册

第一章：快速开始
1. 注册账号并登录
2. 创建知识库
3. 上传文档
4. 开始对话

第二章：知识库管理
- 支持上传PDF、TXT、MD格式文档
- 单个文件最大50MB
- 支持批量上传

第三章：对话功能
- 支持多轮对话
- 支持查看来源引用
- 支持反馈和评价
""",
        "API文档.md": """\
# StarChat API 文档

## 基础信息
- Base URL: https://api.startech.com/v1
- 认证方式: Bearer Token

## 接口列表

### POST /query
用户提问接口

**请求参数:**
```json
{
    "question": "什么是RAG?",
    "top_k": 3
}
```

**响应:**
```json
{
    "answer": "RAG是...",
    "sources": ["doc1.txt", "doc2.pdf"]
}
```

### POST /upload
上传文档接口
- Content-Type: multipart/form-data
- 支持格式: PDF, TXT, MD
""",
    }

    # ---- 常见问题 ----
    faq_docs = {
        "安装问题.txt": """\
常见安装问题

Q: 安装时报错 "pip not found"
A: 请确保已安装Python并添加到PATH环境变量

Q: 安装依赖超时
A: 使用国内镜像源：pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

Q: 启动报错 "port already in use"
A: 修改配置文件中的端口号，或关闭占用该端口的程序
""",
        "使用问题.txt": """\
常见使用问题

Q: 上传文档后无法检索到
A: 请检查文档是否已成功入库（查看知识库页面的文档列表）

Q: 回答不准确怎么办
A: 1. 检查知识库中的文档质量
   2. 尝试调整检索数量（top_k参数）
   3. 优化文档的切分方式

Q: 响应速度慢
A: 1. 减少检索数量
   2. 使用更快的Embedding模型
   3. 升级服务器配置
""",
    }

    # 写入所有文件
    all_files = {
        "技术文档": tech_docs,
        "产品手册": product_docs,
        "常见问题": faq_docs,
    }

    file_count = 0
    for subdir, files in all_files.items():
        for filename, content in files.items():
            file_path = os.path.join(base_dir, subdir, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            file_count += 1
            print(f"  ✓ 创建: {subdir}/{filename}")

    print(f"\n  共创建 {file_count} 个文件，分布在 {len(subdirs)} 个子目录中")
    return base_dir


# ============================================================
# 第二步：DirectoryLoader 批量加载
# ============================================================

def demo_directory_loader(data_dir: str):
    """演示 DirectoryLoader 的用法。"""

    print("\n" + "=" * 60)
    print("  演示 1: DirectoryLoader 基本用法")
    print("=" * 60)

    try:
        from langchain_community.document_loaders import DirectoryLoader, TextLoader

        # 加载所有 .txt 文件
        loader = DirectoryLoader(
            path=data_dir,
            glob="**/*.txt",                    # 递归匹配所有 .txt 文件
            loader_cls=TextLoader,              # 使用 TextLoader 处理每个文件
            loader_kwargs={"encoding": "utf-8"},# TextLoader 的参数
            show_progress=True,                 # 显示进度
            silent_errors=True,                 # 遇到错误继续（不中断）
        )

        docs = loader.load()

        print(f"\n  加载结果:")
        print(f"  文档总数: {len(docs)}")

        # 统计每个子目录的文档数
        source_count = {}
        for doc in docs:
            # 从完整路径中提取子目录名
            source = doc.metadata.get("source", "")
            parts = source.split(os.sep)
            if len(parts) >= 2:
                subdir = parts[-2]
            else:
                subdir = "根目录"
            source_count[subdir] = source_count.get(subdir, 0) + 1

        print(f"\n  按目录统计:")
        for subdir, count in source_count.items():
            print(f"    {subdir}: {count} 个文档")

        # 显示每个文档的信息
        print(f"\n  文档详情:")
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "未知")
            filename = os.path.basename(source)
            content_len = len(doc.page_content)
            print(f"    {i}. {filename} ({content_len} 字符)")

        return docs

    except ImportError:
        print("  langchain 未安装，展示代码示例:")
        print("""
  from langchain_community.document_loaders import DirectoryLoader, TextLoader

  # 基本用法：加载目录下所有 .txt 文件
  loader = DirectoryLoader(
      path="data/documents/",
      glob="**/*.txt",
      loader_cls=TextLoader,
      loader_kwargs={"encoding": "utf-8"},
      show_progress=True,
      use_multithreading=True,  # 多线程加速
  )
  docs = loader.load()
        """)
        return []


def demo_multi_format_directory(data_dir: str):
    """演示加载多种格式的文件。"""

    print("\n" + "=" * 60)
    print("  演示 2: 加载多种格式的文件")
    print("=" * 60)

    try:
        from langchain_community.document_loaders import DirectoryLoader, TextLoader

        all_docs = []

        # 加载 .txt 文件
        txt_loader = DirectoryLoader(
            path=data_dir,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
            silent_errors=True,
        )
        txt_docs = txt_loader.load()
        print(f"\n  TXT 文件: {len(txt_docs)} 个")
        all_docs.extend(txt_docs)

        # 加载 .md 文件
        md_loader = DirectoryLoader(
            path=data_dir,
            glob="**/*.md",
            loader_cls=TextLoader,  # 也可以用 TextLoader 加载 .md
            loader_kwargs={"encoding": "utf-8"},
            silent_errors=True,
        )
        md_docs = md_loader.load()
        print(f"  MD  文件: {len(md_docs)} 个")
        all_docs.extend(md_docs)

        print(f"  总计: {len(all_docs)} 个文档")

        return all_docs

    except ImportError:
        print("  langchain 未安装")
        return []


# ============================================================
# 第三步：加载结果分析
# ============================================================

def analyze_documents(docs: list):
    """分析加载的文档统计信息。"""

    print("\n" + "=" * 60)
    print("  文档分析")
    print("=" * 60)

    if not docs:
        print("  没有文档可分析")
        return

    # 基本统计
    total_chars = sum(len(doc.page_content) for doc in docs)
    avg_chars = total_chars / len(docs) if docs else 0
    min_chars = min(len(doc.page_content) for doc in docs)
    max_chars = max(len(doc.page_content) for doc in docs)

    print(f"\n  文档数量: {len(docs)}")
    print(f"  总字符数: {total_chars:,}")
    print(f"  平均长度: {avg_chars:,.0f} 字符")
    print(f"  最短文档: {min_chars} 字符")
    print(f"  最长文档: {max_chars} 字符")

    # 文件类型统计
    type_count = {}
    for doc in docs:
        source = doc.metadata.get("source", "")
        ext = os.path.splitext(source)[1] or "无扩展名"
        type_count[ext] = type_count.get(ext, 0) + 1

    print(f"\n  文件类型分布:")
    for ext, count in type_count.items():
        print(f"    {ext}: {count} 个 ({count/len(docs)*100:.1f}%)")

    # 长度分布
    print(f"\n  长度分布:")
    ranges = [(0, 200), (200, 500), (500, 1000), (1000, float('inf'))]
    for low, high in ranges:
        count = sum(1 for doc in docs if low <= len(doc.page_content) < high)
        if count > 0:
            label = f"{low}-{high if high != float('inf') else '∞'}"
            print(f"    {label} 字符: {count} 个")


# ============================================================
# 第四步：手动遍历目录（不依赖 LangChain）
# ============================================================

def demo_manual_loading(data_dir: str):
    """不使用 LangChain，手动遍历目录加载文件。"""

    print("\n" + "=" * 60)
    print("  演示 3: 手动遍历目录（不依赖 LangChain）")
    print("=" * 60)

    supported_exts = {'.txt', '.md', '.csv'}
    docs = []

    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in supported_exts:
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 模拟 Document 对象
                    doc = {
                        "page_content": content,
                        "metadata": {
                            "source": file_path,
                            "filename": filename,
                        }
                    }
                    docs.append(doc)
                    print(f"  ✓ 加载: {os.path.relpath(file_path, data_dir)}")

                except Exception as e:
                    print(f"  ✗ 失败: {filename} ({e})")

    print(f"\n  手动加载完成，共 {len(docs)} 个文档")
    return docs


# ============================================================
# 主函数
# ============================================================

def main():
    print("=" * 60)
    print("  批量目录加载 Demo")
    print("=" * 60)

    # 1. 创建示例目录
    print("\n[第一步] 创建示例文档目录:")
    data_dir = create_sample_directory()

    # 2. DirectoryLoader 加载
    print("\n[第二步] 使用 DirectoryLoader 加载:")
    docs = demo_directory_loader(data_dir)

    # 3. 多格式加载
    all_docs = demo_multi_format_directory(data_dir)

    # 4. 分析结果
    analyze_documents(all_docs if all_docs else docs)

    # 5. 手动加载演示
    demo_manual_loading(data_dir)

    # 总结
    print("\n" + "=" * 60)
    print("  总结")
    print("=" * 60)
    print("""
  DirectoryLoader 的关键用法:
  1. path: 指定目录路径
  2. glob: 用通配符匹配文件（**/*.txt 匹配所有子目录）
  3. loader_cls: 指定用哪个 Loader 处理每个文件
  4. loader_kwargs: 传给 Loader 的额外参数
  5. show_progress: 显示加载进度
  6. silent_errors: 遇到错误不中断

  如果不想依赖 LangChain，可以用 os.walk() 手动遍历目录，
  效果一样，只是需要自己处理文件读取和错误。
    """)

    print("Demo 运行完成!")


if __name__ == "__main__":
    main()
