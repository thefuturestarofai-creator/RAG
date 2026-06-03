"""
Demo 2: Chroma + LangChain 集成
===============================

功能：
- 用 LangChain 的 Chroma 封装实现向量存储和检索
- 演示完整的 RAG 检索流程

前置条件：
- pip install langchain langchain-openai langchain-community langchain-chroma chromadb
- 需要 API Key

对应理论：1.Chroma核心操作.md + 2.向量检索原理.md

使用的版本（建议）：
- langchain>=0.2.0
- langchain-openai>=0.1.0
- langchain-chroma>=0.1.0
- chromadb>=0.5.0
"""

import os
import shutil
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# ============================================================
# 请填写你的模型配置
# ============================================================
API_KEY = "your-api-key-here"       # 替换为你的 API Key
BASE_URL = "https://api.openai.com/v1"  # 替换为你的 Base URL


# ============================================================
# 第一部分：创建文档和向量数据库
# ============================================================
print("=" * 60)
print("第一部分：创建文档和向量数据库")
print("=" * 60)

# 准备 LangChain Document 对象
documents = [
    Document(
        page_content="Python虚拟环境是一个独立的Python运行环境，允许在不同项目中使用不同版本的包，避免版本冲突。",
        metadata={"source": "venv_guide.txt", "category": "环境管理", "page": 1}
    ),
    Document(
        page_content="使用 venv 模块创建虚拟环境：python -m venv myenv，然后使用 activate 命令激活。",
        metadata={"source": "venv_guide.txt", "category": "环境管理", "page": 2}
    ),
    Document(
        page_content="pip是Python的包管理工具，使用 pip install 安装包，pip freeze 导出依赖列表到 requirements.txt。",
        metadata={"source": "pip_guide.txt", "category": "包管理", "page": 1}
    ),
    Document(
        page_content="FastAPI是一个现代的Python Web框架，支持异步处理、自动API文档生成和Pydantic数据验证。",
        metadata={"source": "fastapi_intro.txt", "category": "Web开发", "page": 1}
    ),
    Document(
        page_content="RAG（检索增强生成）技术结合了信息检索和文本生成，先从知识库检索相关文档，再让LLM生成答案。",
        metadata={"source": "rag_intro.txt", "category": "AI", "page": 1}
    ),
    Document(
        page_content="向量数据库如Chroma专门用于存储和检索高维向量数据，支持语义相似度搜索。",
        metadata={"source": "vectordb_intro.txt", "category": "数据库", "page": 1}
    ),
    Document(
        page_content="Docker容器技术可以将应用及其依赖打包成标准化的单元，实现一次构建到处运行。",
        metadata={"source": "docker_intro.txt", "category": "DevOps", "page": 1}
    ),
    Document(
        page_content="LangChain框架提供了构建大语言模型应用的工具，包括Chain、Agent、Memory等核心组件。",
        metadata={"source": "langchain_intro.txt", "category": "AI", "page": 1}
    ),
]

print(f"准备了 {len(documents)} 个文档")


# ============================================================
# 第二部分：创建向量数据库
# ============================================================
print("\n" + "=" * 60)
print("第二部分：创建向量数据库（Embedding + Chroma）")
print("=" * 60)

# 创建 Embedding 模型
embeddings = OpenAIEmbeddings(
    api_key=API_KEY,
    base_url=BASE_URL,
    model="text-embedding-3-small"
)

# 创建持久化目录
persist_dir = "./chroma_langchain_db"
if os.path.exists(persist_dir):
    shutil.rmtree(persist_dir)

# 创建向量数据库
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory=persist_dir,
    collection_name="tech_docs"
)

print(f"向量数据库已创建，存储目录：{persist_dir}")
print(f"已存储 {vectorstore._collection.count()} 个文档")


# ============================================================
# 第三部分：基础检索
# ============================================================
print("\n" + "=" * 60)
print("第三部分：基础相似度检索")
print("=" * 60)

# 创建检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 测试检索
queries = [
    "什么是虚拟环境？",
    "如何构建RAG系统？",
    "Docker是什么？"
]

for query in queries:
    print(f"\n查询：{query}")
    print("-" * 40)

    docs = retriever.invoke(query)
    for i, doc in enumerate(docs):
        print(f"  结果{i+1} [{doc.metadata['category']}]：{doc.page_content[:60]}...")


# ============================================================
# 第四部分：带分数的检索
# ============================================================
print("\n" + "=" * 60)
print("第四部分：带相似度分数的检索")
print("=" * 60)

query = "Python包管理"
print(f"查询：{query}")

# 使用 similarity_score_threshold 获取分数
retriever_with_score = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 5, "score_threshold": 0.3}
)

docs_with_score = vectorstore.similarity_search_with_score(query, k=5)

print("\n检索结果（含相似度分数）：")
for doc, score in docs_with_score:
    # Chroma 返回的是 L2 距离，越小越相似
    print(f"  [距离={score:.4f}] {doc.page_content[:60]}...")


# ============================================================
# 第五部分：元数据过滤检索
# ============================================================
print("\n" + "=" * 60)
print("第五部分：元数据过滤检索")
print("=" * 60)

# 只在 AI 类别中检索
query = "智能问答系统"
print(f"查询：{query}")
print("过滤条件：category = 'AI'")

docs = vectorstore.similarity_search(
    query,
    k=3,
    filter={"category": "AI"}
)

print("\n结果：")
for i, doc in enumerate(docs):
    print(f"  {i+1}. [{doc.metadata['category']}] {doc.page_content[:60]}...")


# ============================================================
# 第六部分：添加新文档
# ============================================================
print("\n" + "=" * 60)
print("第六部分：添加新文档")
print("=" * 60)

# 添加新文档
new_docs = [
    Document(
        page_content="Embedding是将文本转换为向量的技术，语义相近的文本会产生相似的向量。",
        metadata={"source": "embedding_intro.txt", "category": "AI", "page": 1}
    )
]

# 添加到现有数据库
vectorstore.add_documents(new_docs)

print(f"已添加 1 个新文档")
print(f"当前文档总数：{vectorstore._collection.count()}")

# 验证新文档可被检索
query = "什么是Embedding？"
print(f"\n验证检索 - 查询：{query}")
docs = vectorstore.similarity_search(query, k=1)
print(f"结果：{docs[0].page_content}")


# ============================================================
# 第七部分：删除文档
# ============================================================
print("\n" + "=" * 60)
print("第七部分：删除文档")
print("=" * 60)

# 获取所有文档的 ID
all_data = vectorstore._collection.get()
print(f"删除前文档数量：{vectorstore._collection.count()}")

# 删除特定文档
vectorstore._collection.delete(ids=[all_data['ids'][0]])
print(f"已删除文档：{all_data['ids'][0]}")
print(f"删除后文档数量：{vectorstore._collection.count()}")


# ============================================================
# 清理
# ============================================================
print("\n" + "=" * 60)
print("清理")
print("=" * 60)

# 删除向量数据库目录
if os.path.exists(persist_dir):
    shutil.rmtree(persist_dir)
    print(f"已删除目录：{persist_dir}")

print("清理完成！")
