# ============================================================
# Demo 2: 条件判断与循环
# 对应理论文档: 2.条件判断与循环.md
# ============================================================
# 这个 Demo 演示 if/elif/else 条件判断和 for/while 循环，
# 以及它们在 RAG 系统中的实际应用。
# 不需要 API Key。
# ============================================================

# ----- 1. 基本条件判断 -----
print("=" * 50)
print("1. 条件判断：根据相似度分数分类")
print("=" * 50)

scores = [0.95, 0.82, 0.55, 0.30, 0.71, 0.60]

for score in scores:
    if score > 0.8:
        label = "✅ 高度相关"
    elif score > 0.5:
        label = "⚠️ 一般相关"
    else:
        label = "❌ 不相关"
    print(f"  分数 {score:.2f} → {label}")

print()

# ----- 2. 多条件组合 -----
print("=" * 50)
print("2. 多条件组合：复合筛选")
print("=" * 50)

docs = [
    {"content": "RAG技术详解", "score": 0.92, "source": "manual.pdf"},
    {"content": "向量检索原理", "score": 0.88, "source": "manual.pdf"},
    {"content": "今天午餐吃什么", "score": 0.15, "source": "chat.txt"},
    {"content": "Docker部署指南", "score": 0.75, "source": "manual.pdf"},
    {"content": "LangChain快速入门", "score": 0.85, "source": "tutorial.md"},
]

# 筛选：来自 manual.pdf 且分数 > 0.8
print("\n来自 manual.pdf 且高度相关的结果:")
for doc in docs:
    if doc["source"] == "manual.pdf" and doc["score"] > 0.8:
        print(f"  ✅ [{doc['score']:.2f}] {doc['content']}")

# 筛选：分数 > 0.8 或来自 tutorial.md
print("\n高度相关 或 来自 tutorial.md 的结果:")
for doc in docs:
    if doc["score"] > 0.8 or doc["source"] == "tutorial.md":
        print(f"  ✅ [{doc['score']:.2f}] {doc['content']} (来源: {doc['source']})")

print()

# ----- 3. for 循环遍历 -----
print("=" * 50)
print("3. for 循环：遍历文档块")
print("=" * 50)

chunks = [
    "RAG（检索增强生成）是一种AI技术架构。",
    "它通过检索外部知识库来增强大语言模型的回答。",
    "核心流程：用户提问 → 检索相关文档 → 将文档作为上下文 → LLM生成回答。",
    "优势：减少幻觉、知识可更新、回答可溯源。",
]

# 基本遍历
print("\n遍历所有文档块:")
for i, chunk in enumerate(chunks):
    print(f"  [块 {i}] {chunk}")

# range() 按次数循环
print("\n模拟重试机制 (最多3次):")
for attempt in range(3):
    print(f"  第 {attempt + 1} 次尝试调用 API...")

print()

# ----- 4. while 循环 -----
print("=" * 50)
print("4. while 循环：重试机制")
print("=" * 50)

import random
random.seed(42)  # 固定随机种子，保证输出可复现

retry_count = 0
max_retries = 5
success = False

while retry_count < max_retries and not success:
    retry_count += 1
    # 模拟 API 调用（随机成功/失败）
    call_success = random.random() > 0.6  # 60% 概率失败
    if call_success:
        success = True
        print(f"  第 {retry_count} 次尝试: ✅ 成功!")
    else:
        print(f"  第 {retry_count} 次尝试: ❌ 失败，重试中...")

if not success:
    print(f"  {max_retries} 次尝试后仍未成功，放弃")

print()

# ----- 5. break 和 continue -----
print("=" * 50)
print("5. break 和 continue：流程控制")
print("=" * 50)

scores = [0.3, 0.45, 0.52, 0.88, 0.91, 0.76]

# break: 找到第一个高分就停
print("\nbreak - 找到第一个 > 0.8 的结果就停止:")
for score in scores:
    if score > 0.8:
        print(f"  找到! 分数: {score}")
        break
    print(f"  跳过: {score}")

# continue: 跳过低分
print("\ncontinue - 只处理 > 0.5 的结果:")
for score in scores:
    if score <= 0.5:
        continue
    print(f"  处理: {score}")

print()

# ----- 6. 列表推导式 -----
print("=" * 50)
print("6. 列表推导式：简洁高效的数据处理")
print("=" * 50)

# 基本推导式
scores = [0.9, 0.3, 0.8, 0.4, 0.95, 0.6]
high_scores = [s for s in scores if s > 0.7]
print(f"所有分数: {scores}")
print(f"高分 (>{0.7}): {high_scores}")

# 带变换的推导式
texts = ["Hello World", "RAG is Great", "Python Basics"]
lowered = [t.lower() for t in texts]
print(f"原文: {texts}")
print(f"小写: {lowered}")

# 从字典列表中提取字段
results = [
    {"content": "文档A", "score": 0.9},
    {"content": "文档B", "score": 0.3},
    {"content": "文档C", "score": 0.8},
]
relevant_contents = [r["content"] for r in results if r["score"] > 0.5]
print(f"相关文档内容: {relevant_contents}")

print()

# ----- 7. 综合示例：RAG 检索结果处理管道 -----
print("=" * 50)
print("综合示例：完整的检索结果处理管道")
print("=" * 50)

search_results = [
    {"content": "RAG通过检索外部知识来增强LLM回答", "score": 0.95, "source": "rag_intro.pdf", "page": 1},
    {"content": "向量数据库用于存储Embedding向量", "score": 0.88, "source": "vector_db.pdf", "page": 3},
    {"content": "今天天气真不错适合出门", "score": 0.12, "source": "random.txt", "page": 1},
    {"content": "LangChain是大模型应用开发框架", "score": 0.91, "source": "langchain.pdf", "page": 5},
    {"content": "Docker用于容器化部署应用", "score": 0.45, "source": "docker.pdf", "page": 2},
    {"content": "Embedding将文本转换为向量表示", "score": 0.86, "source": "vector_db.pdf", "page": 1},
    {"content": "FastAPI是高性能Python Web框架", "score": 0.79, "source": "fastapi.pdf", "page": 4},
]

# 第1步：按分数筛选（阈值过滤）
threshold = 0.7
filtered = [r for r in search_results if r["score"] > threshold]
print(f"\n[第1步] 阈值过滤 (>{threshold}): {len(search_results)} → {len(filtered)} 条")

# 第2步：按分数排序（从高到低）
sorted_results = sorted(filtered, key=lambda r: r["score"], reverse=True)
print(f"[第2步] 按分数降序排列:")
for r in sorted_results:
    print(f"    [{r['score']:.2f}] {r['content']}")

# 第3步：格式化为上下文（模拟构造 Prompt）
context_parts = []
for r in sorted_results:
    context_parts.append(f"[来源: {r['source']} 第{r['page']}页] {r['content']}")

context = "\n".join(context_parts)
print(f"\n[第3步] 拼接上下文:")
print(context)

# 第4步：构造最终 Prompt
user_question = "什么是RAG？它有什么优势？"
final_prompt = f"""请根据以下参考资料回答用户问题。
如果参考资料中没有相关信息，请回答"根据现有资料无法回答"。

参考资料：
{context}

用户问题：{user_question}"""

print(f"\n[第4步] 最终 Prompt:")
print(final_prompt)
