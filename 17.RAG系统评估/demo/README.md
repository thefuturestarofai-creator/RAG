# 第17章：RAG系统评估 - Demo

## 学习顺序

建议按照以下顺序学习本章的 Demo：

### 1. Ragas 评估 (1_demo_ragas_evaluation.py)

**学习目标**：掌握 RAG 系统的定量评估方法

**内容**：
- Ragas 评估框架介绍
- 评估数据集构造方法
- 四大评估指标详解
- 评估结果解读和问题诊断

**是否需要 API Key**：是

**API Key 配置**：
```python
API_KEY = "your-api-key-here"
BASE_URL = "https://api.openai.com/v1"
MODEL = "gpt-3.5-turbo"
```

**运行方式**：
```bash
pip install ragas langchain langchain-openai datasets
python 1_demo_ragas_evaluation.py
```

**注意**：如果没有 API Key，代码会使用简化版评估演示，仍然可以学习评估概念。

---

### 2. 幻觉检测 (2_demo_hallucination_detection.py)

**学习目标**：实现 LLM 回答的幻觉检测

**内容**：
- 幻觉检测原理讲解
- 陈述分解方法
- 基于规则的检测实现
- 基于 LLM 的检测实现
- 综合检测流程

**是否需要 API Key**：是（用于 LLM 检测方法）

**运行方式**：
```bash
pip install openai
python 2_demo_hallucination_detection.py
```

**注意**：规则检测方法不需要 API Key，可以单独学习。

---

## 依赖安装

一键安装所有依赖：
```bash
pip install ragas langchain langchain-openai datasets openai
```

## 知识点对应关系

| Demo | 对应知识点 | 核心内容 |
|------|-----------|---------|
| 1_demo_ragas_evaluation.py | Ragas框架 | 评估流程、指标计算 |
| 2_demo_hallucination_detection.py | 幻觉应对策略 | 幻觉检测实现 |

## 学习建议

1. **先看理论文档**：在运行 Demo 前，先阅读对应的理论文档
2. **理解评估指标**：重点理解四大指标的含义和计算方式
3. **动手运行代码**：实际运行代码，观察输出结果
4. **分析评估结果**：学会从结果中发现问题和优化方向

## 常见问题

### Q1: Ragas 评估需要多少数据？

A: 建议至少 50-100 个样本，覆盖不同类型的问题。太少可能不具代表性，太多成本高。

### Q2: 评估结果不理想怎么办？

A: 按优先级排查：
1. Faithfulness 低 → 优化 Prompt 约束
2. Context Recall 低 → 优化检索
3. Context Precision 低 → 加 Re-ranking
4. Answer Relevancy 低 → 优化 Prompt

### Q3: 评估成本高吗？

A: 每个样本大约 3-5 次 LLM 调用。100 个样本用 GPT-3.5 大约 $1-2。可以用小模型降低成本。

### Q4: 规则检测和 LLM 检测怎么选？

A: 
- 规则检测：快速、免费，适合开发阶段
- LLM 检测：准确，适合正式评估
- 建议：开发用规则，上线前用 LLM

## 面试重点

1. **四大评估指标**：含义、计算方式、优化方向
2. **Ragas 框架**：使用流程、数据集构造、结果解读
3. **幻觉应对策略**：多种方法、组合使用
4. **评估最佳实践**：评估频率、数据集设计、持续优化
