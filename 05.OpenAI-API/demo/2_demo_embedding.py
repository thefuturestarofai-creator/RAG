"""
Demo 2: Embedding - 文本转向量 + 余弦相似度
=============================================

功能：
- 把文本变成向量
- 用 numpy 计算余弦相似度
- 找到最相似的句子

前置条件：
- pip install openai numpy
- 需要 API Key

对应理论：2.Embedding API.md
"""

import numpy as np
from openai import OpenAI

# ============================================================
# 请填写你的模型配置
# ============================================================
API_KEY = "your-api-key-here"       # 替换为你的 API Key
BASE_URL = "https://api.openai.com/v1"  # 替换为你的 Base URL
EMBEDDING_MODEL = "text-embedding-3-small"  # 推荐：text-embedding-3-small（便宜、效果好）

# 创建客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


# ============================================================
# 第一部分：基础 Embedding 操作
# ============================================================
print("=" * 60)
print("第一部分：将文本转换为向量")
print("=" * 60)

def get_embedding(text):
    """
    获取文本的 Embedding 向量

    参数：
        text: 要转换的文本字符串

    返回：
        list: 包含 1536 个浮点数的向量
    """
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


# 测试：将一句话转换为向量
sample_text = "RAG是一种结合检索和生成的AI技术"
vector = get_embedding(sample_text)

print(f"原文：{sample_text}")
print(f"向量维度：{len(vector)}")
print(f"前10个数字：{vector[:10]}")
print(f"向量类型：{type(vector)}")


# ============================================================
# 第二部分：余弦相似度计算
# ============================================================
print("\n" + "=" * 60)
print("第二部分：余弦相似度计算")
print("=" * 60)

def cosine_similarity(vec_a, vec_b):
    """
    计算两个向量的余弦相似度（使用 numpy）

    参数：
        vec_a: 向量A（列表或数组）
        vec_b: 向量B（列表或数组）

    返回：
        float: 余弦相似度，范围 [-1, 1]
               1 表示完全相同，0 表示无关，-1 表示相反
    """
    # 转换为 numpy 数组
    a = np.array(vec_a)
    b = np.array(vec_b)

    # 计算点积：A · B = a1*b1 + a2*b2 + ...
    dot_product = np.dot(a, b)

    # 计算向量的模（长度）：|A| = sqrt(a1^2 + a2^2 + ...)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    # 余弦相似度 = 点积 / (模的乘积)
    return dot_product / (norm_a * norm_b)


# 测试：两个相同向量的相似度
test_vec = [1.0, 2.0, 3.0]
print(f"自身与自身的余弦相似度：{cosine_similarity(test_vec, test_vec):.4f}")  # 应该是 1.0


# ============================================================
# 第三部分：语义相似度实战
# ============================================================
print("\n" + "=" * 60)
print("第三部分：找最相似的句子")
print("=" * 60)

# 知识库：一组待检索的句子
documents = [
    "Python是一种简洁易学的编程语言",
    "机器学习是人工智能的一个分支",
    "深度学习使用神经网络处理复杂数据",
    "RAG技术让大语言模型能够检索外部知识",
    "向量数据库专门用于存储和检索高维向量",
    "今天天气真好，适合出去散步",
    "自然语言处理让计算机理解人类语言",
    "Embedding将文本转换为数字向量表示"
]

# 查询：用户的问题
query = "什么是向量检索？"

print(f"查询：{query}")
print(f"\n正在计算 {len(documents)} 个文档的 Embedding...")

# 1. 计算查询的向量
query_vector = get_embedding(query)

# 2. 计算所有文档的向量
doc_vectors = []
for doc in documents:
    vec = get_embedding(doc)
    doc_vectors.append(vec)

# 3. 计算查询与每个文档的相似度
similarities = []
for i, doc_vec in enumerate(doc_vectors):
    sim = cosine_similarity(query_vector, doc_vec)
    similarities.append((i, sim))

# 4. 按相似度降序排序
similarities.sort(key=lambda x: x[1], reverse=True)

# 5. 显示结果
print("\n按相似度排序的结果：")
print("-" * 60)
for rank, (idx, sim) in enumerate(similarities, 1):
    print(f"第{rank}名 [{sim:.4f}] {documents[idx]}")

# ============================================================
# 第四部分：批量 Embedding（节省 API 调用次数）
# ============================================================
print("\n" + "=" * 60)
print("第四部分：批量 Embedding")
print("=" * 60)

batch_texts = [
    "人工智能改变世界",
    "AI正在革新各行各业",
    "今天中午吃什么"
]

# 一次调用获取多个文本的 Embedding
response = client.embeddings.create(
    model=EMBEDDING_MODEL,
    input=batch_texts  # 传入列表，批量处理
)

print(f"批量处理了 {len(response.data)} 个文本")
for i, item in enumerate(response.data):
    print(f"  文本{i+1} 的向量维度：{len(item.embedding)}")

# 计算批量结果的相似度矩阵
print("\n相似度矩阵：")
print("-" * 40)
vectors = [item.embedding for item in response.data]
for i in range(len(batch_texts)):
    for j in range(len(batch_texts)):
        sim = cosine_similarity(vectors[i], vectors[j])
        print(f"  [{i+1}vs{j+1}] {sim:.4f}", end="")
    print(f"  | {batch_texts[i]}")

print("\n注意：语义相近的句子（1和2）相似度较高，与不相关的句子（3）相似度较低。")
