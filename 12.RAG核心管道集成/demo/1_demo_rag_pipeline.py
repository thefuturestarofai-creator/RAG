"""
Demo 1: 完整 RAG 管道

本 Demo 实现一个完整的 RAG 流程：
  文档加载 → 切分 → Embedding → 存储 → 检索 → Prompt 组装 → LLM 生成 → 返回回答

用法：
    python 1_demo_rag_pipeline.py

需要 API Key：
    - OPENAI_API_KEY：用于 Embedding 和 LLM
    - OPENAI_BASE_URL：API 地址（兼容其他 LLM 服务）
    - MODEL：使用的模型名称
"""

import os

# ============================================================
# 配置区域 - 在这里填写你的 API Key
# ============================================================

API_KEY = os.getenv("OPENAI_API_KEY", "sk-your-api-key-here")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


# ============================================================
# 第一步：准备示例文档
# ============================================================

def create_sample_documents():
    """创建示例文档文件。"""

    data_dir = os.path.join(os.path.dirname(__file__), "rag_data")
    os.makedirs(data_dir, exist_ok=True)

    documents = {
        "RAG技术介绍.txt": """\
RAG（Retrieval-Augmented Generation，检索增强生成）是一种结合了信息检索和文本生成的技术框架。

RAG的核心思想是：在大语言模型生成回答之前，先从外部知识库中检索相关的文档片段，然后将这些片段作为参考信息提供给LLM，让LLM基于这些信息生成更准确、更有依据的回答。

RAG的优势：
1. 知识可更新：不需要重新训练模型，只需要更新知识库即可引入新知识
2. 减少幻觉：LLM的回答有据可查，减少了编造信息的风险
3. 可追溯：可以标注回答的来源，增加可信度
4. 成本低：相比微调大模型，RAG的实现成本更低

RAG的典型应用场景：
- 企业知识库问答：基于内部文档回答员工问题
- 客户服务：基于产品文档回答客户咨询
- 学术研究：基于论文库回答研究问题
- 法律咨询：基于法规和案例回答法律问题
""",
        "向量数据库说明.txt": """\
向量数据库是RAG系统的核心组件之一，负责存储和检索文档的向量表示。

什么是向量？
向量是一组数字的有序列表，比如 [0.1, -0.3, 0.5, ...]。
在RAG中，我们用Embedding模型将文本转换为向量，语义相似的文本会生成相近的向量。

主流向量数据库对比：
1. Chroma：轻量级，适合原型开发和小项目，Python原生支持
2. FAISS：Facebook开源，性能极高，适合大规模向量搜索
3. Milvus：分布式架构，适合生产环境，支持多种索引算法
4. Pinecone：云端托管服务，无需自己部署，按使用量计费

选择建议：
- 学习和原型：Chroma（最简单）
- 性能要求高：FAISS（最快）
- 生产环境：Milvus或Pinecone（最稳定）

向量检索的原理：
1. 将查询文本转为向量
2. 在向量空间中找到与查询向量最相似的k个文档向量
3. 返回对应的文档片段
常用的距离度量：余弦相似度、欧氏距离、内积
""",
        "LangChain使用指南.txt": """\
LangChain是一个用于开发LLM应用的Python框架，提供了丰富的组件和工具。

LangChain的核心概念：
1. Document：文档对象，包含page_content（内容）和metadata（元数据）
2. Document Loader：加载各种格式的文件为Document对象
3. Text Splitter：将长文档切分为小块（chunk）
4. Embeddings：将文本转换为向量
5. Vector Store：存储和检索向量
6. Retriever：检索器，根据查询返回相关文档
7. Chain：链，将多个组件串联成处理管道

LangChain的安装：
pip install langchain langchain-openai langchain-community

基本使用示例：
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo")
response = llm.invoke("你好")
print(response.content)

RAG管道的LangChain实现：
1. 加载文档：TextLoader / PDFPlumberLoader
2. 切分文档：RecursiveCharacterTextSplitter
3. 创建向量库：Chroma.from_documents()
4. 创建检索器：vectorstore.as_retriever()
5. 构建RAG链：retriever | prompt | llm | output_parser

LangChain的优势：
- 组件化设计，易于替换和扩展
- 丰富的文档和社区支持
- 支持多种LLM和向量数据库
- 提供LCEL链式调用语法
""",
    }

    for filename, content in documents.items():
        file_path = os.path.join(data_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"✓ 已创建 {len(documents)} 个示例文档到 {data_dir}")
    return data_dir


# ============================================================
# 第二步：完整 RAG 管道实现
# ============================================================

def run_rag_pipeline(data_dir: str, question: str):
    """
    运行完整的 RAG 管道。

    Args:
        data_dir: 文档目录
        question: 用户问题
    """

    print("=" * 60)
    print("  完整 RAG 管道")
    print("=" * 60)

    # ---- 步骤 1: 文档加载 ----
    print("\n[步骤 1/6] 文档加载")
    print("-" * 40)

    from langchain_community.document_loaders import DirectoryLoader, TextLoader

    loader = DirectoryLoader(
        path=data_dir,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()
    print(f"  加载了 {len(documents)} 个文档")
    for doc in documents:
        print(f"    - {doc.metadata['source']}: {len(doc.page_content)} 字符")

    # ---- 步骤 2: 文档切分 ----
    print("\n[步骤 2/6] 文档切分")
    print("-" * 40)

    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "！", "？", ".", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"  {len(documents)} 个文档 → {len(chunks)} 个 chunks")
    print(f"  chunk_size=300, overlap=50")

    # 显示前3个 chunk 的预览
    print("\n  前 3 个 chunks 预览:")
    for i, chunk in enumerate(chunks[:3]):
        print(f"    [{i+1}] {chunk.page_content[:80]}...")

    # ---- 步骤 3: Embedding + 向量存储 ----
    print("\n[步骤 3/6] Embedding + 向量存储")
    print("-" * 40)

    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma

    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        openai_api_key=API_KEY,
        openai_api_base=BASE_URL,
    )

    persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name="rag_demo",
    )
    print(f"  向量数据库已创建，存储目录: {persist_dir}")
    print(f"  共存储 {len(chunks)} 个文档向量")

    # ---- 步骤 4: 相似度检索 ----
    print("\n[步骤 4/6] 相似度检索")
    print("-" * 40)
    print(f"  用户问题: {question}")

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    relevant_docs = retriever.invoke(question)

    print(f"  检索到 {len(relevant_docs)} 个相关文档:")
    for i, doc in enumerate(relevant_docs):
        source = os.path.basename(doc.metadata.get("source", "未知"))
        print(f"    [{i+1}] 来源: {source}")
        print(f"        内容: {doc.page_content[:100]}...")

    # ---- 步骤 5: Prompt 组装 ----
    print("\n[步骤 5/6] Prompt 组装")
    print("-" * 40)

    from langchain.prompts import ChatPromptTemplate

    template = """你是一个知识库助手。请根据以下参考资料回答用户的问题。

要求：
1. 只根据参考资料回答，不要编造信息
2. 如果参考资料中没有相关信息，请如实说明
3. 回答要简洁、准确、有条理

参考资料：
{context}

用户问题：{question}

请回答："""

    context = "\n\n---\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = ChatPromptTemplate.from_template(template)
    messages = prompt.format_messages(context=context, question=question)

    print(f"  Prompt 长度: {len(messages[0].content)} 字符")
    print(f"  参考资料: {len(relevant_docs)} 个文档片段")

    # ---- 步骤 6: LLM 生成 ----
    print("\n[步骤 6/6] LLM 生成回答")
    print("-" * 40)

    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model=MODEL,
        openai_api_key=API_KEY,
        openai_api_base=BASE_URL,
        temperature=0.3,
    )

    print(f"  模型: {MODEL}")
    print(f"  正在生成回答...")

    response = llm.invoke(messages)
    answer = response.content

    # ---- 返回结果 ----
    print("\n" + "=" * 60)
    print("  回答结果")
    print("=" * 60)
    print(f"\n  问题: {question}")
    print(f"\n  回答:\n  {answer}")
    print(f"\n  参考来源:")
    for i, doc in enumerate(relevant_docs):
        source = os.path.basename(doc.metadata.get("source", "未知"))
        print(f"    [{i+1}] {source}")

    return {
        "question": question,
        "answer": answer,
        "sources": [doc.metadata for doc in relevant_docs],
    }


# ============================================================
# 主函数
# ============================================================

def main():
    print("=" * 60)
    print("  Demo 1: 完整 RAG 管道")
    print("=" * 60)

    # 检查 API Key
    if API_KEY == "sk-your-api-key-here":
        print("\n⚠️  请先设置 API Key!")
        print("  方式一：修改脚本顶部的 API_KEY 变量")
        print("  方式二：设置环境变量 OPENAI_API_KEY")
        print("\n  本 Demo 将展示代码结构，但不会实际调用 API。")
        print("  请阅读代码理解完整流程。")

        # 创建示例文档（不需要 API Key）
        data_dir = create_sample_documents()

        print("\n" + "=" * 60)
        print("  RAG 管道流程说明（无需 API Key）")
        print("=" * 60)
        print("""
  完整的 RAG 管道包括 6 个步骤：

  1. 文档加载：用 DirectoryLoader 加载目录下所有 .txt 文件
     → 每个文件变成一个 Document 对象

  2. 文档切分：用 RecursiveCharacterTextSplitter 切分
     → chunk_size=300, overlap=50
     → 长文档切成多个小 chunk

  3. Embedding + 向量存储：
     → 用 OpenAI Embedding 将每个 chunk 转为向量
     → 存入 Chroma 向量数据库

  4. 相似度检索：
     → 将用户问题转为向量
     → 在向量数据库中找 top-3 最相似的 chunk

  5. Prompt 组装：
     → 将检索到的 chunk 拼接为参考资料
     → 用模板将问题和参考资料组装成 Prompt

  6. LLM 生成：
     → 调用 GPT 生成回答
     → 返回问题、回答和来源信息
        """)
        return

    # 实际运行 RAG 管道
    data_dir = create_sample_documents()

    # 运行管道
    question = "RAG是什么？它有什么优势？"
    result = run_rag_pipeline(data_dir, question)

    print("\n" + "=" * 60)
    print("  Demo 运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
