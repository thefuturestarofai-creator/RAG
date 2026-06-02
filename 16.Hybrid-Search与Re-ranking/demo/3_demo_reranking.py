"""
Demo 3: Re-ranking 重排序实现
============================

本 Demo 展示如何使用 sentence-transformers 的 CrossEncoder 实现重排序。
重排序是两阶段检索的第二阶段，对召回的候选文档进行精细排序。

学习目标：
1. 理解 Re-ranking 的原理和作用
2. 掌握 CrossEncoder 的使用方法
3. 对比 Bi-Encoder 和 CrossEncoder 的效果

依赖安装：
pip install sentence-transformers

注意：本 Demo 不需要 API Key（使用本地模型）
"""

from typing import List, Tuple, Dict
import json


# ============================================================
# 第一部分：Re-ranking 概念讲解
# ============================================================

def explain_reranking_concept():
    """
    讲解 Re-ranking 的核心概念
    """
    print("=" * 60)
    print("Re-ranking 概念讲解")
    print("=" * 60)

    print("""
Re-ranking（重排序）是两阶段检索的核心组件：

第一阶段：召回（Retrieval）
    - 目标：快速从海量文档中筛选候选集
    - 方法：BM25、向量检索、混合检索
    - 特点：速度快，召回率高，精度一般
    - 输出：Top-K 个候选文档（如 K=50）

第二阶段：重排（Re-ranking）
    - 目标：对候选集精细排序，提高精度
    - 方法：Cross-Encoder、专业 Rerank 模型
    - 特点：速度慢，精度高
    - 输出：Top-N 个最终文档（如 N=5）

类比：
    召回 = 海选（快速筛选简历）
    重排 = 复试（仔细评估候选人）
    """)


# ============================================================
# 第二部分：CrossEncoder 使用
# ============================================================

def demo_cross_encoder():
    """
    演示 CrossEncoder 的使用
    """
    print("\n" + "=" * 60)
    print("CrossEncoder 使用演示")
    print("=" * 60)

    try:
        from sentence_transformers import CrossEncoder
        print("sentence-transformers 库导入成功")
    except ImportError:
        print("错误：请安装 sentence-transformers 库")
        print("运行: pip install sentence-transformers")
        return

    # 加载 CrossEncoder 模型
    # 使用中文 Rerank 模型
    model_name = "BAAI/bge-reranker-base"
    print(f"\n加载模型: {model_name}")
    print("首次运行会下载模型，请稍候...")

    try:
        model = CrossEncoder(model_name, max_length=512)
        print("模型加载成功！")
    except Exception as e:
        print(f"模型加载失败: {e}")
        print("尝试使用备用模型...")
        try:
            # 备用模型
            model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", max_length=512)
            print("备用模型加载成功！")
        except Exception as e2:
            print(f"备用模型也加载失败: {e2}")
            print("请检查网络连接或手动下载模型")
            return

    return model


def rerank_demo(model):
    """
    使用 CrossEncoder 进行重排序演示

    参数：
        model: CrossEncoder 模型实例
    """
    print("\n" + "=" * 60)
    print("重排序演示")
    print("=" * 60)

    # 示例查询和文档
    query = "如何学习机器学习？"

    documents = [
        "机器学习入门教程：从零开始学习Python编程",
        "深度学习是机器学习的一个分支，需要先掌握基础",
        "今天天气真好，适合出去玩",
        "机器学习需要掌握线性代数和概率统计",
        "学习机器学习的步骤：1. 学Python 2. 学数学基础 3. 学算法",
        "我喜欢吃苹果和香蕉",
        "TensorFlow和PyTorch是常用的机器学习框架",
        "如何高效学习机器学习？建议从项目实践开始",
    ]

    print(f"\n查询: {query}")
    print(f"候选文档数量: {len(documents)}")

    # 构建 query-doc 对
    pairs = [[query, doc] for doc in documents]

    # 使用 CrossEncoder 计算相关性分数
    print("\n正在计算相关性分数...")
    scores = model.predict(pairs)

    # 按分数排序
    scored_docs = list(zip(documents, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    # 打印排序结果
    print("\n重排序结果:")
    for rank, (doc, score) in enumerate(scored_docs, 1):
        print(f"  {rank}. [分数: {score:.4f}] {doc}")


# ============================================================
# 第三部分：完整两阶段检索流程
# ============================================================

def two_stage_retrieval_demo(model):
    """
    完整的两阶段检索流程演示
    第一阶段：BM25 召回
    第二阶段：CrossEncoder 重排
    """
    print("\n" + "=" * 60)
    print("两阶段检索流程演示")
    print("=" * 60)

    try:
        import jieba
        from rank_bm25 import BM25Okapi
    except ImportError:
        print("错误：请安装 rank_bm25 和 jieba 库")
        print("运行: pip install rank_bm25 jieba")
        return

    # 文档库
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
        "卷积神经网络（CNN）常用于图像识别任务",
        "循环神经网络（RNN）适合处理序列数据",
        "强化学习通过与环境交互来学习最优策略",
    ]

    query = "深度学习框架推荐"

    print(f"\n查询: {query}")
    print(f"文档库大小: {len(documents)}")

    # 第一阶段：BM25 召回
    print("\n" + "-" * 40)
    print("第一阶段：BM25 召回")
    print("-" * 40)

    tokenized_docs = [list(jieba.cut(doc)) for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    tokenized_query = list(jieba.cut(query))
    bm25_scores = bm25.get_scores(tokenized_query)

    # 召回 Top-10
    recall_k = 10
    recalled_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:recall_k]
    recalled_docs = [documents[i] for i in recalled_indices]

    print(f"召回 Top-{recall_k} 文档:")
    for rank, idx in enumerate(recalled_indices, 1):
        print(f"  {rank}. [BM25: {bm25_scores[idx]:.4f}] {documents[idx][:40]}...")

    # 第二阶段：CrossEncoder 重排
    print("\n" + "-" * 40)
    print("第二阶段：CrossEncoder 重排")
    print("-" * 40)

    # 构建 query-doc 对
    pairs = [[query, doc] for doc in recalled_docs]

    # 计算相关性分数
    print("正在计算相关性分数...")
    rerank_scores = model.predict(pairs)

    # 按重排分数排序
    reranked_results = list(zip(recalled_indices, recalled_docs, rerank_scores))
    reranked_results.sort(key=lambda x: x[2], reverse=True)

    # 打印重排结果
    print(f"\n重排后 Top-5 结果:")
    for rank, (idx, doc, score) in enumerate(reranked_results[:5], 1):
        print(f"  {rank}. [Rerank: {score:.4f}] {doc[:50]}...")

    # 对比分析
    print("\n" + "-" * 40)
    print("对比分析")
    print("-" * 40)

    print("\nBM25 排名 vs Rerank 排名:")
    for i, (idx, doc, rerank_score) in enumerate(reranked_results[:5]):
        bm25_rank = recalled_indices.index(idx) + 1
        print(f"  文档: {doc[:30]}...")
        print(f"    BM25排名: {bm25_rank}, Rerank排名: {i+1}")


# ============================================================
# 第四部分：Reranking 效果分析
# ============================================================

def analyze_reranking_effect(model):
    """
    分析 Reranking 的效果
    """
    print("\n" + "=" * 60)
    print("Reranking 效果分析")
    print("=" * 60)

    # 设计测试案例：展示 Reranking 的优势
    test_cases = [
        {
            "query": "Python机器学习库",
            "documents": [
                "scikit-learn是Python最流行的机器学习库",  # 最相关
                "Python是一种编程语言",                    # 部分相关
                "机器学习需要大量数据",                    # 部分相关
                "Java也有机器学习库Weka",                  # 不太相关
            ],
            "expected_top1": 0  # 预期第一个文档排第一
        },
        {
            "query": "如何提高深度学习模型准确率",
            "documents": [
                "使用数据增强可以提高模型泛化能力",        # 最相关
                "深度学习需要GPU加速训练",                 # 相关但不直接
                "准确率是分类任务的常用指标",              # 相关但不直接
                "今天天气很好",                           # 不相关
            ],
            "expected_top1": 0
        }
    ]

    for case_idx, case in enumerate(test_cases, 1):
        print(f"\n测试案例 {case_idx}:")
        print(f"查询: {case['query']}")

        # 计算 Rerank 分数
        pairs = [[case['query'], doc] for doc in case['documents']]
        scores = model.predict(pairs)

        # 按分数排序
        scored_docs = list(zip(case['documents'], scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        print("Rerank 结果:")
        for rank, (doc, score) in enumerate(scored_docs, 1):
            marker = " ✓" if rank == 1 and case['documents'].index(doc) == case['expected_top1'] else ""
            print(f"  {rank}. [分数: {score:.4f}] {doc}{marker}")


# ============================================================
# 第五部分：Reranking 最佳实践
# ============================================================

def reranking_best_practices():
    """
    Reranking 最佳实践
    """
    print("\n" + "=" * 60)
    print("Reranking 最佳实践")
    print("=" * 60)

    print("""
1. 选择合适的模型
   - 中文场景：BAAI/bge-reranker-base 或 bge-reranker-large
   - 英文场景：cross-encoder/ms-marco-MiniLM-L-6-v2
   - 多语言：BAAI/bge-reranker-v2-m3

2. 合理设置召回数量
   - 召回 Top-K：通常 20-100
   - 重排 Top-N：通常 3-10
   - K 太小：可能漏掉好文档
   - K 太大：增加计算成本

3. 处理长文本
   - 设置合理的 max_length（如 512）
   - 对长文档做分段处理
   - 考虑使用支持长文本的模型

4. 性能优化
   - 批量处理：一次计算多个 query-doc 对
   - 缓存结果：相同 query-doc 对的分数可以缓存
   - 并行计算：多线程/多进程处理

5. 评估指标
   - MRR（Mean Reciprocal Rank）
   - NDCG（Normalized Discounted Cumulative Gain）
   - 人工评估
    """)


# ============================================================
# 第六部分：与 Cohere Rerank 对比
# ============================================================

def compare_with_cohere():
    """
    对比本地 CrossEncoder 和 Cohere Rerank API
    """
    print("\n" + "=" * 60)
    print("本地 CrossEncoder vs Cohere Rerank API")
    print("=" * 60)

    print("""
本地 CrossEncoder (sentence-transformers)
    优点：
        - 免费，无 API 费用
        - 无网络延迟
        - 数据隐私保护
        - 可自定义微调
    缺点：
        - 需要 GPU 加速
        - 模型下载占用空间
        - 效果可能不如商业 API

Cohere Rerank API
    优点：
        - 开箱即用，无需部署
        - 效果通常更好
        - 支持多语言
        - 持续更新优化
    缺点：
        - 需要 API 费用
        - 网络延迟
        - 数据隐私考虑

选择建议：
    - 预算有限 + 数据敏感 → 本地 CrossEncoder
    - 追求最佳效果 → Cohere Rerank
    - 快速原型验证 → Cohere Rerank
    - 生产环境大规模部署 → 本地 CrossEncoder
    """)


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("Re-ranking 重排序 Demo")
    print("=" * 60)

    # 讲解概念
    explain_reranking_concept()

    # 加载模型
    model = demo_cross_encoder()

    if model is not None:
        # 运行演示
        rerank_demo(model)
        two_stage_retrieval_demo(model)
        analyze_reranking_effect(model)

    # 最佳实践
    reranking_best_practices()
    compare_with_cohere()

    print("\n" + "=" * 60)
    print("Demo 完成！")
    print("=" * 60)
