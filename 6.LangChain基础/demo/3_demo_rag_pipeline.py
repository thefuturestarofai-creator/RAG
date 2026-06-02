"""
Demo 3: 完整 RAG 管道
====================

功能：
- 文档加载 → 切分 → Embedding → Chroma存储 → 检索 → LLM回答

前置条件：
- pip install langchain langchain-openai langchain-community langchain-chroma langchain-text-splitters chromadb
- 需要 API Key

对应理论：3.向量存储与检索.md

使用的版本（建议）：
- langchain>=0.2.0
- langchain-openai>=0.1.0
- langchain-community>=0.2.0
- langchain-chroma>=0.1.0
- chromadb>=0.5.0
"""

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ============================================================
# 请填写你的模型配置
# ============================================================
API_KEY = "your-api-key-here"       # 替换为你的 API Key
BASE_URL = "https://api.openai.com/v1"  # 替换为你的 Base URL
MODEL = "gpt-4o-mini"               # 推荐：gpt-4o-mini（性价比高）或 gpt-4o（更强）


# ============================================================
# 第一步：准备知识库文档
# ============================================================
print("=" * 60)
print("第一步：准备知识库文档")
print("=" * 60)

# 创建示例知识库
knowledge_content = """Python虚拟环境指南

什么是虚拟环境？
Python虚拟环境是一个独立的Python运行环境。它允许你在不同的项目中使用不同版本的包，而不会相互影响。
虚拟环境就像是给每个项目一个独立的"房间"，各个房间里的家具（包）互不影响。

为什么要使用虚拟环境？
1. 隔离依赖：不同项目可能需要不同版本的同一个包。
2. 避免冲突：全局安装的包可能与项目需求冲突。
3. 便于部署：可以精确记录项目依赖，方便在其他机器上复现。
4. 保持整洁：不会污染系统的Python环境。

如何创建虚拟环境？
使用venv模块创建虚拟环境：
1. 打开终端，进入项目目录
2. 运行命令：python -m venv myenv
3. 激活虚拟环境：
   - Windows: myenv\\Scripts\\activate
   - Mac/Linux: source myenv/bin/activate
4. 激活后，终端提示符会显示环境名称

如何管理依赖？
1. 安装包：pip install package_name
2. 生成依赖文件：pip freeze > requirements.txt
3. 从文件安装：pip install -r requirements.txt
4. 查看已安装包：pip list

conda和venv有什么区别？
conda是一个跨平台的包管理和环境管理工具，它可以管理Python本身以及非Python的依赖。
venv是Python内置的虚拟环境工具，只能管理Python包。
选择建议：数据科学项目推荐conda，Web开发等项目推荐venv。
"""

file_path = "python_venv_guide.txt"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(knowledge_content)

print(f"已创建知识库文件：{file_path}")


# ============================================================
# 第二步：加载并切分文档
# ============================================================
print("\n" + "=" * 60)
print("第二步：加载并切分文档")
print("=" * 60)

# 加载文档
loader = TextLoader(file_path, encoding="utf-8")
documents = loader.load()

# 切分文档
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]
)
chunks = splitter.split_documents(documents)

print(f"文档已切分为 {len(chunks)} 个块")
for i, chunk in enumerate(chunks):
    preview = chunk.page_content[:60].replace("\n", " ")
    print(f"  块{i+1}: {preview}...")


# ============================================================
# 第三步：创建向量数据库
# ============================================================
print("\n" + "=" * 60)
print("第三步：创建向量数据库（Embedding + Chroma）")
print("=" * 60)

# 创建 Embedding 模型
embeddings = OpenAIEmbeddings(
    api_key=API_KEY,
    base_url=BASE_URL,
    model="text-embedding-3-small"
)

# 创建向量数据库（同时完成 Embedding 和存储）
persist_dir = "./chroma_db"

# 如果存在旧的数据库，先删除
if os.path.exists(persist_dir):
    import shutil
    shutil.rmtree(persist_dir)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=persist_dir
)

print(f"向量数据库已创建，存储目录：{persist_dir}")
print(f"已存储 {vectorstore._collection.count()} 个文档块")


# ============================================================
# 第四步：创建检索器
# ============================================================
print("\n" + "=" * 60)
print("第四步：创建检索器并测试")
print("=" * 60)

# 创建检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # 返回前3个最相关的文档
)

# 测试检索
test_query = "如何创建虚拟环境？"
print(f"\n测试检索 - 查询：{test_query}")
retrieved_docs = retriever.invoke(test_query)

for i, doc in enumerate(retrieved_docs):
    preview = doc.page_content[:80].replace("\n", " ")
    print(f"  检索结果{i+1}: {preview}...")


# ============================================================
# 第五步：构建完整 RAG 管道
# ============================================================
print("\n" + "=" * 60)
print("第五步：构建完整 RAG 管道")
print("=" * 60)

# 创建 LLM
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    model=MODEL,
    temperature=0  # RAG 场景建议低温度
)

# 创建 RAG 提示模板
rag_prompt = ChatPromptTemplate.from_template("""
你是一个Python技术助手。请根据以下检索到的文档内容回答用户的问题。
如果文档中没有相关信息，请如实说明。

检索到的文档：
{context}

用户问题：{question}

请回答：
""")

def format_docs(docs):
    """将检索到的文档格式化为字符串"""
    formatted = []
    for i, doc in enumerate(docs, 1):
        formatted.append(f"[文档{i}] {doc.page_content}")
    return "\n\n".join(formatted)

# 构建 RAG 管道（使用 LCEL）
rag_chain = (
    {
        "context": retriever | format_docs,  # 检索 + 格式化
        "question": RunnablePassthrough()     # 直接传递问题
    }
    | rag_prompt                              # 填充提示模板
    | llm                                     # 调用 LLM
    | StrOutputParser()                       # 解析输出
)

print("RAG 管道已构建完成！")


# ============================================================
# 第六步：测试 RAG 问答
# ============================================================
print("\n" + "=" * 60)
print("第六步：测试 RAG 问答")
print("=" * 60)

questions = [
    "什么是虚拟环境？为什么要用它？",
    "如何创建和激活虚拟环境？",
    "conda和venv有什么区别？"
]

for i, question in enumerate(questions, 1):
    print(f"\n问题{i}：{question}")
    print("-" * 40)
    answer = rag_chain.invoke(question)
    print(f"回答：{answer}")


# ============================================================
# 清理
# ============================================================
print("\n" + "=" * 60)
print("清理临时文件")
print("=" * 60)

os.remove(file_path)
print(f"已删除：{file_path}")
print("注意：Chroma 数据库目录 ./chroma_db 已保留，可手动删除")
