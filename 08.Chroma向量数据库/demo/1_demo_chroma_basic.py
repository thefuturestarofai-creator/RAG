"""
Demo 1: Chroma 基础操作
======================

功能：
- 创建 Collection
- 添加文档
- 查询文档
- 元数据过滤
- 持久化存储

前置条件：
- pip install chromadb
- 不需要 API Key（使用 Chroma 内置 Embedding）

对应理论：1.Chroma核心操作.md
"""

import chromadb

# ============================================================
# 第一部分：创建客户端和集合
# ============================================================
print("=" * 60)
print("第一部分：创建客户端和集合")
print("=" * 60)

# 创建持久化客户端（数据保存到磁盘）
client = chromadb.PersistentClient(path="./chroma_demo_db")

# 创建集合（如果已存在则获取）
collection = client.get_or_create_collection(
    name="python_docs",
    metadata={"description": "Python技术文档集合"}
)

print(f"集合名称：{collection.name}")
print(f"集合中的文档数量：{collection.count()}")


# ============================================================
# 第二部分：添加文档
# ============================================================
print("\n" + "=" * 60)
print("第二部分：添加文档")
print("=" * 60)

# 准备文档数据
documents = [
    "Python虚拟环境是一个独立的Python运行环境，允许在不同项目中使用不同版本的包。",
    "使用 pip install 命令可以安装Python包，pip freeze 可以导出依赖列表。",
    "FastAPI是一个现代的Python Web框架，支持异步和自动API文档生成。",
    "RAG是检索增强生成技术，结合了信息检索和文本生成。",
    "向量数据库专门用于存储和检索高维向量数据。",
    "Docker容器是一种轻量级的虚拟化技术，可以打包应用及其依赖。",
    "LangChain是一个用于构建大语言模型应用的框架。",
    "Pydantic使用Python类型提示进行数据验证和序列化。",
    "机器学习是人工智能的一个分支，让计算机从数据中学习规律。",
    "深度学习使用多层神经网络处理复杂的模式识别任务。"
]

# 准备元数据
metadatas = [
    {"source": "venv_guide.txt", "category": "环境管理", "difficulty": "入门"},
    {"source": "pip_guide.txt", "category": "包管理", "difficulty": "入门"},
    {"source": "fastapi_intro.txt", "category": "Web开发", "difficulty": "中级"},
    {"source": "rag_intro.txt", "category": "AI", "difficulty": "中级"},
    {"source": "vectordb_intro.txt", "category": "数据库", "difficulty": "中级"},
    {"source": "docker_intro.txt", "category": "DevOps", "difficulty": "中级"},
    {"source": "langchain_intro.txt", "category": "AI", "difficulty": "中级"},
    {"source": "pydantic_intro.txt", "category": "Web开发", "difficulty": "入门"},
    {"source": "ml_intro.txt", "category": "AI", "difficulty": "高级"},
    {"source": "dl_intro.txt", "category": "AI", "difficulty": "高级"}
]

# 生成文档 ID
ids = [f"doc_{i}" for i in range(len(documents))]

# 添加文档到集合
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"已添加 {len(documents)} 个文档")
print(f"集合中的文档数量：{collection.count()}")


# ============================================================
# 第三部分：查询文档
# ============================================================
print("\n" + "=" * 60)
print("第三部分：查询文档")
print("=" * 60)

# 基础查询
query = "什么是虚拟环境？"
results = collection.query(
    query_texts=[query],
    n_results=3
)

print(f"查询：{query}")
print(f"\n返回 {len(results['ids'][0])} 个结果：")

for i in range(len(results['ids'][0])):
    doc_id = results['ids'][0][i]
    doc = results['documents'][0][i]
    distance = results['distances'][0][i]
    metadata = results['metadatas'][0][i]

    print(f"\n--- 结果 {i+1} ---")
    print(f"ID：{doc_id}")
    print(f"距离：{distance:.4f}")
    print(f"来源：{metadata['source']}")
    print(f"类别：{metadata['category']}")
    print(f"内容：{doc}")


# ============================================================
# 第四部分：元数据过滤
# ============================================================
print("\n" + "=" * 60)
print("第四部分：元数据过滤")
print("=" * 60)

# 按类别过滤
query = "如何安装Python包？"
results = collection.query(
    query_texts=[query],
    n_results=3,
    where={"category": "包管理"}  # 只在"包管理"类别中检索
)

print(f"查询：{query}")
print(f"过滤条件：category = '包管理'")
print(f"\n结果：")
for i in range(len(results['ids'][0])):
    print(f"  [{results['distances'][0][i]:.4f}] {results['documents'][0][i]}")


# 复杂过滤：多条件
print("\n--- 复杂过滤示例 ---")
results = collection.query(
    query_texts=["AI相关技术"],
    n_results=5,
    where={
        "$and": [
            {"category": {"$eq": "AI"}},
            {"difficulty": {"$ne": "高级"}}  # 不等于"高级"
        ]
    }
)

print(f"过滤条件：category='AI' 且 difficulty!='高级'")
print(f"\n结果：")
for i in range(len(results['ids'][0])):
    doc = results['documents'][0][i]
    meta = results['metadatas'][0][i]
    print(f"  [{meta['difficulty']}] {doc[:50]}...")


# ============================================================
# 第五部分：更新和删除文档
# ============================================================
print("\n" + "=" * 60)
print("第五部分：更新和删除文档")
print("=" * 60)

# 更新文档
collection.update(
    ids=["doc_0"],
    documents=["Python虚拟环境（已更新）：venv是Python内置的虚拟环境工具，推荐使用。"],
    metadatas=[{"source": "venv_guide_v2.txt", "category": "环境管理", "difficulty": "入门"}]
)

print("已更新 doc_0")

# 验证更新
result = collection.get(ids=["doc_0"])
print(f"更新后的内容：{result['documents'][0]}")

# 删除文档
collection.delete(ids=["doc_9"])
print("\n已删除 doc_9")
print(f"删除后集合中的文档数量：{collection.count()}")


# ============================================================
# 第六部分：查看集合统计
# ============================================================
print("\n" + "=" * 60)
print("第六部分：集合统计")
print("=" * 60)

# 获取所有文档
all_docs = collection.get()

print(f"集合名称：{collection.name}")
print(f"文档总数：{collection.count()}")

# 统计类别分布
categories = {}
for meta in all_docs['metadatas']:
    cat = meta['category']
    categories[cat] = categories.get(cat, 0) + 1

print(f"\n类别分布：")
for cat, count in categories.items():
    print(f"  {cat}: {count} 个文档")


# ============================================================
# 清理
# ============================================================
print("\n" + "=" * 60)
print("清理")
print("=" * 60)

# 删除集合
client.delete_collection("python_docs")
print("已删除集合 'python_docs'")

# 注意：持久化目录 ./chroma_demo_db 可能仍存在
# 如需完全清理，可手动删除该目录
print("注意：持久化目录 ./chroma_demo_db 已保留，可手动删除")
