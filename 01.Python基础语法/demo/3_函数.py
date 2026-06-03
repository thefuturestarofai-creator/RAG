# ============================================================
# Demo 3: 函数
# 对应理论文档: 3.函数.md
# ============================================================
# 这个 Demo 演示 Python 函数的各种用法，
# 以及如何用函数组织 RAG 系统的代码结构。
# 不需要 API Key。
# ============================================================

# ----- 1. 基本函数 -----
print("=" * 50)
print("1. 基本函数定义和调用")
print("=" * 50)

def greet(name):
    """向某人打招呼"""
    print(f"  你好，{name}！欢迎学习 RAG！")

greet("学习者")
greet("未来的AI工程师")
print()

# ----- 2. 带返回值的函数 -----
print("=" * 50)
print("2. 带返回值的函数")
print("=" * 50)

def split_text(text, chunk_size=50):
    """把文本按指定大小切分（模拟 Chunking）"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

# 使用函数
long_text = "RAG（检索增强生成）是一种AI技术架构。它通过检索外部知识库来增强大语言模型的回答能力。核心流程包括：用户提问、检索相关文档、将文档作为上下文、LLM生成回答。这种技术可以有效减少大模型的幻觉问题。"
chunks = split_text(long_text, chunk_size=30)

print(f"原文长度: {len(long_text)} 字符")
print(f"切分成 {len(chunks)} 个块:")
for i, chunk in enumerate(chunks):
    print(f"  [块{i}] ({len(chunk)}字) {chunk}")
print()

# ----- 3. 返回多个值 -----
print("=" * 50)
print("3. 返回多个值")
print("=" * 50)

def analyze_chunks(chunks):
    """分析文本块的统计信息"""
    total_chars = sum(len(c) for c in chunks)
    avg_length = total_chars / len(chunks) if chunks else 0
    max_length = max(len(c) for c in chunks) if chunks else 0
    min_length = min(len(c) for c in chunks) if chunks else 0
    return total_chars, avg_length, max_length, min_length

total, avg, max_len, min_len = analyze_chunks(chunks)
print(f"总字符数: {total}")
print(f"平均长度: {avg:.1f}")
print(f"最长: {max_len}")
print(f"最短: {min_len}")
print()

# ----- 4. 默认参数和关键字参数 -----
print("=" * 50)
print("4. 默认参数和关键字参数")
print("=" * 50)

def search(query, top_k=3, threshold=0.5, source_filter=None):
    """模拟搜索函数（带默认参数）"""
    print(f"  查询: '{query}'")
    print(f"  返回数量: {top_k}, 阈值: {threshold}")
    if source_filter:
        print(f"  来源过滤: {source_filter}")
    else:
        print(f"  来源过滤: 无")
    return [f"结果{i+1}" for i in range(top_k)]

# 不同调用方式
print("调用1 - 全部用默认值:")
search("什么是RAG")

print("\n调用2 - 指定部分参数:")
search("什么是RAG", top_k=5)

print("\n调用3 - 关键字参数（顺序随意）:")
search("什么是RAG", source_filter="manual.pdf", threshold=0.8)
print()

# ----- 5. 函数作为参数（高阶函数） -----
print("=" * 50)
print("5. 函数作为参数（高阶函数）")
print("=" * 50)

def apply_to_chunks(chunks, transform_func):
    """对每个文本块应用一个变换函数"""
    return [transform_func(chunk) for chunk in chunks]

def add_prefix(text):
    return f"[文档片段] {text}"

def to_lowercase(text):
    return text.lower()

def count_chars(text):
    return f"({len(text)}字) {text}"

sample_chunks = ["RAG是检索增强生成", "向量数据库存储Embedding", "LangChain是框架"]

print("原始块:")
for c in sample_chunks:
    print(f"  {c}")

print("\n添加前缀:")
result = apply_to_chunks(sample_chunks, add_prefix)
for c in result:
    print(f"  {c}")

print("\n转小写:")
result = apply_to_chunks(sample_chunks, to_lowercase)
for c in result:
    print(f"  {c}")

print("\n添加字数统计:")
result = apply_to_chunks(sample_chunks, count_chars)
for c in result:
    print(f"  {c}")
print()

# ----- 6. Lambda 匿名函数 -----
print("=" * 50)
print("6. Lambda 匿名函数")
print("=" * 50)

results = [
    {"content": "文档A: RAG技术详解", "score": 0.7},
    {"content": "文档B: 向量检索原理", "score": 0.95},
    {"content": "文档C: LangChain入门", "score": 0.85},
    {"content": "文档D: Docker部署", "score": 0.60},
]

# 按分数排序
sorted_by_score = sorted(results, key=lambda r: r["score"], reverse=True)
print("按分数降序:")
for r in sorted_by_score:
    print(f"  [{r['score']:.2f}] {r['content']}")

# 用 lambda 做简单变换
texts = ["Hello", "World", "RAG"]
upper_texts = list(map(lambda t: t.upper(), texts))
print(f"\n转大写: {upper_texts}")
print()

# ----- 7. 可变参数 -----
print("=" * 50)
print("7. 可变参数 *args 和 **kwargs")
print("=" * 50)

def build_context(*chunks):
    """接收任意数量的文本块，拼接成上下文"""
    return "\n---\n".join(chunks)

context = build_context("第一段关于RAG的描述", "第二段关于向量检索", "第三段关于LangChain")
print("拼接的上下文:")
print(context)

def build_metadata(**kwargs):
    """接收任意关键字参数，构建元数据字典"""
    return kwargs

meta = build_metadata(source="doc.pdf", page=5, chunk_id="c001", model="gpt-4o")
print(f"\n元数据: {meta}")
print()

# ----- 8. 综合示例：用函数构建 RAG 管道 -----
print("=" * 50)
print("综合示例：用函数构建迷你 RAG 管道")
print("=" * 50)

def load_document(text):
    """第1步：加载文档（模拟）"""
    print(f"  [加载] 文档长度: {len(text)} 字符")
    return text

def split_document(text, chunk_size=60):
    """第2步：切分文档"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    print(f"  [切分] 切成 {len(chunks)} 个块")
    return chunks

def search_chunks(query, chunks, top_k=2):
    """第3步：模拟检索（这里用简单的包含判断，真实项目用向量检索）"""
    results = []
    for chunk in chunks:
        # 简单的关键词匹配（真实项目会用向量相似度）
        score = sum(1 for word in query if word in chunk) / len(query)
        results.append({"content": chunk, "score": score})

    # 按分数排序，取 top_k
    results.sort(key=lambda r: r["score"], reverse=True)
    top_results = results[:top_k]
    print(f"  [检索] 从 {len(chunks)} 个块中找到 {len(top_results)} 个相关块")
    return top_results

def generate_answer(query, context_chunks):
    """第4步：模拟生成回答（真实项目调用 LLM）"""
    context = "\n".join([c["content"] for c in context_chunks])
    answer = f"根据检索到的 {len(context_chunks)} 个相关文档块，关于'{query}'的回答：\n{context}"
    print(f"  [生成] 基于 {len(context_chunks)} 个块生成回答")
    return answer

def rag_pipeline(question, document_text):
    """完整的 RAG 管道：加载 → 切分 → 检索 → 生成"""
    print(f"\n问题: {question}")
    print("-" * 40)

    # 第1步：加载
    doc = load_document(document_text)

    # 第2步：切分
    chunks = split_document(doc, chunk_size=40)

    # 第3步：检索
    results = search_chunks(question, chunks, top_k=2)

    # 第4步：生成
    answer = generate_answer(question, results)

    return answer

# 运行 RAG 管道
knowledge_base = """RAG（检索增强生成）是一种AI技术架构，通过检索外部知识库来增强大语言模型的回答能力。
向量数据库是RAG系统的核心组件，用于存储和检索文本的Embedding向量表示。
LangChain是一个流行的大模型应用开发框架，提供了丰富的工具链。
FastAPI是高性能的Python Web框架，适合构建RAG系统的API接口。
Docker用于容器化部署，确保RAG系统在任何环境中都能一致运行。"""

answer = rag_pipeline("什么是向量数据库？", knowledge_base)
print(f"\n最终回答:\n{answer}")
