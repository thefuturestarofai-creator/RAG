"""
Demo 2: 幻觉检测 - 检测 LLM 回答中的幻觉
==========================================

本 Demo 展示如何实现简单的幻觉检测逻辑，对比 LLM 回答和检索上下文的一致性。

学习目标：
1. 理解幻觉检测的原理
2. 实现基于规则的幻觉检测
3. 实现基于 LLM 的幻觉检测

依赖安装：
pip install openai

注意：本 Demo 需要 API Key（用于 LLM 评估）
"""

import json
import re
from typing import List, Dict, Tuple

# ============================================================
# API 配置
# ============================================================
# 请替换为你的 API Key
API_KEY = "your-api-key-here"
BASE_URL = "https://api.openai.com/v1"  # 或你的 API 地址
MODEL = "gpt-3.5-turbo"


# ============================================================
# 第一部分：幻觉检测概念讲解
# ============================================================

def explain_hallucination_detection():
    """
    讲解幻觉检测的核心概念
    """
    print("=" * 60)
    print("幻觉检测概念讲解")
    print("=" * 60)

    print("""
幻觉检测的目标：判断 LLM 的回答是否基于检索到的上下文。

两种检测方法：

1. 基于规则的检测（Rule-based）
   - 原理：检查回答中的关键词是否在上下文中出现
   - 优点：快速、不需要 API
   - 缺点：精度低，无法理解语义

2. 基于 LLM 的检测（LLM-based）
   - 原理：用 LLM 判断回答是否有上下文支持
   - 优点：精度高，能理解语义
   - 缺点：需要 API，有成本

检测流程：
    1. 将回答分解成多个陈述（statements）
    2. 对每个陈述，检查是否有上下文支持
    3. 计算有支持的陈述比例 = Faithfulness
    """)


# ============================================================
# 第二部分：陈述分解
# ============================================================

def decompose_statements(answer: str) -> List[str]:
    """
    将回答分解成多个独立陈述

    参数：
        answer: LLM 的回答

    返回：
        陈述列表
    """
    # 方法1：按句号分割
    statements = re.split(r'[。！？]', answer)
    statements = [s.strip() for s in statements if s.strip()]

    # 方法2：按逗号分割（更细粒度）
    # statements = re.split(r'[，。！？,]', answer)
    # statements = [s.strip() for s in statements if s.strip()]

    return statements


# ============================================================
# 第三部分：基于规则的幻觉检测
# ============================================================

def rule_based_hallucination_check(
    statements: List[str],
    contexts: List[str]
) -> List[Dict]:
    """
    基于规则的幻觉检测

    原理：检查陈述中的关键词是否在上下文中出现

    参数：
        statements: 陈述列表
        contexts: 上下文列表

    返回：
        检测结果列表
    """
    results = []
    context_text = " ".join(contexts).lower()

    for statement in statements:
        # 提取陈述中的关键词（简单方法：分词后取名词动词）
        words = set(statement.lower().split())

        # 检查关键词是否在上下文中出现
        matched_words = [w for w in words if w in context_text]
        coverage = len(matched_words) / max(len(words), 1)

        # 判断是否支持
        is_supported = coverage >= 0.3  # 阈值可调

        results.append({
            "statement": statement,
            "is_supported": is_supported,
            "coverage": coverage,
            "matched_words": matched_words,
            "method": "rule_based",
        })

    return results


# ============================================================
# 第四部分：基于 LLM 的幻觉检测
# ============================================================

def llm_based_hallucination_check(
    statements: List[str],
    contexts: List[str]
) -> List[Dict]:
    """
    基于 LLM 的幻觉检测

    原理：用 LLM 判断陈述是否有上下文支持

    参数：
        statements: 陈述列表
        contexts: 上下文列表

    返回：
        检测结果列表
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        print("OpenAI 客户端初始化成功")
    except ImportError:
        print("错误：请安装 openai 库")
        print("运行: pip install openai")
        return []
    except Exception as e:
        print(f"初始化失败: {e}")
        return []

    results = []
    context_text = "\n".join(contexts)

    for statement in statements:
        prompt = f"""请判断以下陈述是否有提供的上下文支持。

上下文：
{context_text}

陈述：{statement}

判断标准：
1. 陈述中的每个事实是否有上下文支持
2. 是否有编造或推测的内容
3. 数字、日期、名称是否准确

请只回答"支持"或"不支持"，然后简要说明原因。

格式：
判断：支持/不支持
原因：xxx"""

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=200,
            )

            result_text = response.choices[0].message.content

            # 解析结果
            is_supported = "支持" in result_text and "不支持" not in result_text

            results.append({
                "statement": statement,
                "is_supported": is_supported,
                "reason": result_text,
                "method": "llm_based",
            })

        except Exception as e:
            print(f"LLM 调用失败: {e}")
            results.append({
                "statement": statement,
                "is_supported": None,
                "reason": f"检测失败: {e}",
                "method": "llm_based",
            })

    return results


# ============================================================
# 第五部分：综合幻觉检测
# ============================================================

def comprehensive_hallucination_detection(
    answer: str,
    contexts: List[str]
) -> Dict:
    """
    综合幻觉检测

    结合规则和 LLM 两种方法

    参数：
        answer: LLM 的回答
        contexts: 上下文列表

    返回：
        综合检测结果
    """
    print("\n" + "=" * 60)
    print("综合幻觉检测")
    print("=" * 60)

    # 1. 分解陈述
    statements = decompose_statements(answer)
    print(f"\n陈述分解：共 {len(statements)} 个陈述")
    for i, stmt in enumerate(statements, 1):
        print(f"  {i}. {stmt}")

    # 2. 基于规则的检测
    print("\n基于规则的检测:")
    rule_results = rule_based_hallucination_check(statements, contexts)

    for result in rule_results:
        status = "✓ 支持" if result["is_supported"] else "✗ 不支持"
        print(f"  {status} [覆盖率: {result['coverage']:.2f}] {result['statement'][:30]}...")

    # 3. 基于 LLM 的检测
    print("\n基于 LLM 的检测:")
    llm_results = llm_based_hallucination_check(statements, contexts)

    for result in llm_results:
        if result["is_supported"] is not None:
            status = "✓ 支持" if result["is_supported"] else "✗ 不支持"
            print(f"  {status} {result['statement'][:30]}...")
        else:
            print(f"  ? 检测失败 {result['statement'][:30]}...")

    # 4. 综合判断
    supported_count = sum(1 for r in rule_results if r["is_supported"])
    faithfulness = supported_count / max(len(statements), 1)

    print(f"\n综合结果:")
    print(f"  总陈述数: {len(statements)}")
    print(f"  支持陈述数: {supported_count}")
    print(f"  Faithfulness: {faithfulness:.2f}")

    if faithfulness >= 0.8:
        print(f"  评估: 优秀 ✓")
    elif faithfulness >= 0.6:
        print(f"  评估: 良好")
    elif faithfulness >= 0.4:
        print(f"  评估: 一般")
    else:
        print(f"  评估: 需要优化 ✗")

    return {
        "statements": statements,
        "rule_results": rule_results,
        "llm_results": llm_results,
        "faithfulness": faithfulness,
    }


# ============================================================
# 第六部分：演示案例
# ============================================================

def demo_cases():
    """
    演示不同类型的幻觉案例
    """
    print("\n" + "=" * 60)
    print("幻觉检测演示案例")
    print("=" * 60)

    # 案例 1：忠实回答
    print("\n案例 1：忠实回答")
    print("-" * 40)

    answer1 = "Python 是一种高级编程语言。它由 Guido van Rossum 创建。Python 广泛用于数据科学和 Web 开发。"
    contexts1 = [
        "Python 是一种高级编程语言，由 Guido van Rossum 创建。",
        "Python 广泛用于数据科学、Web 开发和自动化脚本。",
    ]

    print(f"回答: {answer1}")
    print(f"上下文: {contexts1}")

    # 简化检测
    statements1 = decompose_statements(answer1)
    results1 = rule_based_hallucination_check(statements1, contexts1)
    supported1 = sum(1 for r in results1 if r["is_supported"])
    print(f"Faithfulness: {supported1}/{len(statements1)} = {supported1/len(statements1):.2f}")

    # 案例 2：有幻觉
    print("\n案例 2：有幻觉（编造年份）")
    print("-" * 40)

    answer2 = "Python 由 Guido van Rossum 于 1991 年创建。Python 的最新版本是 4.0。"
    contexts2 = [
        "Python 由 Guido van Rossum 创建。",
        "Python 是一种高级编程语言。",
    ]

    print(f"回答: {answer2}")
    print(f"上下文: {contexts2}")

    statements2 = decompose_statements(answer2)
    results2 = rule_based_hallucination_check(statements2, contexts2)
    supported2 = sum(1 for r in results2 if r["is_supported"])
    print(f"Faithfulness: {supported2}/{len(statements2)} = {supported2/len(statements2):.2f}")
    print("注意：年份和版本号是编造的")

    # 案例 3：完全跑题
    print("\n案例 3：完全跑题")
    print("-" * 40)

    answer3 = "今天天气很好，适合出去玩。我最喜欢的运动是篮球。"
    contexts3 = [
        "Python 是一种高级编程语言。",
        "机器学习是人工智能的子领域。",
    ]

    print(f"回答: {answer3}")
    print(f"上下文: {contexts3}")

    statements3 = decompose_statements(answer3)
    results3 = rule_based_hallucination_check(statements3, contexts3)
    supported3 = sum(1 for r in results3 if r["is_supported"])
    print(f"Faithfulness: {supported3}/{len(statements3)} = {supported3/len(statements3):.2f}")


# ============================================================
# 第七部分：幻觉检测最佳实践
# ============================================================

def hallucination_detection_best_practices():
    """
    幻觉检测最佳实践
    """
    print("\n" + "=" * 60)
    print("幻觉检测最佳实践")
    print("=" * 60)

    print("""
1. 检测方法选择
   - 开发阶段：规则方法快速迭代
   - 上线前：LLM 方法精确评估
   - 生产环境：两者结合，规则过滤 + LLM 验证

2. 陈述分解策略
   - 按句号分割：简单，粒度适中
   - 按逗号分割：更细粒度，检测更精确
   - 语义分割：用 LLM 分解，最准确

3. 阈值设置
   - Faithfulness >= 0.8：优秀
   - Faithfulness >= 0.6：可接受
   - Faithfulness < 0.6：需要优化

4. 优化方向
   - 如果 Faithfulness 低，优化 Prompt
   - 如果特定类型幻觉多，针对性约束
   - 持续监控，建立反馈循环

5. 成本控制
   - 批量处理，减少 API 调用
   - 缓存检测结果
   - 使用小模型做初步筛选
    """)


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("幻觉检测 Demo")
    print("=" * 60)

    # 讲解概念
    explain_hallucination_detection()

    # 演示案例
    demo_cases()

    # 综合检测
    answer = "机器学习是人工智能的一个子领域。它使计算机能够从数据中学习。深度学习需要大量计算资源。"
    contexts = [
        "机器学习是人工智能的一个子领域。",
        "机器学习使计算机能够从数据中学习。",
        "深度学习是机器学习的一个分支。",
    ]
    comprehensive_hallucination_detection(answer, contexts)

    # 最佳实践
    hallucination_detection_best_practices()

    print("\n" + "=" * 60)
    print("Demo 完成！")
    print("=" * 60)
