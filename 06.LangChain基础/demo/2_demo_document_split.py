"""
Demo 2: 文档加载与切分
====================

功能：
- 创建示例文本文件
- 用 TextLoader 加载文档
- 用 RecursiveCharacterTextSplitter 切分文档

前置条件：
- pip install langchain langchain-community langchain-text-splitters
- 不需要 API Key

对应理论：2.文档处理.md

使用的版本（建议）：
- langchain>=0.2.0
- langchain-community>=0.2.0
- langchain-text-splitters>=0.2.0
"""

import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ============================================================
# 第一部分：创建示例文档
# ============================================================
print("=" * 60)
print("第一部分：创建示例文档")
print("=" * 60)

# 示例知识库内容
sample_content = """RAG（检索增强生成）基础教程

第一章：什么是RAG？
RAG是Retrieval-Augmented Generation的缩写，中文翻译为"检索增强生成"。
它是一种结合了信息检索和文本生成的技术。
RAG的核心思想是：先从知识库中检索相关信息，然后将检索到的信息交给大语言模型，让模型基于这些信息生成答案。

RAG的优势在于：
1. 减少幻觉：模型基于真实文档生成答案，而不是凭空编造。
2. 知识可更新：只需要更新知识库，不需要重新训练模型。
3. 可追溯：可以告诉用户答案来自哪些文档。

第二章：RAG的核心组件
RAG系统由以下几个核心组件构成：
1. 文档加载器（Document Loader）：负责读取各种格式的文档。
2. 文本切分器（Text Splitter）：将长文档切分成小块。
3. 向量数据库（Vector Store）：存储文档的向量表示。
4. 检索器（Retriever）：根据问题检索相关文档。
5. 语言模型（LLM）：基于检索结果生成答案。

第三章：向量检索原理
向量检索是RAG的核心技术之一。
它的工作流程是：
1. 使用Embedding模型将文档转换为向量。
2. 将向量存储到向量数据库中。
3. 用户提问时，将问题也转换为向量。
4. 计算问题向量与所有文档向量的相似度。
5. 返回最相似的文档作为上下文。

常用的相似度计算方法包括余弦相似度和欧氏距离。
余弦相似度衡量的是两个向量的方向相似性，不受向量长度影响。

第四章：实际应用场景
RAG技术在以下场景中有广泛应用：
1. 企业知识库问答：让员工快速找到公司内部文档中的信息。
2. 客户服务：自动回答客户常见问题。
3. 技术文档查询：帮助开发者快速查找API文档。
4. 法律咨询：检索相关法律条文和案例。
5. 医疗问答：基于医学文献回答健康问题。
"""

# 保存为文件
file_path = "knowledge_base.txt"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(sample_content)

print(f"已创建示例文件：{file_path}")
print(f"文件大小：{len(sample_content)} 字符")


# ============================================================
# 第二部分：加载文档
# ============================================================
print("\n" + "=" * 60)
print("第二部分：加载文档")
print("=" * 60)

# 使用 TextLoader 加载文档
loader = TextLoader(file_path, encoding="utf-8")
documents = loader.load()

print(f"加载了 {len(documents)} 个文档")
print(f"文档元数据：{documents[0].metadata}")
print(f"内容前100字符：{documents[0].page_content[:100]}...")


# ============================================================
# 第三部分：文本切分
# ============================================================
print("\n" + "=" * 60)
print("第三部分：文本切分")
print("=" * 60)

# 创建切分器
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,          # 每块最大200字符
    chunk_overlap=30,        # 相邻块重叠30字符
    separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
    length_function=len      # 使用字符长度计算
)

# 切分文档
chunks = splitter.split_documents(documents)

print(f"切分后共 {len(chunks)} 个块")
print(f"\n各块内容预览：")
print("-" * 60)

for i, chunk in enumerate(chunks):
    content_preview = chunk.page_content[:80].replace("\n", " ")
    print(f"块{i+1:2d} [{len(chunk.page_content):3d}字符]：{content_preview}...")


# ============================================================
# 第四部分：不同 chunk_size 对比
# ============================================================
print("\n" + "=" * 60)
print("第四部分：不同 chunk_size 对比")
print("=" * 60)

for size in [100, 200, 500]:
    test_splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=20,
        separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]
    )
    test_chunks = test_splitter.split_documents(documents)
    avg_size = sum(len(c.page_content) for c in test_chunks) / len(test_chunks)
    print(f"chunk_size={size:3d} → 生成 {len(test_chunks):2d} 个块，平均大小 {avg_size:.0f} 字符")


# ============================================================
# 第五部分：查看切分结果
# ============================================================
print("\n" + "=" * 60)
print("第五部分：查看切分详情")
print("=" * 60)

# 显示前3个块的完整内容
for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- 块 {i+1} ---")
    print(f"内容：{chunk.page_content}")
    print(f"元数据：{chunk.metadata}")
    print(f"长度：{len(chunk.page_content)} 字符")


# 清理临时文件
os.remove(file_path)
print(f"\n已清理临时文件：{file_path}")
