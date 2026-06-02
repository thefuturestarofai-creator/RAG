"""
Demo 1: BM25 检索实现
=====================

本 Demo 展示如何使用 rank_bm25 库实现基于关键词的稀疏检索。
BM25 是一种经典的信息检索算法，基于词频和逆文档频率进行文档排序。

学习目标：
1. 理解 BM25 的工作原理
2. 掌握 rank_bm25 库的使用
3. 对比中文和英文的检索效果

依赖安装：
pip install rank_bm25 jieba

注意：本 Demo 不需要 API Key
"""

import math
from typing import List, Tuple
import jieba
from rank_bm25 import BM25Okapi


# ============================================================
# 第一部分：基础 BM25 使用
# ============================================================

def basic_bm25_demo():
    """
    基础 BM25 检索示例
    展示如何用 BM25 对文档进行关键词检索
    """
    print("=" * 60)
    print("基础 BM25 检索示例")
    print("=" * 60)

    # 示例文档集合
    documents = [
        "Python是一种广泛使用的高级编程语言",
        "机器学习是人工智能的一个子领域",
        "深度学习使用神经网络进行模式识别",
        "自然语言处理涉及文本分析和理解",
        "Python在数据科学和机器学习中很流行",
        "神经网络是深度学习的核心组件",
        "数据预处理是机器学习的重要步骤",
        "Transformer模型革新了自然语言处理",
        "BERT是一种预训练语言模型",
        "GPT系列模型展示了大语言模型的能力",
    ]

    # 对中文文档进行分词
    tokenized_docs = [list(jieba.cut(doc)) for doc in documents]

    # 创建 BM25 索引
    bm25 = BM25Okapi(tokenized_docs)

    # 测试查询
    queries = [
        "Python编程",
        "深度学习神经网络",
        "自然语言处理模型",
        "数据科学机器学习",
    ]

    for query in queries:
        print(f"\n查询: {query}")

        # 对查询进行分词
        tokenized_query = list(jieba.cut(query))

        # 获取 BM25 分数
        scores = bm25.get_scores(tokenized_query)

        # 按分数排序
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        # 打印 Top-3 结果
        print("Top-3 结果:")
        for rank, idx in enumerate(ranked_indices[:3], 1):
            print(f"  {rank}. [分数: {scores[idx]:.4f}] {documents[idx]}")


# ============================================================
# 第二部分：BM25 参数详解
# ============================================================

def bm25_parameters_demo():
    """
    BM25 参数详解
    展示 k1 和 b 参数对检索结果的影响
    """
    print("\n" + "=" * 60)
    print("BM25 参数详解")
    print("=" * 60)

    # 示例文档
    documents = [
        "机器学习 机器学习 机器学习 入门教程",  # 词频高
        "机器学习基础概念介绍",                   # 词频中
        "深度学习是机器学习的子领域，涉及神经网络",  # 词频低，但文档长
        "学习编程",                              # 词频低，文档短
    ]

    tokenized_docs = [list(jieba.cut(doc)) for doc in documents]

    # 不同参数配置
    configs = [
        {"k1": 1.5, "b": 0.75, "desc": "默认参数"},
        {"k1": 2.0, "b": 0.75, "desc": "高 k1（更重视词频）"},
        {"k1": 1.0, "b": 0.75, "desc": "低 k1（词频影响小）"},
        {"k1": 1.5, "b": 1.0, "desc": "高 b（更重视文档长度归一化）"},
        {"k1": 1.5, "b": 0.0, "desc": "低 b（不考虑文档长度）"},
    ]

    query = "机器学习"
    tokenized_query = list(jieba.cut(query))

    print(f"\n查询: {query}")
    print("-" * 60)

    for config in configs:
        bm25 = BM25Okapi(tokenized_docs, k1=config["k1"], b=config["b"])
        scores = bm25.get_scores(tokenized_query)

        print(f"\n{config['desc']} (k1={config['k1']}, b={config['b']}):")
        for i, (doc, score) in enumerate(zip(documents, scores)):
            print(f"  文档{i+1}: {score:.4f} - {doc[:20]}...")


# ============================================================
# 第三部分：BM25 的 TF-IDF 原理讲解
# ============================================================

def explain_bm25_scoring():
    """
    手动实现 BM25 评分，帮助理解原理
    """
    print("\n" + "=" * 60)
    print("BM25 评分原理讲解")
    print("=" * 60)

    # 示例
    documents = [
        "猫 喜欢 吃 鱼",
        "狗 喜欢 吃 骨头",
        "猫 和 狗 是 宠物",
    ]

    query = "猫 喜欢"

    # 手动计算 BM25 分数
    k1 = 1.5
    b = 0.75

    # 计算平均文档长度
    doc_lens = [len(doc.split()) for doc in documents]
    avgdl = sum(doc_lens) / len(doc_lens)
    N = len(documents)

    print(f"查询: {query}")
    print(f"文档数量: {N}")
    print(f"平均文档长度: {avgdl:.2f}")
    print("-" * 60)

    for query_term in query.split():
        print(f"\n查询词: '{query_term}'")

        # 计算 IDF
        # 包含该词的文档数
        doc_count = sum(1 for doc in documents if query_term in doc.split())
        idf = math.log((N - doc_count + 0.5) / (doc_count + 0.5) + 1)
        print(f"  包含该词的文档数: {doc_count}")
        print(f"  IDF = {idf:.4f}")

        for i, doc in enumerate(documents):
            terms = doc.split()
            tf = terms.count(query_term)
            doc_len = len(terms)

            # BM25 TF 公式
            tf_component = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avgdl))
            score = idf * tf_component

            print(f"  文档{i+1}: TF={tf}, 长度={doc_len}, TF分量={tf_component:.4f}, 得分={score:.4f}")


# ============================================================
# 第四部分：实际应用场景
# ============================================================

def practical_bm25_demo():
    """
    BM25 在实际场景中的应用
    模拟一个简单的 FAQ 检索系统
    """
    print("\n" + "=" * 60)
    print("实际应用：FAQ 检索系统")
    print("=" * 60)

    # FAQ 数据库
    faq_database = [
        {
            "question": "如何重置密码？",
            "answer": "点击登录页面的'忘记密码'链接，输入注册邮箱，系统会发送重置链接。"
        },
        {
            "question": "如何修改个人信息？",
            "answer": "登录后进入'个人中心'，点击'编辑资料'即可修改。"
        },
        {
            "question": "支持哪些支付方式？",
            "answer": "我们支持支付宝、微信支付、银行卡等多种支付方式。"
        },
        {
            "question": "如何申请退款？",
            "answer": "在订单详情页点击'申请退款'，填写退款原因，提交后等待审核。"
        },
        {
            "question": "配送时间是多久？",
            "answer": "普通配送3-5个工作日，加急配送1-2个工作日。"
        },
        {
            "question": "如何联系客服？",
            "answer": "可以通过在线客服、电话400-xxx-xxxx或邮件联系我们。"
        },
    ]

    # 提取问题列表
    questions = [faq["question"] for faq in faq_database]

    # 分词并建立索引
    tokenized_questions = [list(jieba.cut(q)) for q in questions]
    bm25 = BM25Okapi(tokenized_questions)

    # 测试查询
    test_queries = [
        "怎么改密码",
        "退款怎么操作",
        "发货要几天",
        "客服电话多少",
    ]

    for query in test_queries:
        print(f"\n用户问题: {query}")

        tokenized_query = list(jieba.cut(query))
        scores = bm25.get_scores(tokenized_query)

        # 找到最匹配的 FAQ
        best_idx = scores.argmax()
        best_score = scores[best_idx]

        print(f"最匹配的FAQ: {faq_database[best_idx]['question']}")
        print(f"匹配分数: {best_score:.4f}")
        print(f"回答: {faq_database[best_idx]['answer']}")

        # 显示所有分数
        print("所有FAQ的匹配分数:")
        for i, (faq, score) in enumerate(zip(faq_database, scores)):
            print(f"  {i+1}. [{score:.4f}] {faq['question']}")


# ============================================================
# 第五部分：BM25 与向量检索对比
# ============================================================

def compare_bm25_and_vector():
    """
    对比 BM25 和向量检索的特点
    这里只做概念性对比，实际向量检索需要 embedding 模型
    """
    print("\n" + "=" * 60)
    print("BM25 vs 向量检索 对比分析")
    print("=" * 60)

    # 展示 BM25 擅长的场景
    print("\n1. BM25 擅长的场景（精确匹配）:")
    examples_good = [
        ("查询: iPhone 15 Pro Max", "文档: Apple iPhone 15 Pro Max 256GB 评测", True),
        ("查询: Python 3.11 新特性", "文档: Python 3.11 版本更新日志", True),
        ("查询: ERROR 404", "文档: HTTP 状态码 404 Not Found 解释", True),
    ]
    for query, doc, good in examples_good:
        print(f"  {query}")
        print(f"  → {doc} ✓" if good else f"  → {doc} ✗")

    # 展示 BM25 不擅长的场景
    print("\n2. BM25 不擅长的场景（语义匹配）:")
    examples_bad = [
        ("查询: 电脑", "文档: 计算机选购指南", "BM25 可能匹配不到（关键词不同）"),
        ("查询: 怎么减肥", "文档: 健康饮食和运动计划", "BM25 可能匹配不到（没有'减肥'这个词）"),
        ("查询: 苹果", "文档: Apple 公司产品线", "BM25 无法区分水果和公司"),
    ]
    for query, doc, reason in examples_bad:
        print(f"  {query}")
        print(f"  → {doc}")
        print(f"    问题: {reason}")

    # 总结
    print("\n3. 总结:")
    print("  BM25: 适合精确匹配、专有名词、数字、缩写")
    print("  向量: 适合语义匹配、同义词、意图理解")
    print("  混合: 结合两者优势，覆盖更多场景")


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("BM25 检索 Demo")
    print("=" * 60)

    # 运行各个 Demo
    basic_bm25_demo()
    bm25_parameters_demo()
    explain_bm25_scoring()
    practical_bm25_demo()
    compare_bm25_and_vector()

    print("\n" + "=" * 60)
    print("Demo 完成！")
    print("=" * 60)
