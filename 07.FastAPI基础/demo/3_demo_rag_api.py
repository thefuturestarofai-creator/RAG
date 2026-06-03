"""
Demo 3: RAG问答API - 把RAG管道封装成API接口
=============================================

功能：
- 把第6章的 RAG 管道封装成 FastAPI 接口
- 包含完整的异常处理
- 使用依赖注入管理组件

前置条件：
- pip install fastapi uvicorn langchain langchain-openai langchain-community langchain-chroma chromadb
- 需要 API Key

对应理论：3.依赖注入与异步.md

运行方式：
- uvicorn 3_demo_rag_api:app --reload
- 或 python 3_demo_rag_api.py
"""

import os
import shutil
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from contextlib import asynccontextmanager

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
# Pydantic 模型定义
# ============================================================

class QuestionRequest(BaseModel):
    """问答请求模型"""
    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="用户的问题"
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="检索的文档数量"
    )


class DocumentInfo(BaseModel):
    """检索到的文档信息"""
    content: str = Field(..., description="文档内容")
    source: str = Field(default="unknown", description="文档来源")


class QuestionResponse(BaseModel):
    """问答响应模型"""
    answer: str = Field(..., description="AI的回答")
    documents: List[DocumentInfo] = Field(
        default=[],
        description="检索到的相关文档"
    )
    status: str = Field(default="success", description="状态")


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    components: dict


# ============================================================
# 全局变量（存储 RAG 组件）
# ============================================================
rag_components = {}


# ============================================================
# 应用生命周期管理
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    启动时初始化 RAG 组件，关闭时清理资源
    """
    print("=" * 50)
    print("正在初始化 RAG 系统...")

    try:
        # 1. 创建示例知识库
        knowledge = """Python虚拟环境指南

什么是虚拟环境？
Python虚拟环境是一个独立的Python运行环境，允许在不同项目中使用不同版本的包。
虚拟环境给每个项目一个独立的空间，避免包版本冲突。

如何创建虚拟环境？
使用 venv 模块：python -m venv myenv
激活虚拟环境：
- Windows: myenv\\Scripts\\activate
- Mac/Linux: source myenv/bin/activate

什么是包管理？
pip 是 Python 的包管理工具。
pip install package_name 安装包
pip freeze > requirements.txt 导出依赖
pip install -r requirements.txt 从文件安装依赖

conda和venv的区别？
conda 可以管理 Python 版本和非 Python 依赖。
venv 只能管理 Python 包，是 Python 内置工具。
数据科学用 conda，Web 开发用 venv。
"""

        file_path = "temp_knowledge.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(knowledge)

        # 2. 加载并切分文档
        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]
        )
        chunks = splitter.split_documents(documents)
        print(f"文档已切分为 {len(chunks)} 个块")

        # 3. 创建向量数据库
        embeddings = OpenAIEmbeddings(
            api_key=API_KEY,
            base_url=BASE_URL,
            model="text-embedding-3-small"
        )

        persist_dir = "./rag_chroma_db"
        if os.path.exists(persist_dir):
            shutil.rmtree(persist_dir)

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_dir
        )
        print("向量数据库已创建")

        # 4. 创建检索器
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

        # 5. 创建 LLM
        llm = ChatOpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
            model=MODEL,
            temperature=0
        )

        # 6. 创建 RAG 提示模板
        rag_prompt = ChatPromptTemplate.from_template("""
你是一个Python技术助手。请根据以下文档内容回答用户问题。
如果文档中没有相关信息，请如实说明。

检索到的文档：
{context}

用户问题：{question}

请用简洁清晰的中文回答：
""")

        # 7. 保存组件
        rag_components["retriever"] = retriever
        rag_components["llm"] = llm
        rag_components["rag_prompt"] = rag_prompt
        rag_components["file_path"] = file_path

        print("RAG 系统初始化完成！")
        print("=" * 50)

        yield  # 应用运行期间

    finally:
        # 清理资源
        print("正在清理资源...")
        if "file_path" in rag_components and os.path.exists(rag_components["file_path"]):
            os.remove(rag_components["file_path"])
        print("资源清理完成")


# 创建 FastAPI 应用
app = FastAPI(
    title="RAG 问答系统 API",
    description="基于检索增强生成的智能问答系统",
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================
# 依赖注入
# ============================================================

def get_rag_chain():
    """
    依赖注入：获取 RAG 管道

    将检索、提示、LLM 组合成完整的管道
    """
    retriever = rag_components["retriever"]
    llm = rag_components["llm"]
    rag_prompt = rag_components["rag_prompt"]

    def format_docs(docs):
        return "\n\n".join([f"[文档{i+1}] {doc.page_content}" for i, doc in enumerate(docs)])

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return chain


# ============================================================
# 路由定义
# ============================================================

@app.get("/", tags=["基础"])
async def root():
    """首页"""
    return {"message": "RAG 问答系统 API", "docs": "/docs"}


@app.get("/health", response_model=HealthResponse, tags=["基础"])
async def health_check():
    """健康检查"""
    return HealthResponse(
        status="healthy",
        components={
            "retriever": "retriever" in rag_components,
            "llm": "llm" in rag_components,
            "vectorstore": True
        }
    )


@app.post("/ask", response_model=QuestionResponse, tags=["问答"])
async def ask_question(request: QuestionRequest):
    """
    RAG 问答接口

    接收用户问题，检索相关文档，生成回答
    """
    try:
        # 获取 RAG 管道
        chain = get_rag_chain()

        # 执行检索和生成
        answer = chain.invoke(request.question)

        # 获取检索到的文档（用于返回来源信息）
        retriever = rag_components["retriever"]
        retrieved_docs = retriever.invoke(request.question)

        documents = [
            DocumentInfo(
                content=doc.page_content[:200],
                source=doc.metadata.get("source", "unknown")
            )
            for doc in retrieved_docs
        ]

        return QuestionResponse(
            answer=answer,
            documents=documents,
            status="success"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"处理问题时出错：{str(e)}"
        )


@app.post("/search", tags=["检索"])
async def search_documents(request: QuestionRequest):
    """
    纯检索接口（不经过LLM生成）

    只返回检索到的相关文档
    """
    try:
        retriever = rag_components["retriever"]
        retriever.search_kwargs["k"] = request.top_k

        docs = retriever.invoke(request.question)

        results = [
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown")
            }
            for doc in docs
        ]

        return {
            "query": request.question,
            "results": results,
            "total": len(results)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"检索出错：{str(e)}"
        )


# ============================================================
# 主程序入口
# ============================================================
if __name__ == "__main__":
    import uvicorn

    print("=" * 50)
    print("RAG 问答系统 API")
    print("=" * 50)
    print()
    print("接口说明：")
    print("  - GET  /          - 首页")
    print("  - GET  /health    - 健康检查")
    print("  - POST /ask       - RAG问答（检索+生成）")
    print("  - POST /search    - 纯检索（只检索不生成）")
    print()
    print("API 文档：http://127.0.0.1:8000/docs")
    print()
    print("测试请求体示例：")
    print("""
    {
        "question": "什么是虚拟环境？",
        "top_k": 3
    }
    """)
    print("=" * 50)

    uvicorn.run(app, host="127.0.0.1", port=8000)
