"""
Demo 1: Ragas 评估 - RAG 系统定量评估
====================================

本 Demo 展示如何使用 Ragas 框架对 RAG 系统进行定量评估。
包括评估数据集构造、评估运行和结果解读。

学习目标：
1. 理解 Ragas 评估流程
2. 掌握评估数据集构造方法
3. 学会解读评估结果

依赖安装：
pip install ragas langchain langchain-openai datasets

注意：本 Demo 需要 API Key（用于 LLM 评估）
"""

import json
from typing import List, Dict

# ============================================================
# API 配置
# ============================================================
# 请替换为你的 API Key
API_KEY = "your-api-key-here"
BASE_URL = "https://api.openai.com/v1"  # 或你的 API 地址
MODEL = "gpt-3.5-turbo"  # 用于评估的模型


# ============================================================
# 第一部分：Ragas 评估概念讲解
# ============================================================

def explain_ragas_concept():
    """
    讲解 Ragas 评估的核心概念
    """
    print("=" * 60)
    print("Ragas 评估概念讲解")
    print("=" * 60)

    print("""
Ragas (Retrieval Augmented Generation Assessment) 是一个专门用于评估 RAG 系统的框架。

核心评估指标：
    1. Faithfulness（忠实度）：回答是否基于检索到的上下文
    2. Answer Relevancy（答案相关性）：回答是否切题
    3. Context Precision（上下文精确率）：检索到的文档是否相关
    4. Context Recall（上下文召回率）：是否找全相关文档

评估流程：
    1. 准备评估数据集（question, answer, contexts, ground_truth）
    2. 配置 LLM（用于评估的模型）
    3. 运行 evaluate() 函数
    4. 解读评估结果

评估数据集格式：
    {
        "question": "用户问题",
        "answer": "LLM 生成的回答",
        "contexts": ["检索到的文档1", "检索到的文档2"],
        "ground_truth": "标准答案（可选）"
    }
    """)


# ============================================================
# 第二部分：评估数据集构造
# ============================================================

def create_evaluation_dataset():
    """
    构造评估数据集
    模拟一个简单的 RAG 系统的输入输出
    """
    print("\n" + "=" * 60)
    print("构造评估数据集")
    print("=" * 60)

    # 模拟 RAG 系统的输入输出
    evaluation_data = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": [],
    }

    # 示例 1：忠实的回答
    evaluation_data["question"].append("什么是机器学习？")
    evaluation_data["answer"].append(
        "机器学习是人工智能的一个子领域，它使计算机能够从数据中学习，"
        "而不需要显式编程。机器学习算法通过训练数据来识别模式，"
        "并做出预测或决策。"
    )
    evaluation_data["contexts"].append([
        "机器学习是人工智能的一个子领域，它使计算机能够从数据中学习。",
        "机器学习算法通过训练数据来识别模式，并做出预测或决策。",
        "机器学习不需要显式编程，而是通过数据驱动的方式学习。"
    ])
    evaluation_data["ground_truth"].append(
        "机器学习是人工智能的子领域，让计算机从数据中学习并做出预测。"
    )

    # 示例 2：有幻觉的回答
    evaluation_data["question"].append("Python 是谁创建的？")
    evaluation_data["answer"].append(
        "Python 由 Guido van Rossum 于 1991 年创建。"
        "他是荷兰程序员，被称为 Python 之父。"
    )
    evaluation_data["contexts"].append([
        "Python 由 Guido van Rossum 创建。",
        "Python 是一种高级编程语言。",
        "Python 的设计哲学强调代码可读性。"
    ])
    evaluation_data["ground_truth"].append(
        "Python 由 Guido van Rossum 创建。"
    )

    # 示例 3：不相关的回答
    evaluation_data["question"].append("深度学习的应用有哪些？")
    evaluation_data["answer"].append(
        "Python 是一种流行的编程语言，广泛用于 Web 开发、"
        "数据科学和自动化脚本。"
    )
    evaluation_data["contexts"].append([
        "深度学习在图像识别领域有广泛应用。",
        "自然语言处理也大量使用深度学习技术。",
        "自动驾驶汽车使用深度学习进行环境感知。"
    ])
    evaluation_data["ground_truth"].append(
        "深度学习应用于图像识别、自然语言处理、自动驾驶等领域。"
    )

    # 示例 4：检索不完整
    evaluation_data["question"].append("RAG 系统的优势是什么？")
    evaluation_data["answer"].append(
        "RAG 系统的主要优势是能够减少幻觉，"
        "因为它基于检索到的文档生成回答。"
    )
    evaluation_data["contexts"].append([
        "RAG 系统可以减少 LLM 的幻觉问题。",
        "RAG 系统能够访问最新的信息。",
    ])
    evaluation_data["ground_truth"].append(
        "RAG 系统的优势包括：1. 减少幻觉 2. 访问最新信息 "
        "3. 可追溯来源 4. 知识可更新 5. 成本效益高"
    )

    print(f"评估数据集构造完成，共 {len(evaluation_data['question'])} 个样本")

    # 显示数据集
    for i in range(len(evaluation_data["question"])):
        print(f"\n样本 {i+1}:")
        print(f"  问题: {evaluation_data['question'][i]}")
        print(f"  回答: {evaluation_data['answer'][i][:50]}...")
        print(f"  上下文数量: {len(evaluation_data['contexts'][i])}")

    return evaluation_data


# ============================================================
# 第三部分：Ragas 评估实现
# ============================================================

def run_ragas_evaluation(evaluation_data):
    """
    使用 Ragas 框架运行评估

    参数：
        evaluation_data: 评估数据集
    """
    print("\n" + "=" * 60)
    print("运行 Ragas 评估")
    print("=" * 60)

    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import (
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        )
        print("Ragas 库导入成功")
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请安装依赖: pip install ragas datasets")
        print("\n将使用简化版评估演示...")
        run_simplified_evaluation(evaluation_data)
        return

    try:
        from langchain_openai import ChatOpenAI

        # 配置 LLM
        llm = ChatOpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
            model=MODEL,
            temperature=0,
        )
        print(f"LLM 配置完成: {MODEL}")
    except Exception as e:
        print(f"LLM 配置失败: {e}")
        print("将使用简化版评估演示...")
        run_simplified_evaluation(evaluation_data)
        return

    # 创建 Dataset
    dataset = Dataset.from_dict(evaluation_data)
    print("数据集创建成功")

    # 运行评估
    print("\n正在运行评估，请稍候...")
    try:
        result = evaluate(
            dataset=dataset,
            metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
            llm=llm,
        )

        # 打印结果
        print("\n评估结果:")
        print("-" * 40)
        print(f"Faithfulness: {result['faithfulness']:.4f}")
        print(f"Answer Relevancy: {result['answer_relevancy']:.4f}")
        print(f"Context Precision: {result['context_precision']:.4f}")
        print(f"Context Recall: {result['context_recall']:.4f}")

        # 详细结果
        print("\n详细结果:")
        for i, scores in enumerate(result.scores):
            print(f"\n样本 {i+1}:")
            print(f"  问题: {evaluation_data['question'][i]}")
            print(f"  Faithfulness: {scores['faithfulness']:.4f}")
            print(f"  Answer Relevancy: {scores['answer_relevancy']:.4f}")

        return result

    except Exception as e:
        print(f"评估失败: {e}")
        print("可能原因：API Key 无效或网络问题")
        print("将使用简化版评估演示...")
        run_simplified_evaluation(evaluation_data)
        return None


# ============================================================
# 第四部分：简化版评估（不需要 API）
# ============================================================

def run_simplified_evaluation(evaluation_data):
    """
    简化版评估，不需要 API
    使用规则和简单计算来演示评估概念
    """
    print("\n" + "=" * 60)
    print("简化版评估演示（不需要 API）")
    print("=" * 60)

    print("\n以下使用简化方法演示评估概念：")

    for i in range(len(evaluation_data["question"])):
        question = evaluation_data["question"][i]
        answer = evaluation_data["answer"][i]
        contexts = evaluation_data["contexts"][i]
        ground_truth = evaluation_data["ground_truth"][i]

        print(f"\n样本 {i+1}:")
        print(f"  问题: {question}")

        # 简化版 Faithfulness 计算
        # 检查回答中的关键句是否在上下文中出现
        answer_sentences = answer.split("。")
        context_text = " ".join(contexts)

        supported_count = 0
        for sentence in answer_sentences:
            if sentence.strip() and any(word in context_text for word in sentence.split()[:3]):
                supported_count += 1

        faithfulness_score = supported_count / max(len(answer_sentences), 1)

        # 简化版 Answer Relevancy 计算
        # 检查回答和问题的关键词重叠
        question_words = set(question.split())
        answer_words = set(answer.split())
        overlap = len(question_words & answer_words)
        relevancy_score = overlap / max(len(question_words), 1)

        # 简化版 Context Precision 计算
        # 检查上下文与问题的相关性
        relevant_count = 0
        for context in contexts:
            if any(word in context for word in question.split()):
                relevant_count += 1
        precision_score = relevant_count / max(len(contexts), 1)

        print(f"  Faithfulness (简化): {faithfulness_score:.2f}")
        print(f"  Answer Relevancy (简化): {relevancy_score:.2f}")
        print(f"  Context Precision (简化): {precision_score:.2f}")

        # 分析
        if faithfulness_score < 0.5:
            print(f"  ⚠️ 警告：Faithfulness 较低，可能存在幻觉")
        if relevancy_score < 0.3:
            print(f"  ⚠️ 警告：Answer Relevancy 较低，回答可能不切题")


# ============================================================
# 第五部分：结果解读指南
# ============================================================

def explain_results_interpretation():
    """
    讲解如何解读评估结果
    """
    print("\n" + "=" * 60)
    print("结果解读指南")
    print("=" * 60)

    print("""
评估结果分数范围：0-1

分数等级：
    0.8+  ：优秀 ✓
    0.6-0.8：良好
    0.4-0.6：一般
    0.4 以下：需要优化 ✗

常见问题诊断：

1. Faithfulness 低
   原因：LLM 幻觉严重
   优化：
   - Prompt 约束："只基于上下文回答"
   - Temperature 设为 0
   - 后处理验证

2. Answer Relevancy 低
   原因：回答跑题
   优化：
   - 优化 Prompt，明确问题
   - 限制回答长度
   - 使用 CoT（思维链）

3. Context Precision 低
   原因：检索到不相关文档
   优化：
   - 使用 Re-ranking
   - 提高相似度阈值
   - 优化 embedding 模型

4. Context Recall 低
   原因：遗漏相关文档
   优化：
   - 增加 Top-K
   - 使用混合检索
   - Query 改写和扩展
    """)


# ============================================================
# 第六部分：评估最佳实践
# ============================================================

def evaluation_best_practices():
    """
    评估最佳实践
    """
    print("\n" + "=" * 60)
    print("评估最佳实践")
    print("=" * 60)

    print("""
1. 评估数据集设计
   - 样本数量：至少 50-100 个
   - 数据多样性：覆盖不同类型问题
   - 标注质量：人工审核标准答案

2. 评估频率
   - 开发阶段：每次改动都评估
   - 上线前：完整评估
   - 生产环境：定期抽样评估

3. 评估指标选择
   - 重点关注 Faithfulness（核心价值）
   - 根据业务场景调整优先级
   - 综合看多个指标

4. 结果分析
   - 找出低分样本，分析原因
   - 分类统计，找出系统性问题
   - 对比不同配置的效果

5. 持续优化
   - 评估 → 分析 → 优化 → 再评估
   - 记录每次优化的效果
   - 建立评估基线，跟踪改进
    """)


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("Ragas 评估 Demo")
    print("=" * 60)

    # 讲解概念
    explain_ragas_concept()

    # 构造评估数据集
    evaluation_data = create_evaluation_dataset()

    # 运行评估
    result = run_ragas_evaluation(evaluation_data)

    # 结果解读
    explain_results_interpretation()

    # 最佳实践
    evaluation_best_practices()

    print("\n" + "=" * 60)
    print("Demo 完成！")
    print("=" * 60)
