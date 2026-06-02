"""
Demo 4: 文本切分策略对比
========================

本脚本演示 4 种主流的文本切分策略，并对比它们的效果：
1. 固定长度切分（Fixed-size Chunking）
2. 递归字符切分（Recursive Character Splitting）
3. 语义切分（Semantic Chunking）
4. 按文档结构切分（Document Structure Splitting）

运行方式：
    python 4_demo_chunking_strategies.py

不需要 API Key（使用本地实现，不调用外部 API）
"""

# ============================================================
# 第一部分：准备测试文本
# ============================================================

# 一段用于测试的中文文档（模拟 RAG 相关的技术文档）
SAMPLE_DOCUMENT = """
# RAG 系统概述

## 什么是 RAG？

RAG（Retrieval-Augmented Generation，检索增强生成）是一种结合了信息检索和文本生成的技术框架。
它的核心思想是：先从知识库中检索相关文档，然后将检索到的文档作为上下文，输入给大语言模型生成回答。

RAG 的优势在于：
1. 知识可以实时更新，不需要重新训练模型
2. 回答有据可查，可以追溯到具体来源
3. 减少模型幻觉，提高回答准确性
4. 成本比微调模型更低

## RAG 的核心组件

一个完整的 RAG 系统包含以下核心组件：

### 1. 文档加载器（Document Loader）

文档加载器负责将各种格式的文档（PDF、Word、Markdown、网页等）转换为统一的文本格式。
常用的加载器包括：
- PyPDFLoader：加载 PDF 文档
- TextLoader：加载纯文本文件
- DirectoryLoader：批量加载目录中的文档
- WebBaseLoader：加载网页内容

### 2. 文本切分器（Text Splitter）

文本切分器将长文档切分成较小的文本块（Chunk）。
切分的原因是：
- Embedding 模型有 Token 限制
- 小块文本更容易匹配查询意图
- 可以控制检索结果的数量和质量

### 3. 向量数据库（Vector Store）

向量数据库用于存储文本块的向量表示（Embedding）。
常用的向量数据库包括：
- Chroma：轻量级，适合开发测试
- FAISS：Facebook 开源，性能优秀
- Pinecone：云服务，适合生产环境
- Weaviate：支持混合检索

### 4. 检索器（Retriever）

检索器负责根据用户查询，从向量数据库中找到最相关的文本块。
检索策略包括：
- 相似度检索：基于向量相似度
- MMR 检索：平衡相关性和多样性
- 混合检索：结合关键词和语义检索

### 5. 生成器（Generator）

生成器是大语言模型，负责根据检索到的文本块生成回答。
常用的模型包括：
- GPT-4：OpenAI 的旗舰模型
- Claude：Anthropic 的对话模型
- Llama：Meta 的开源模型
- Qwen：阿里的通义千问

## RAG 的工作流程

RAG 的工作流程可以分为两个阶段：

### 索引阶段（离线）

1. 加载文档：从各种来源读取文档
2. 文档切分：将长文档切分成小块
3. 生成向量：用 Embedding 模型将文本转换为向量
4. 存储向量：将向量存入向量数据库

### 查询阶段（在线）

1. 用户提问：用户输入问题
2. 问题向量化：将问题转换为向量
3. 相似度检索：在向量数据库中找到最相关的文本块
4. 构建 Prompt：将检索到的文本块和问题组合成 Prompt
5. 生成回答：调用 LLM 生成最终回答

## 文本切分策略详解

文本切分是 RAG 管道中最关键的环节之一。切分质量直接影响检索效果。

### 策略一：固定长度切分

最简单的切分方式，按照固定的字符数切分。
- 优点：实现简单，速度快
- 缺点：可能在句子中间断开，破坏语义

### 策略二：递归字符切分

按照分隔符的优先级递归切分。
- 优点：尊重文本结构，保持语义完整
- 缺点：需要调参

### 策略三：语义切分

使用 Embedding 模型计算语义相似度，在语义变化处切分。
- 优点：切分点符合语义边界
- 缺点：需要调用 Embedding 模型，成本高

### 策略四：按文档结构切分

根据文档的标题、章节等结构进行切分。
- 优点：保留文档层级结构
- 缺点：依赖文档格式

## 最佳实践建议

1. 从递归字符切分开始，Chunk Size 500，Overlap 15%
2. 给每个 Chunk 注入 Metadata（来源、章节、页码）
3. 用真实查询测试不同参数的效果
4. 根据测试结果调优 Chunk Size 和 Overlap
"""


def print_separator(title: str):
    """打印分隔线和标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def print_chunks(chunks: list, max_display: int = 5):
    """打印切分结果，最多显示 max_display 个 chunk"""
    print(f"总共切分为 {len(chunks)} 个 chunk\n")
    for i, chunk in enumerate(chunks[:max_display]):
        # 截断显示，避免输出太长
        display_text = chunk[:100] + "..." if len(chunk) > 100 else chunk
        display_text = display_text.replace("\n", "\\n")  # 换行符转义显示
        print(f"  Chunk {i+1} (长度 {len(chunk)} 字符):")
        print(f"    {display_text}")
        print()
    if len(chunks) > max_display:
        print(f"  ... 还有 {len(chunks) - max_display} 个 chunk 未显示\n")


# ============================================================
# 第二部分：策略1 - 固定长度切分
# ============================================================

def fixed_size_chunking(text: str, chunk_size: int = 200, overlap: int = 0) -> list:
    """
    固定长度切分策略

    原理：按照固定的字符数切分，不考虑文本内容
    类比：就像用尺子量布，每隔 N 厘米剪一刀

    参数：
        text: 要切分的文本
        chunk_size: 每个 chunk 的字符数
        overlap: 相邻 chunk 的重叠字符数
    返回：
        切分后的文本列表
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():  # 跳过空白 chunk
            chunks.append(chunk)
        start = end - overlap  # 移动到下一个位置（考虑重叠）
    return chunks


# ============================================================
# 第三部分：策略2 - 递归字符切分
# ============================================================

def recursive_character_splitting(
    text: str,
    chunk_size: int = 200,
    overlap: int = 30,
    separators: list = None
) -> list:
    """
    递归字符切分策略

    原理：按照分隔符的优先级递归切分
    先尝试用段落分隔符，如果还是太长，就用换行符，再不行就用句号...

    类比：就像切蛋糕，先沿着纹路切，如果一块太大，再切小一点

    参数：
        text: 要切分的文本
        chunk_size: 每个 chunk 的最大字符数
        overlap: 相邻 chunk 的重叠字符数
        separators: 分隔符列表（按优先级排序）
    返回：
        切分后的文本列表
    """
    if separators is None:
        # 中文文档常用的分隔符优先级
        separators = ["\n\n", "\n", "。", "！", "？", "；", "，", "、", " ", ""]

    def _split_text(text: str, separators: list) -> list:
        """递归切分的核心函数"""
        final_chunks = []

        # 如果文本已经够短，直接返回
        if len(text) <= chunk_size:
            if text.strip():
                return [text.strip()]
            return []

        # 尝试用不同的分隔符切分
        separator = separators[-1]  # 默认用最后一个（最细粒度的）
        for sep in separators:
            if sep in text:
                separator = sep
                break

        # 按分隔符切分
        splits = text.split(separator)

        # 合并小块，直到达到 chunk_size
        current_chunk = ""
        for split in splits:
            # 如果当前块加上新内容不超过限制，就合并
            if len(current_chunk) + len(split) + len(separator) <= chunk_size:
                current_chunk += split + separator
            else:
                # 保存当前块
                if current_chunk.strip():
                    final_chunks.append(current_chunk.strip())
                current_chunk = split + separator

        # 保存最后一块
        if current_chunk.strip():
            final_chunks.append(current_chunk.strip())

        # 对于仍然太长的块，递归切分
        result = []
        for chunk in final_chunks:
            if len(chunk) > chunk_size and len(separators) > 1:
                # 用更细粒度的分隔符继续切分
                sub_chunks = _split_text(chunk, separators[1:])
                result.extend(sub_chunks)
            else:
                result.append(chunk)

        return result

    chunks = _split_text(text, separators)

    # 添加 overlap（简化实现）
    if overlap > 0 and len(chunks) > 1:
        overlapped_chunks = [chunks[0]]
        for i in range(1, len(chunks)):
            # 从前一个 chunk 的末尾取 overlap 个字符
            prev_tail = chunks[i-1][-overlap:] if len(chunks[i-1]) > overlap else chunks[i-1]
            overlapped_chunks.append(prev_tail + chunks[i])
        return overlapped_chunks

    return chunks


# ============================================================
# 第四部分：策略3 - 语义切分（简化版，不调用 Embedding API）
# ============================================================

def semantic_chunking_simulation(
    text: str,
    similarity_threshold: float = 0.5
) -> list:
    """
    语义切分策略（模拟版本）

    原理说明：
    真正的语义切分需要调用 Embedding 模型计算相邻句子的相似度。
    这里我们用简化的方式模拟：基于段落和主题变化来切分。

    在实际项目中，你会使用：
    from langchain_experimental.text_splitter import SemanticChunker
    from langchain_openai import OpenAIEmbeddings

    splitter = SemanticChunker(OpenAIEmbeddings())
    chunks = splitter.split_text(text)

    参数：
        text: 要切分的文本
        similarity_threshold: 相似度阈值（这里未使用，仅作说明）
    返回：
        切分后的文本列表
    """
    # 模拟语义切分：按段落切分，保留每个段落的完整性
    # 这是一种启发式方法，真正的语义切分需要 Embedding 模型

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # 如果当前块加上新段落太长，就保存当前块，开始新块
        if len(current_chunk) + len(para) > 300 and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            current_chunk += "\n\n" + para if current_chunk else para

    # 保存最后一块
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


# ============================================================
# 第五部分：策略4 - 按文档结构切分
# ============================================================

def structure_based_chunking(text: str) -> list:
    """
    按文档结构切分策略

    原理：根据文档的标题、章节等结构进行切分
    类比：就像按照书的目录来分章节

    参数：
        text: 要切分的文本（Markdown 格式）
    返回：
        切分后的文本列表，每个 chunk 包含章节标题
    """
    lines = text.split("\n")

    chunks = []
    current_chunk = ""
    current_header = ""

    for line in lines:
        # 检测 Markdown 标题
        if line.startswith("#"):
            # 遇到新标题，保存之前的 chunk
            if current_chunk.strip():
                # 在 chunk 前面加上所属的标题
                if current_header:
                    chunk_with_header = current_header + "\n" + current_chunk
                else:
                    chunk_with_header = current_chunk
                chunks.append(chunk_with_header.strip())

            # 更新当前标题
            current_header = line
            current_chunk = ""
        else:
            current_chunk += line + "\n"

    # 保存最后一个 chunk
    if current_chunk.strip():
        if current_header:
            chunk_with_header = current_header + "\n" + current_chunk
        else:
            chunk_with_header = current_chunk
        chunks.append(chunk_with_header.strip())

    # 对于过长的 chunk，进行二次切分
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > 500:
            # 用递归切分处理过长的 chunk
            sub_chunks = recursive_character_splitting(chunk, chunk_size=300, overlap=30)
            final_chunks.extend(sub_chunks)
        else:
            final_chunks.append(chunk)

    return final_chunks


# ============================================================
# 第六部分：Chunk Size 和 Overlap 调优演示
# ============================================================

def demonstrate_chunk_size_impact():
    """
    演示不同 Chunk Size 的效果
    """
    print_separator("Chunk Size 调优演示")

    test_text = SAMPLE_DOCUMENT[:1000]  # 取前 1000 字符用于演示

    chunk_sizes = [100, 200, 400, 800]

    for size in chunk_sizes:
        chunks = recursive_character_splitting(test_text, chunk_size=size, overlap=0)
        print(f"Chunk Size = {size} 字符:")
        print(f"  切分结果：{len(chunks)} 个 chunk")
        if chunks:
            avg_len = sum(len(c) for c in chunks) / len(chunks)
            print(f"  平均长度：{avg_len:.0f} 字符")
        print()


def demonstrate_overlap_impact():
    """
    演示不同 Overlap 的效果
    """
    print_separator("Chunk Overlap 调优演示")

    test_text = "。".join([
        "这是第一段内容，包含重要信息A",
        "这是第二段内容，包含重要信息B",
        "这是第三段内容，包含重要信息C",
        "这是第四段内容，包含重要信息D",
    ])

    overlaps = [0, 10, 20]

    for overlap in overlaps:
        chunks = recursive_character_splitting(
            test_text,
            chunk_size=50,
            overlap=overlap
        )
        print(f"Overlap = {overlap} 字符:")
        print(f"  切分结果：{len(chunks)} 个 chunk")
        for i, chunk in enumerate(chunks):
            display = chunk[:60] + "..." if len(chunk) > 60 else chunk
            print(f"  Chunk {i+1}: {display}")
        print()


# ============================================================
# 第七部分：主程序 - 对比四种策略
# ============================================================

def main():
    """
    主函数：对比四种切分策略的效果
    """
    print_separator("RAG 文本切分策略对比 Demo")

    print("本文档演示 4 种主流的文本切分策略：")
    print("1. 固定长度切分（Fixed-size Chunking）")
    print("2. 递归字符切分（Recursive Character Splitting）")
    print("3. 语义切分（Semantic Chunking - 模拟版）")
    print("4. 按文档结构切分（Document Structure Splitting）")
    print()
    print("测试文档长度：", len(SAMPLE_DOCUMENT), "字符")

    # ---- 策略1：固定长度切分 ----
    print_separator("策略1：固定长度切分")
    print("原理：按照固定的字符数切分，不考虑文本内容")
    print("类比：就像用尺子量布，每隔 200 字符剪一刀")
    print()

    chunks_fixed = fixed_size_chunking(SAMPLE_DOCUMENT, chunk_size=200, overlap=0)
    print_chunks(chunks_fixed)

    # ---- 策略2：递归字符切分 ----
    print_separator("策略2：递归字符切分")
    print("原理：按照分隔符的优先级递归切分")
    print("优先级：段落 > 换行 > 句号 > 逗号 > 空格 > 字符")
    print()

    chunks_recursive = recursive_character_splitting(
        SAMPLE_DOCUMENT,
        chunk_size=200,
        overlap=30
    )
    print_chunks(chunks_recursive)

    # ---- 策略3：语义切分 ----
    print_separator("策略3：语义切分（模拟版）")
    print("原理：基于段落和主题变化来切分")
    print("注意：真正的语义切分需要调用 Embedding API")
    print()

    chunks_semantic = semantic_chunking_simulation(SAMPLE_DOCUMENT)
    print_chunks(chunks_semantic)

    # ---- 策略4：按文档结构切分 ----
    print_separator("策略4：按文档结构切分")
    print("原理：根据 Markdown 标题进行切分")
    print("类比：按照书的目录来分章节")
    print()

    chunks_structure = structure_based_chunking(SAMPLE_DOCUMENT)
    print_chunks(chunks_structure)

    # ---- 对比总结 ----
    print_separator("四种策略对比总结")

    strategies = [
        ("固定长度切分", chunks_fixed),
        ("递归字符切分", chunks_recursive),
        ("语义切分", chunks_semantic),
        ("按文档结构切分", chunks_structure),
    ]

    print(f"{'策略名称':<15} {'Chunk数量':<10} {'平均长度':<10} {'最大长度':<10} {'最小长度':<10}")
    print("-" * 55)

    for name, chunks in strategies:
        if chunks:
            avg_len = sum(len(c) for c in chunks) / len(chunks)
            max_len = max(len(c) for c in chunks)
            min_len = min(len(c) for c in chunks)
            print(f"{name:<15} {len(chunks):<10} {avg_len:<10.0f} {max_len:<10} {min_len:<10}")

    print()
    print("观察：")
    print("  - 固定长度切分：Chunk 大小一致，但可能破坏语义")
    print("  - 递归字符切分：Chunk 大小较均匀，尊重文本结构")
    print("  - 语义切分：Chunk 大小差异较大，但语义完整性好")
    print("  - 按文档结构切分：保留章节标题，适合 Markdown 文档")

    # ---- 调优演示 ----
    demonstrate_chunk_size_impact()
    demonstrate_overlap_impact()

    # ---- 最佳实践建议 ----
    print_separator("最佳实践建议")
    print("""
1. 首选策略：递归字符切分
   - 通用性最好，大多数场景表现良好
   - 推荐参数：Chunk Size = 500, Overlap = 50-75

2. Markdown 文档：按文档结构切分
   - 保留章节标题作为 Metadata
   - 过长的 chunk 用递归切分二次处理

3. 高精度需求：语义切分
   - 需要调用 Embedding API（有成本）
   - 适合主题频繁切换的文档

4. 快速原型：固定长度切分
   - 实现简单，速度快
   - 适合初期验证想法

5. 通用建议：
   - 给每个 chunk 注入 Metadata（来源、章节、页码）
   - 用真实查询测试不同参数的效果
   - Chunk Overlap 设置为 Chunk Size 的 10-20%
""")


# ============================================================
# 运行主程序
# ============================================================

if __name__ == "__main__":
    main()
