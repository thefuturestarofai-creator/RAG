"""
Demo 2: 带来源追溯的 RAG

本 Demo 在 Demo 1 的基础上，增加来源追溯功能：
1. 回答中标注信息来源（哪个文件、第几页）
2. 返回结构化的来源信息
3. 用 metadata 记录文档来源

用法：
    python 2_demo_rag_with_sources.py

需要 API Key：
    - OPENAI_API_KEY：用于 Embedding 和 LLM
    - OPENAI_BASE_URL：API 地址
    - MODEL：使用的模型名称
"""

import os
import json
from typing import List, Dict, Any

# ============================================================
# 配置区域
# ============================================================

API_KEY = os.getenv("OPENAI_API_KEY", "sk-your-api-key-here")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


# ============================================================
# 第一步：创建带 metadata 的示例文档
# ============================================================

def create_documents_with_metadata():
    """创建示例文档，每个文档都有详细的 metadata。"""

    data_dir = os.path.join(os.path.dirname(__file__), "rag_data_with_meta")
    os.makedirs(data_dir, exist_ok=True)

    documents = [
        {
            "filename": "RAG技术白皮书.txt",
            "content": """\
RAG技术白皮书
作者：AI研究院
版本：V2.0
日期：2024年6月

第一章 RAG概述

RAG（Retrieval-Augmented Generation，检索增强生成）是一种将信息检索与文本生成相结合的技术框架。
该技术由Facebook AI Research（FAIR）团队于2020年提出，旨在解决大语言模型的知识更新和幻觉问题。

RAG的核心流程包括三个阶段：
1. 索引阶段：将文档加载、切分、向量化后存入向量数据库
2. 检索阶段：根据用户查询，从向量数据库中检索相关文档片段
3. 生成阶段：将检索到的片段与查询一起输入LLM，生成最终回答

第二章 RAG的优势

相比传统的纯LLM方案，RAG具有以下优势：

1. 知识时效性：通过更新知识库即可引入新知识，无需重新训练模型
2. 减少幻觉：LLM的回答基于检索到的真实文档，大幅减少编造信息
3. 可追溯性：可以标注回答的来源文档和具体位置
4. 成本效益：比微调大模型的成本低得多
5. 灵活性：可以针对不同场景使用不同的知识库

第三章 RAG的挑战

1. 检索质量：如果检索不到相关文档，生成的回答质量会很差
2. chunk切分：切分策略直接影响检索效果
3. 上下文窗口：LLM的上下文长度限制了参考资料的数量
4. 延迟：检索和生成都会增加响应时间
""",
            "metadata": {
                "source": "RAG技术白皮书.txt",
                "author": "AI研究院",
                "version": "V2.0",
                "date": "2024-06",
                "category": "技术文档",
            }
        },
        {
            "filename": "RAG应用案例集.txt",
            "content": """\
RAG应用案例集
编辑：产品部
日期：2024年5月

案例一：企业知识库问答

客户：某大型制造企业
需求：基于内部技术文档和操作手册，为工程师提供智能问答服务
方案：部署RAG系统，导入500+份技术文档，构建企业知识库
效果：
- 问题回答准确率：92%
- 平均响应时间：2.3秒
- 工程师效率提升：40%

案例二：智能客服系统

客户：某电商平台
需求：基于产品信息和FAQ，自动回答客户咨询
方案：RAG + 多轮对话管理
效果：
- 客服人力减少：60%
- 客户满意度：95%
- 24小时不间断服务

案例三：法律知识检索

客户：某律师事务所
需求：快速检索相关法规和案例
方案：RAG + 法律知识库（10万+文档）
效果：
- 检索准确率：88%
- 律师研究时间减少：50%
- 支持自然语言查询

案例四：学术论文助手

客户：某高校研究团队
需求：基于论文库回答研究问题
方案：RAG + 论文数据库
效果：
- 支持跨论文检索和问答
- 自动生成文献综述
- 研究效率提升：35%
""",
            "metadata": {
                "source": "RAG应用案例集.txt",
                "author": "产品部",
                "date": "2024-05",
                "category": "案例文档",
            }
        },
    ]

    for doc_info in documents:
        file_path = os.path.join(data_dir, doc_info["filename"])
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(doc_info["content"])

    print(f"✓ 已创建 {len(documents)} 个示例文档到 {data_dir}")
    return data_dir, documents


# ============================================================
# 第二步：带来源追溯的 RAG 管道
# ============================================================

class RAGWithSources:
    """带来源追溯的 RAG 系统。"""

    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.vectorstore = None

    def build_index(self, data_dir: str):
        """构建向量索引。"""
        from langchain_community.document_loaders import DirectoryLoader, TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_openai import OpenAIEmbeddings
        from langchain_community.vectorstores import Chroma

        print("\n[1/3] 加载文档...")
        loader = DirectoryLoader(
            path=data_dir,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        documents = loader.load()
        print(f"  加载了 {len(documents)} 个文档")

        # 为每个文档添加 metadata
        for doc in documents:
            source = doc.metadata.get("source", "")
            filename = os.path.basename(source)
            doc.metadata["filename"] = filename

        print("\n[2/3] 切分文档...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "！", "？", ".", " ", ""]
        )
        chunks = splitter.split_documents(documents)
        print(f"  切分为 {len(chunks)} 个 chunks")

        # 显示 metadata 示例
        print("\n  chunk metadata 示例:")
        for i, chunk in enumerate(chunks[:3]):
            print(f"    [{i+1}] source={chunk.metadata.get('source', '未知')}")
            print(f"        filename={chunk.metadata.get('filename', '未知')}")
            print(f"        content={chunk.page_content[:60]}...")

        print("\n[3/3] 构建向量索引...")
        embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
        )

        persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db_with_meta")
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_dir,
            collection_name="rag_with_sources",
        )
        print(f"  向量索引构建完成!")

    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """
        查询并返回带来源的回答。

        Args:
            question: 用户问题
            top_k: 检索数量

        Returns:
            包含 answer 和 sources 的字典
        """
        from langchain_openai import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate

        # 1. 检索相关文档
        print(f"\n  检索相关文档 (top_k={top_k})...")
        results = self.vectorstore.similarity_search_with_score(question, k=top_k)

        # 2. 构造带来源信息的 context
        context_parts = []
        sources = []

        for i, (doc, score) in enumerate(results, 1):
            source = doc.metadata.get("filename", "未知")
            page = doc.metadata.get("page", "")

            # 添加到 context
            source_info = f"[来源{i}: {source}]"
            context_parts.append(f"{source_info}\n{doc.page_content}")

            # 记录来源
            sources.append({
                "index": i,
                "filename": source,
                "page": page,
                "relevance_score": round(1 - score, 4) if score < 1 else round(score, 4),
                "snippet": doc.page_content[:150],
            })

        context = "\n\n---\n\n".join(context_parts)

        # 3. 构造带来源标注要求的 Prompt
        template = """你是一个知识库助手。请根据以下参考资料回答问题。

要求：
1. 只根据参考资料回答，不要编造信息
2. 在回答中用 [来源X] 标注每条信息的出处
3. 在回答末尾列出参考来源
4. 如果参考资料中没有相关信息，请如实说明

参考资料：
{context}

问题：{question}

回答："""

        prompt = ChatPromptTemplate.from_template(template)
        messages = prompt.format_messages(context=context, question=question)

        # 4. 调用 LLM
        print(f"  调用 LLM 生成回答...")
        llm = ChatOpenAI(
            model=self.model,
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            temperature=0.3,
        )
        response = llm.invoke(messages)
        answer = response.content

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
        }


# ============================================================
# 第三步：结果展示
# ============================================================

def display_result(result: Dict[str, Any]):
    """格式化展示查询结果。"""

    print("\n" + "=" * 60)
    print("  查询结果")
    print("=" * 60)

    print(f"\n  问题: {result['question']}")

    print(f"\n  回答:")
    # 按行显示，加缩进
    for line in result['answer'].split('\n'):
        print(f"    {line}")

    print(f"\n  来源信息 ({len(result['sources'])} 个):")
    for source in result['sources']:
        print(f"    [{source['index']}] 文件: {source['filename']}")
        if source.get('page'):
            print(f"        页码: {source['page']}")
        print(f"        相关度: {source['relevance_score']}")
        print(f"        片段: {source['snippet']}...")
        print()


# ============================================================
# 主函数
# ============================================================

def main():
    print("=" * 60)
    print("  Demo 2: 带来源追溯的 RAG")
    print("=" * 60)

    # 检查 API Key
    if API_KEY == "sk-your-api-key-here":
        print("\n⚠️  请先设置 API Key!")
        print("  方式一：修改脚本顶部的 API_KEY 变量")
        print("  方式二：设置环境变量 OPENAI_API_KEY")

        # 展示代码结构
        data_dir, _ = create_documents_with_metadata()

        print("\n" + "=" * 60)
        print("  来源追溯实现说明（无需 API Key）")
        print("=" * 60)
        print("""
  来源追溯的实现分 3 步：

  1. 文档入库时记录 metadata:
     Document(
         page_content="RAG是...",
         metadata={
             "source": "RAG技术白皮书.txt",
             "author": "AI研究院",
             "page": 1,
         }
     )

  2. 检索时返回 metadata:
     results = vectorstore.similarity_search_with_score(query, k=3)
     for doc, score in results:
         print(doc.metadata["source"])

  3. Prompt 中要求 LLM 标注来源:
     "在回答中用 [来源X] 标注每条信息的出处"

  最终效果示例:
    问题: RAG是什么？
    回答: RAG是检索增强生成技术 [来源1]，
          由Facebook AI Research于2020年提出 [来源1]。
          它的优势包括知识可更新 [来源2]、减少幻觉 [来源2]。

    来源:
    [1] RAG技术白皮书.txt - 相关度: 0.95
    [2] RAG应用案例集.txt - 相关度: 0.87
        """)
        return

    # 实际运行
    data_dir, _ = create_documents_with_metadata()

    rag = RAGWithSources(
        api_key=API_KEY,
        base_url=BASE_URL,
        model=MODEL,
    )

    rag.build_index(data_dir)

    # 测试查询
    questions = [
        "RAG是什么？它有哪些优势？",
        "RAG有哪些实际应用案例？",
    ]

    for question in questions:
        result = rag.query(question)
        display_result(result)

    print("\n" + "=" * 60)
    print("  Demo 运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
