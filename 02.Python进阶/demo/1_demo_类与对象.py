# ============================================================
# Demo 1: 类与对象
# 对应理论文档: 1.类与对象.md
# ============================================================
# 这个 Demo 定义 RAG 中的核心数据结构：Document 和 TextSplitter，
# 演示类的定义、实例化、继承、方法、魔术方法。
# 最后用这些类构建一个完整的文档处理管道。
# 不需要 API Key。
# ============================================================

# ----- 1. 定义 Document 类 -----
# RAG 中每个文档块就是一个 Document 对象

class Document:
    """文档类 —— RAG 中每个文档块的基本结构"""

    # 类属性：所有对象共享
    document_count = 0

    def __init__(self, content, source="unknown", page=None):
        """
        构造方法：创建 Document 对象时自动调用
        - content: 文档内容（字符串）
        - source: 文档来源（文件名）
        - page: 页码（可选）
        """
        self.content = content        # 实例属性：每个对象独有
        self.source = source
        self.page = page
        self.score = 0.0              # 相似度分数，默认 0
        self.chunk_id = None          # 文档块 ID

        Document.document_count += 1  # 每创建一个对象，计数+1
        self.chunk_id = f"chunk_{Document.document_count:03d}"

    def summary(self, max_length=30):
        """返回文档摘要"""
        text = self.content[:max_length]
        if len(self.content) > max_length:
            text += "..."
        return f"[{self.chunk_id}] [{self.source}] {text}"

    def __repr__(self):
        """魔术方法：打印对象时显示的内容"""
        return f"Document(chunk_id='{self.chunk_id}', source='{self.source}', score={self.score})"

    def __lt__(self, other):
        """魔术方法：定义小于比较，用于排序"""
        return self.score < other.score

    def __len__(self):
        """魔术方法：len() 函数的返回值"""
        return len(self.content)

    def __eq__(self, other):
        """魔术方法：判断两个 Document 是否相等"""
        if not isinstance(other, Document):
            return False
        return self.content == other.content and self.source == other.source


# ----- 2. 创建 Document 对象 -----
print("=" * 50)
print("1. 创建 Document 对象")
print("=" * 50)

doc1 = Document("RAG是检索增强生成技术，通过检索外部知识来增强大模型的回答。", "rag_intro.pdf", page=1)
doc2 = Document("向量数据库用于存储和检索文本的Embedding向量表示。", "vector_db.pdf", page=5)
doc3 = Document("LangChain是一个用于构建大模型应用的Python框架。", "langchain.pdf")

print(f"doc1: {doc1}")
print(f"doc2: {doc2}")
print(f"doc3: {doc3}")
print(f"\n摘要: {doc1.summary()}")
print(f"doc1 长度: {len(doc1)} 字符")
print(f"总文档数: {Document.document_count}")
print()


# ----- 3. 继承：定义不同类型的文档 -----
print("=" * 50)
print("2. 继承：不同类型的文档")
print("=" * 50)


class PDFDocument(Document):
    """PDF 文档类 —— 继承 Document，新增 PDF 特有属性"""

    def __init__(self, content, source, page, total_pages):
        super().__init__(content, source, page)   # 调用父类构造方法
        self.total_pages = total_pages             # 子类新增属性

    def page_info(self):
        """子类新增方法"""
        return f"第 {self.page}/{self.total_pages} 页"


class WebDocument(Document):
    """网页文档类 —— 继承 Document，新增 URL 属性"""

    def __init__(self, content, url):
        super().__init__(content, source=url)     # 用 url 作为 source
        self.url = url

    def get_domain(self):
        """子类新增方法：提取域名"""
        parts = self.url.split("/")
        return parts[2] if len(parts) > 2 else "unknown"


# 使用子类
pdf = PDFDocument("这是PDF文档的内容...", "paper.pdf", page=3, total_pages=10)
web = WebDocument("这是网页抓取的内容...", "https://example.com/article")

print(f"PDF 文档: {pdf}")
print(f"PDF 页码: {pdf.page_info()}")
print(f"PDF 摘要: {pdf.summary()}")        # 继承自父类的方法

print(f"\n网页文档: {web}")
print(f"网页域名: {web.get_domain()}")
print(f"网页长度: {len(web)}")             # 继承自父类的魔术方法
print()


# ----- 4. 定义 TextSplitter 类 -----
print("=" * 50)
print("3. TextSplitter 文本切分器")
print("=" * 50)


class TextSplitter:
    """文本切分器 —— 将长文本切分成小块"""

    def __init__(self, chunk_size=100, overlap=20):
        """
        - chunk_size: 每块的最大字符数
        - overlap: 相邻块之间的重叠字符数（保证上下文连贯）
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text, source="unknown"):
        """将文本切分成多个 Document 对象"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_content = text[start:end]
            doc = Document(chunk_content, source=source)
            chunks.append(doc)
            start = end - self.overlap    # 向前回退 overlap 个字符
            if start < 0:
                start = 0
            if start >= len(text):
                break
        return chunks

    def __repr__(self):
        return f"TextSplitter(chunk_size={self.chunk_size}, overlap={self.overlap})"


# 使用 TextSplitter
long_text = "RAG（检索增强生成）是一种结合了信息检索和文本生成的技术。" \
            "它的核心思想是：先从知识库中检索相关文档，再将检索结果作为上下文提供给大模型，" \
            "让大模型基于这些真实信息生成回答。这样可以有效减少幻觉，提高回答的准确性和可追溯性。"

splitter = TextSplitter(chunk_size=50, overlap=10)
chunks = splitter.split(long_text, source="rag_intro.txt")

print(f"切分器: {splitter}")
print(f"原文长度: {len(long_text)} 字符")
print(f"切分结果: {len(chunks)} 个文档块\n")

for i, chunk in enumerate(chunks):
    print(f"  块 {i+1}: {chunk.summary(max_length=40)}")
print()


# ----- 5. 排序和过滤 -----
print("=" * 50)
print("4. 排序和过滤（魔术方法的实际应用）")
print("=" * 50)

# 模拟检索结果（给每个文档打分）
import random
random.seed(42)    # 固定随机种子，保证结果可复现

docs = [
    Document("RAG通过检索外部知识来增强LLM回答", "doc1.txt"),
    Document("向量数据库用于存储Embedding向量", "doc2.txt"),
    Document("今天天气真不错适合出门", "doc3.txt"),
    Document("LangChain是大模型应用开发框架", "doc4.txt"),
    Document("Docker用于容器化部署应用", "doc5.txt"),
]

# 给每个文档打一个随机分数
for doc in docs:
    doc.score = round(random.uniform(0.3, 0.99), 2)

print("原始检索结果:")
for doc in docs:
    print(f"  {doc} (内容: {doc.content[:15]}...)")

# 排序（因为定义了 __lt__，可以直接 sort）
docs.sort(reverse=True)    # 降序排列
print("\n按分数降序排列:")
for doc in docs:
    print(f"  {doc}")

# 过滤高分结果
threshold = 0.7
relevant = [doc for doc in docs if doc.score >= threshold]
print(f"\n过滤 (分数 >= {threshold}): {len(relevant)} 条")
for doc in relevant:
    print(f"  {doc}")
print()


# ----- 6. 综合示例：文档处理管道 -----
print("=" * 50)
print("综合示例：完整的文档处理管道")
print("=" * 50)


def simulate_rag_pipeline(raw_documents):
    """
    模拟 RAG 的文档处理流程：
    1. 读取原始文档
    2. 切分成小块
    3. 模拟检索（随机打分）
    4. 过滤和排序
    5. 构造上下文
    """
    print("\n--- 第1步：读取原始文档 ---")
    for doc in raw_documents:
        print(f"  已加载: {doc.source} ({len(doc)} 字符)")

    print("\n--- 第2步：文本切分 ---")
    splitter = TextSplitter(chunk_size=80, overlap=20)
    all_chunks = []
    for doc in raw_documents:
        chunks = splitter.split(doc.content, source=doc.source)
        all_chunks.extend(chunks)
        print(f"  {doc.source} → {len(chunks)} 个块")
    print(f"  总计: {len(all_chunks)} 个文档块")

    print("\n--- 第3步：模拟检索（随机打分） ---")
    random.seed(123)
    for chunk in all_chunks:
        chunk.score = round(random.uniform(0.2, 0.99), 2)
    print(f"  已为 {len(all_chunks)} 个块打分")

    print("\n--- 第4步：过滤和排序 ---")
    threshold = 0.6
    relevant = [c for c in all_chunks if c.score >= threshold]
    relevant.sort(reverse=True)    # 按分数降序
    top_k = relevant[:3]           # 取 Top 3
    print(f"  阈值过滤: {len(all_chunks)} → {len(relevant)} 条")
    print(f"  取 Top {len(top_k)}:")
    for doc in top_k:
        print(f"    {doc}")

    print("\n--- 第5步：构造上下文 ---")
    context = "\n".join([f"[来源: {d.source}] {d.content}" for d in top_k])
    print(f"  上下文长度: {len(context)} 字符")

    return top_k, context


# 运行管道
raw_docs = [
    Document(
        "RAG（检索增强生成）是一种结合信息检索和文本生成的技术。"
        "它先从知识库中检索相关文档，再将结果作为上下文提供给大模型。",
        source="rag_intro.txt"
    ),
    Document(
        "向量数据库是 RAG 系统的核心组件。常见的向量数据库有 Chroma、FAISS、Pinecone 等。"
        "它们支持高效的相似度检索。",
        source="vector_db.txt"
    ),
    Document(
        "LangChain 提供了 Document Loader、Text Splitter、Retriever 等组件。"
        "开发者可以用它快速搭建 RAG 应用。",
        source="langchain.txt"
    ),
]

top_results, context = simulate_rag_pipeline(raw_docs)

print(f"\n最终结果:")
print(f"检索到 {len(top_results)} 个最相关的文档块")
print(f"\n构造的上下文:\n{context}")
