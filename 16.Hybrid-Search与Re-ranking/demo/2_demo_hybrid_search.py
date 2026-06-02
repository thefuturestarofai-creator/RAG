"""
Demo 2: 混合检索 - BM25 + 向量检索的 RRF 融合
==============================================

本 Demo 展示如何实现混合检索，将 BM25 稀疏检索和向量稠密检索结合，
使用 RRF（Reciprocal Rank Fusion）算法融合两者的排序结果。

学习目标：
1. 理解混合检索的原理和优势
2. 掌握 RRF 分数融合算法
3. 实现完整的混合检索流程

依赖安装：
pip install rank_bm25 jieba openai chromadb

注意：本 Demo 需要 API Key（用于 embedding）
"""

import json
from typing import List, Dict, Tuple
import jieba
from rank_bm25 import BM25Okapi

# ============================================================
# API 配置
# ============================================================
# 请替换为你的 API Key
API_KEY = "your-api-key-here"
BASE_URL = "https://api.openai.com/v1"  # 或你的 API 地址
MODEL = "text-embedding-ada-002"  # 或你的 embedding 模型


# ============================================================
# 第一部分：RRF 算法实现
# ============================================================

def reciprocal_rank_fusion(
    rankings: List[List[int]],
    k: int = 60
) -> List[Tuple[int, float]]:
    """
    RRF（Reciprocal Rank Fusion）算法实现

    原理：对于每个文档，计算其在所有排名列表中的 RRF 分数
    RRF_score(d) = Σ 1 / (k + rank_i(d))

    参数：
        rankings: 多个排名列表，每个列表包含文档索引
        k: 常数，控制排名衰减速度，默认 60

    返回：
        按 RRF 分数排序的 (文档索引, 分数) 列表
    """
    # 存储每个文档的 RRF 分数
    rrf_scores = {}

    # 遍历每个排名列表
    for ranking in rankings:
        # 遍历排名中的每个文档
        for rank, doc_idx in enumerate(ranking, start=1):
            # 计算 RRF 分数并累加
            if doc_idx not in rrf_scores:
                rrf_scores[doc_idx] = 0
            rrf_scores[doc_idx] += 1.0 / (k + rank)

    # 按分数降序排序
    sorted_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_results


def explain_rrf_formula():
    """
    详细讲解 RRF 公式
    """
    print("\n" + "=" * 60)
    print("RRF 公式详解")
    print("=" * 60)

    print("""
RRF (Reciprocal Rank Fusion) 公式：

    RRF_score(d) = Σ 1 / (k + rank_i(d))

其中：
    - d: 文档
    - k: 常数（通常取 60）
    - rank_i(d): 文档 d 在第 i 个检索器中的排名

举例：
    假设文档 D 在两个检索器中的排名：
    - BM25 排名：第 2 名
    - 向量检索排名：第 5 名
    - k = 60

    RRF 分数 = 1/(60+2) + 1/(60+5)
             = 1/62 + 1/65
             ≈ 0.0161 + 0.0154
             = 0.0315

特点：
    1. 只关心排名，不关心具体分数
    2. 对不同检索器的分数尺度不敏感
    3. 排名越靠前，分数贡献越大
    4. k 值控制衰减速度（k 越大，衰减越慢）
    """)


# ============================================================
# 第二部分：BM25 检索器
# ============================================================

class BM25Retriever:
    """
    BM25 稀疏检索器
    基于关键词匹配的检索方式
    """

    def __init__(self, documents: List[str]):
        """
        初始化 BM25 检索器

        参数：
            documents: 文档列表
        """
        self.documents = documents

        # 对文档进行分词
        self.tokenized_docs = [list(jieba.cut(doc)) for doc in documents]

        # 创建 BM25 索引
        self.bm25 = BM25Okapi(self.tokenized_docs)

        print(f"BM25 检索器初始化完成，共 {len(documents)} 个文档")

    def search(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """
        BM25 检索

        参数：
            query: 查询文本
            top_k: 返回前 k 个结果

        返回：
            (文档索引, 分数) 列表
        """
        # 对查询进行分词
        tokenized_query = list(jieba.cut(query))

        # 获取 BM25 分数
        scores = self.bm25.get_scores(tokenized_query)

        # 按分数排序，返回 top_k
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        results = [(idx, scores[idx]) for idx in ranked_indices[:top_k]]

        return results


# ============================================================
# 第三部分：向量检索器
# ============================================================

class VectorRetriever:
    """
    向量稠密检索器
    基于语义相似度的检索方式
    """

    def __init__(self, documents: List[str]):
        """
        初始化向量检索器

        参数：
            documents: 文档列表
        """
        self.documents = documents
        self.embeddings = []

        # 尝试导入 openai
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
            self.use_openai = True
            print("向量检索器初始化完成（使用 OpenAI API）")
        except ImportError:
            print("警告：未安装 openai 库，将使用随机向量模拟")
            self.use_openai = False

        # 计算文档向量
        self._compute_embeddings()

    def _get_embedding(self, text: str) -> List[float]:
        """
        获取文本的 embedding 向量

        参数：
            text: 输入文本

        返回：
            embedding 向量
        """
        if self.use_openai:
            try:
                response = self.client.embeddings.create(
                    model=MODEL,
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"API 调用失败: {e}，使用随机向量")
                import random
                return [random.random() for _ in range(1536)]
        else:
            # 模拟：使用随机向量
            import random
            # 使用 hash 确保相同文本得到相同向量
            random.seed(hash(text) % 2**32)
            return [random.random() for _ in range(1536)]

    def _compute_embeddings(self):
        """
        计算所有文档的 embedding
        """
        print("正在计算文档向量...")
        self.embeddings = [self._get_embedding(doc) for doc in self.documents]
        print(f"向量计算完成，维度: {len(self.embeddings[0])}")

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        计算余弦相似度

        参数：
            vec1, vec2: 两个向量

        返回：
            余弦相似度（-1 到 1）
        """
        import math

        # 计算点积
        dot_product = sum(a * b for a, b in zip(vec1, vec2))

        # 计算向量长度
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        # 避免除零
        if norm1 == 0 or norm2 == 0:
            return 0

        return dot_product / (norm1 * norm2)

    def search(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """
        向量检索

        参数：
            query: 查询文本
            top_k: 返回前 k 个结果

        返回：
            (文档索引, 分数) 列表
        """
        # 获取查询向量
        query_embedding = self._get_embedding(query)

        # 计算与所有文档的相似度
        similarities = [
            self._cosine_similarity(query_embedding, doc_embedding)
            for doc_embedding in self.embeddings
        ]

        # 按相似度排序
        ranked_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)

        results = [(idx, similarities[idx]) for idx in ranked_indices[:top_k]]

        return results


# ============================================================
# 第四部分：混合检索器
# ============================================================

class HybridRetriever:
    """
    混合检索器
    结合 BM25 和向量检索，使用 RRF 融合排序
    """

    def __init__(self, documents: List[str]):
        """
        初始化混合检索器

        参数：
            documents: 文档列表
        """
        self.documents = documents

        # 初始化两个检索器
        print("\n初始化混合检索器...")
        self.bm25_retriever = BM25Retriever(documents)
        self.vector_retrieever = VectorRetriever(documents)

        print("混合检索器初始化完成！")

    def search(
        self,
        query: str,
        top_k: int = 10,
        bm25_weight: float = 1.0,
        vector_weight: float = 1.0
    ) -> List[Tuple[int, float, Dict]]:
        """
        混合检索

        参数：
            query: 查询文本
            top_k: 返回前 k 个结果
            bm25_weight: BM25 权重
            vector_weight: 向量检索权重

        返回：
            (文档索引, RRF分数, 详细信息) 列表
        """
        print(f"\n执行混合检索: '{query}'")

        # 1. BM25 检索
        bm25_results = self.bm25_retriever.search(query, top_k=top_k * 2)
        bm25_ranking = [idx for idx, _ in bm25_results]
        print(f"  BM25 检索完成，返回 {len(bm25_results)} 个结果")

        # 2. 向量检索
        vector_results = self.vector_retrieever.search(query, top_k=top_k * 2)
        vector_ranking = [idx for idx, _ in vector_results]
        print(f"  向量检索完成，返回 {len(vector_results)} 个结果")

        # 3. RRF 融合
        # 构建带权重的排名列表
        weighted_rankings = []
        for _ in range(int(bm25_weight * 10)):  # 权重放大
            weighted_rankings.append(bm25_ranking)
        for _ in range(int(vector_weight * 10)):
            weighted_rankings.append(vector_ranking)

        rrf_results = reciprocal_rank_fusion(weighted_rankings, k=60)

        # 4. 构建详细结果
        detailed_results = []
        for idx, rrf_score in rrf_results[:top_k]:
            # 获取在各检索器中的排名
            bm25_rank = bm25_ranking.index(idx) + 1 if idx in bm25_ranking else -1
            vector_rank = vector_ranking.index(idx) + 1 if idx in vector_ranking else -1

            detail = {
                "document": self.documents[idx],
                "bm25_rank": bm25_rank,
                "vector_rank": vector_rank,
                "bm25_score": next((s for i, s in bm25_results if i == idx), 0),
                "vector_score": next((s for i, s in vector_results if i == idx), 0),
            }

            detailed_results.append((idx, rrf_score, detail))

        return detailed_results


# ============================================================
# 第五部分：演示混合检索效果
# ============================================================

def demo_hybrid_search():
    """
    演示混合检索的效果
    """
    print("\n" + "=" * 60)
    print("混合检索演示")
    print("=" * 60)

    # 示例文档集合
    documents = [
        "Python是一种广泛使用的高级编程语言，适用于Web开发、数据科学和人工智能",
        "机器学习是人工智能的一个子领域，它使计算机能够从数据中学习",
        "深度学习是机器学习的一个分支，使用多层神经网络进行模式识别",
        "自然语言处理（NLP）涉及计算机与人类语言的交互",
        "TensorFlow和PyTorch是两个流行的深度学习框架",
        "数据预处理是机器学习流程中的重要步骤，包括数据清洗和特征工程",
        "Transformer架构革新了自然语言处理领域",
        "BERT是一种基于Transformer的预训练语言模型",
        "GPT系列模型展示了大语言模型在文本生成方面的能力",
        "RAG（检索增强生成）结合了信息检索和文本生成",
        "向量数据库用于存储和检索高维向量，支持语义搜索",
        "Python的pandas库是数据处理和分析的强大工具",
    ]

    # 创建混合检索器
    hybrid_retriever = HybridRetriever(documents)

    # 测试查询
    test_queries = [
        "深度学习框架有哪些",
        "如何处理数据",
        "NLP相关的技术",
    ]

    for query in test_queries:
        print("\n" + "-" * 60)
        print(f"查询: {query}")

        # 执行混合检索
        results = hybrid_retriever.search(query, top_k=5)

        # 打印结果
        print("\n混合检索结果:")
        for rank, (idx, rrf_score, detail) in enumerate(results, 1):
            print(f"\n  {rank}. [RRF: {rrf_score:.6f}]")
            print(f"     文档: {detail['document'][:50]}...")
            print(f"     BM25排名: {detail['bm25_rank']}, 向量排名: {detail['vector_rank']}")


# ============================================================
# 第六部分：对比分析
# ============================================================

def compare_retrieval_methods():
    """
    对比 BM25、向量检索和混合检索的效果
    """
    print("\n" + "=" * 60)
    print("检索方法对比分析")
    print("=" * 60)

    documents = [
        "苹果公司发布了新款iPhone手机",
        "Apple released the new iPhone smartphone",
        "吃苹果对健康有益",
        "机器学习需要大量数据训练",
        "深度学习是机器学习的子领域",
    ]

    query = "苹果手机"

    print(f"\n查询: {query}")
    print(f"文档数量: {len(documents)}")
    print("\n预期最佳结果: 文档1（苹果公司发布了新款iPhone手机）")

    # BM25 检索
    print("\n1. BM25 检索结果:")
    bm25 = BM25Retriever(documents)
    bm25_results = bm25.search(query, top_k=3)
    for rank, (idx, score) in enumerate(bm25_results, 1):
        print(f"   {rank}. [分数: {score:.4f}] {documents[idx]}")

    print("\n分析: BM25 依赖关键词匹配，'苹果'能匹配到文档1和文档3")

    # 向量检索（概念说明）
    print("\n2. 向量检索结果（概念说明）:")
    print("   如果使用好的 embedding 模型，可能的结果:")
    print("   1. 苹果公司发布了新款iPhone手机（语义最相关）")
    print("   2. Apple released the new iPhone smartphone（语义相同）")
    print("   3. 吃苹果对健康有益（'苹果'的另一种含义）")

    print("\n分析: 向量检索能理解语义，区分'苹果公司'和'水果苹果'")

    # 混合检索
    print("\n3. 混合检索优势:")
    print("   - 结合 BM25 的精确匹配和向量的语义理解")
    print("   - RRF 融合确保两个检索器都认可的文档排名更高")
    print("   - 文档1 在两种检索中都应该排名靠前")


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("混合检索 Demo")
    print("=" * 60)

    # 运行各个 Demo
    explain_rrf_formula()
    demo_hybrid_search()
    compare_retrieval_methods()

    print("\n" + "=" * 60)
    print("Demo 完成！")
    print("=" * 60)
