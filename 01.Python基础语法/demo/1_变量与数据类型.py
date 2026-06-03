# ============================================================
# Demo 1: 变量与数据类型
# 对应理论文档: 1.变量与数据类型.md
# ============================================================
# 这个 Demo 演示 Python 的 6 大核心数据类型，
# 以及它们在 RAG 项目中的实际用法。
# 不需要 API Key。
# ============================================================

# ----- 1. 字符串 str -----
# RAG 项目中最常见的类型：用户提问、文档内容、LLM 回答

question = "什么是RAG？"
answer = "RAG是检索增强生成的缩写，它通过检索外部知识库来增强大模型的回答。"

# f-string 格式化（构造 Prompt 时天天用）
prompt = f"用户问：{question}\n请根据以下内容回答：{answer}"
print("=== Prompt 示例 ===")
print(prompt)
print()

# 常用字符串方法
text = "  Hello, RAG World!  "
print("strip():", text.strip())        # 去掉首尾空格
print("lower():", text.lower())        # 全部小写
print("split():", text.split(","))     # 按逗号分割
print("长度:", len(text))              # 字符串长度
print("包含 RAG:", "RAG" in text)      # 是否包含子串
print()

# ----- 2. 整数 int 和浮点数 float -----

chunk_size = 500             # 整数：Chunk 大小（Token 数）
similarity = 0.87            # 浮点数：相似度分数
temperature = 0.1            # 浮点数：模型创意度

print("=== 数字类型 ===")
print(f"Chunk 大小: {chunk_size} Token")
print(f"相似度分数: {similarity}")
print(f"Temperature: {temperature}")
print(f"10 / 3 = {10 / 3}")       # 除法 → 3.333...
print(f"10 // 3 = {10 // 3}")     # 整除 → 3
print(f"10 % 3 = {10 % 3}")       # 取余 → 1
print()

# ----- 3. 布尔 bool -----

is_relevant = True
has_error = False

print("=== 布尔类型 ===")
print(f"是否相关: {is_relevant}")
print(f"是否有错: {has_error}")
print(f"0.85 > 0.8 → {0.85 > 0.8}")       # True
print(f"True and False → {True and False}") # False
print(f"True or False → {True or False}")   # True
print()

# ----- 4. 列表 list -----
# RAG 核心数据结构：检索结果、对话历史、切分后的文本块

chunks = ["第一段文本内容", "第二段文本内容", "第三段文本内容", "第四段文本内容"]

print("=== 列表操作 ===")
print(f"所有块: {chunks}")
print(f"第一个: {chunks[0]}")        # 索引从 0 开始
print(f"最后一个: {chunks[-1]}")     # -1 表示倒数第一个
print(f"前两个: {chunks[0:2]}")      # 切片
print(f"块数量: {len(chunks)}")      # 长度

# 添加和删除
chunks.append("第五段文本内容")
print(f"添加后: {chunks}")
popped = chunks.pop()
print(f"取出最后一个: {popped}")
print(f"剩余: {chunks}")

# 遍历（RAG 中极其常用）
print("\n遍历所有块:")
for i, chunk in enumerate(chunks):
    print(f"  块 {i}: {chunk}")

# 列表推导式
scores = [0.95, 0.3, 0.87, 0.45, 0.72]
high_scores = [s for s in scores if s > 0.7]
print(f"\n高分结果 (>{0.7}): {high_scores}")
print()

# ----- 5. 字典 dict -----
# RAG 核心数据结构：API 响应 JSON、文档元数据

doc = {
    "content": "RAG是检索增强生成技术",
    "source": "knowledge_base.pdf",
    "page": 3,
    "score": 0.92
}

print("=== 字典操作 ===")
print(f"内容: {doc['content']}")
print(f"来源: {doc['source']}")
print(f"分数: {doc.get('score', 0)}")        # get 方法可以设默认值
print(f"标签: {doc.get('tag', '无标签')}")    # key 不存在时返回默认值

# 修改和添加
doc["score"] = 0.95
doc["chunk_id"] = "chunk_001"
print(f"更新后: {doc}")

# 遍历字典
print("\n遍历元数据:")
for key, value in doc.items():
    print(f"  {key}: {value}")
print()

# ----- 6. None 空值 -----

result = None
print("=== None 空值 ===")
print(f"result 的值: {result}")
print(f"是否为 None: {result is None}")

if result is None:
    print("还没获取到结果，需要调用 API")
print()

# ----- 7. 类型转换 -----

print("=== 类型转换 ===")
num_str = "42"
num = int(num_str)
print(f"字符串 '42' → 整数 {num}，类型: {type(num)}")

text = "hello,world,rag"
parts = text.split(",")
print(f"字符串分割 → 列表: {parts}")

joined = " | ".join(parts)
print(f"列表拼接 → 字符串: {joined}")
print()

# ----- 8. 综合示例：模拟 RAG 检索结果处理 -----
print("=" * 50)
print("综合示例：处理 RAG 检索结果")
print("=" * 50)

search_results = [
    {"content": "RAG通过检索外部知识来增强LLM回答", "score": 0.95, "source": "rag_intro.pdf"},
    {"content": "向量数据库用于存储Embedding向量", "score": 0.88, "source": "vector_db.pdf"},
    {"content": "今天天气真不错", "score": 0.23, "source": "random.txt"},
    {"content": "LangChain是大模型应用开发框架", "score": 0.91, "source": "langchain.pdf"},
    {"content": "Docker用于容器化部署", "score": 0.45, "source": "docker.pdf"},
]

# 筛选高分结果（条件判断 + 循环）
threshold = 0.7
relevant = [r for r in search_results if r["score"] > threshold]

print(f"\n阈值: {threshold}，找到 {len(relevant)} 条相关结果:")
for i, result in enumerate(relevant):
    print(f"  [{i+1}] (分数: {result['score']}) [{result['source']}] {result['content']}")

# 拼接成上下文（构造 Prompt 的输入）
context = "\n".join([r["content"] for r in relevant])
print(f"\n拼接后的上下文:\n{context}")
