"""
Demo 1: RAG 项目骨架

本 Demo 创建一个完整的 RAG 项目目录结构，并在每个模块中生成占位代码。
运行此脚本后，你会得到一个可以直接运行的项目框架。

用法：
    python 1_demo_project_skeleton.py

运行后会在当前目录下创建 rag_project/ 目录，包含完整的项目结构。
"""

import os


# ============================================================
# 定义项目结构
# ============================================================

# 项目根目录名
PROJECT_NAME = "rag_project"

# 目录结构定义：目录名列表
DIRECTORIES = [
    "config",
    "src",
    "src/document_processing",
    "src/vector_store",
    "src/retrieval",
    "src/generation",
    "src/api",
    "src/utils",
    "tests",
    "data/raw",
    "data/processed",
    "logs",
]

# 文件内容定义：相对路径 -> 内容字符串
FILES = {}


# ============================================================
# 配置文件
# ============================================================

FILES[".env.example"] = """\
# ============================================================
# 环境变量配置示例
# 复制此文件为 .env，然后填入实际值
# .env 文件不应提交到 Git
# ============================================================

# OpenAI 配置
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# Embedding 模型配置
EMBEDDING_MODEL=text-embedding-ada-002

# 向量数据库配置
CHROMA_PERSIST_DIR=./data/chroma_db
COLLECTION_NAME=rag_collection

# 文档处理配置
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# 检索配置
TOP_K=3

# 服务配置
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
"""

FILES[".gitignore"] = """\
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/
*.egg

# 环境变量（包含敏感信息）
.env

# 数据和日志（运行时产物）
data/
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 系统文件
.DS_Store
Thumbs.db
"""

FILES["requirements.txt"] = """\
# Web 框架
fastapi==0.104.1
uvicorn==0.24.0

# LangChain 核心
langchain==0.0.350
langchain-community==0.0.5
langchain-openai==0.0.2

# 向量数据库
chromadb==0.4.22

# 配置管理
pydantic-settings==2.1.0
python-dotenv==1.0.0

# 工具库
tenacity==8.2.3
python-multipart==0.0.6

# 可选：前端
# streamlit==1.29.0
# gradio==4.12.0
"""


# ============================================================
# 配置模块
# ============================================================

FILES["config/__init__.py"] = """\
\"\"\"配置模块，集中管理所有配置项。\"\"\"
from config.settings import settings

__all__ = ["settings"]
"""

FILES["config/settings.py"] = """\"\"\"
配置管理模块

使用 pydantic-settings 从环境变量和 .env 文件中读取配置。
所有配置项都集中在这里管理，其他模块通过 settings 对象访问。

用法：
    from config.settings import settings
    print(settings.openai_api_key)
\"\"\"

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    \"\"\"应用配置类，所有配置项都在这里定义。\"\"\"

    # ---- OpenAI 配置 ----
    openai_api_key: str = Field(
        default="sk-placeholder",
        description="OpenAI API Key"
    )
    openai_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="OpenAI API Base URL（兼容其他 LLM 服务）"
    )
    openai_model: str = Field(
        default="gpt-3.5-turbo",
        description="使用的模型名称"
    )

    # ---- Embedding 配置 ----
    embedding_model: str = Field(
        default="text-embedding-ada-002",
        description="Embedding 模型名称"
    )

    # ---- 向量数据库配置 ----
    chroma_persist_dir: str = Field(
        default="./data/chroma_db",
        description="Chroma 数据持久化目录"
    )
    collection_name: str = Field(
        default="rag_collection",
        description="向量集合名称"
    )

    # ---- 文档处理配置 ----
    chunk_size: int = Field(
        default=500,
        description="文档切分的 chunk 大小（token 数）"
    )
    chunk_overlap: int = Field(
        default=50,
        description="相邻 chunk 的重叠 token 数"
    )

    # ---- 检索配置 ----
    top_k: int = Field(
        default=3,
        description="检索返回的最相关文档数量"
    )

    # ---- 服务配置 ----
    host: str = Field(
        default="0.0.0.0",
        description="服务监听地址"
    )
    port: int = Field(
        default=8000,
        description="服务监听端口"
    )
    log_level: str = Field(
        default="INFO",
        description="日志级别"
    )

    class Config:
        \"\"\"pydantic-settings 的配置\"\"\"
        env_file = ".env"           # 从 .env 文件读取
        env_file_encoding = "utf-8"
        case_sensitive = False      # 环境变量名不区分大小写


# 全局单例：整个应用共享一个 settings 实例
settings = Settings()
"""


# ============================================================
# 工具模块
# ============================================================

FILES["src/__init__.py"] = '"""RAG 项目源代码包。"""\n'

FILES["src/utils/__init__.py"] = '"""工具函数模块。"""\n'

FILES["src/utils/logger.py"] = """\"\"\"
日志工具模块

提供统一的日志配置和获取方式。
所有模块通过 get_logger() 获取 logger 实例。

用法：
    from src.utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("文档加载完成")
\"\"\"

import logging
import os
from config.settings import settings


def setup_logging():
    \"\"\"初始化日志配置，在应用启动时调用一次。\"\"\"

    # 确保日志目录存在
    os.makedirs("logs", exist_ok=True)

    # 设置日志级别
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # 日志格式：时间 [级别] 模块名: 消息
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 文件输出
    file_handler = logging.FileHandler(
        "logs/app.log",
        encoding="utf-8",
        mode="a"  # 追加模式
    )
    file_handler.setFormatter(formatter)

    # 配置根 logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    \"\"\"
    获取 logger 实例。

    Args:
        name: 通常传入 __name__，用于标识日志来源

    Returns:
        logging.Logger 实例
    \"\"\"
    return logging.getLogger(name)
"""

FILES["src/utils/exceptions.py"] = """\"\"\"
自定义异常模块

定义 RAG 系统中各模块可能抛出的异常。
统一的异常体系让错误处理更清晰。

异常层级：
    RAGBaseException          # 基础异常
    ├── DocumentLoadError     # 文档加载失败
    ├── DocumentProcessError  # 文档处理（清洗/切分）失败
    ├── VectorStoreError      # 向量数据库操作失败
    ├── RetrievalError        # 检索失败
    └── GenerationError       # LLM 生成失败
\"\"\"


class RAGBaseException(Exception):
    \"\"\"RAG 系统基础异常，所有自定义异常都继承它。\"\"\"

    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self):
        if self.details:
            return f"{self.message} | 详情: {self.details}"
        return self.message


class DocumentLoadError(RAGBaseException):
    \"\"\"文档加载失败（文件不存在、格式不支持、读取错误等）。\"\"\"
    pass


class DocumentProcessError(RAGBaseException):
    \"\"\"文档处理失败（清洗、切分等步骤出错）。\"\"\"
    pass


class VectorStoreError(RAGBaseException):
    \"\"\"向量数据库操作失败（连接失败、写入失败等）。\"\"\"
    pass


class RetrievalError(RAGBaseException):
    \"\"\"检索失败（查询出错、返回结果异常等）。\"\"\"
    pass


class GenerationError(RAGBaseException):
    \"\"\"LLM 生成失败（API 调用超时、返回格式错误等）。\"\"\"
    pass
"""


# ============================================================
# 文档处理模块
# ============================================================

FILES["src/document_processing/__init__.py"] = '"""文档处理模块：加载、清洗、切分。"""\n'

FILES["src/document_processing/loader.py"] = """\"\"\"
文档加载器模块

负责将不同格式的文件加载为统一的 Document 对象。
后续会支持 txt、pdf、md 等多种格式。

用法：
    from src.document_processing.loader import DocumentLoader
    loader = DocumentLoader()
    docs = loader.load("data/raw/example.txt")
\"\"\"

from typing import List
from langchain.schema import Document
from src.utils.logger import get_logger
from src.utils.exceptions import DocumentLoadError

logger = get_logger(__name__)


class DocumentLoader:
    \"\"\"文档加载器，支持多种文件格式。\"\"\"

    def load(self, file_path: str) -> List[Document]:
        \"\"\"
        加载单个文件。

        Args:
            file_path: 文件路径

        Returns:
            Document 对象列表

        Raises:
            DocumentLoadError: 加载失败时抛出
        \"\"\"
        logger.info(f"开始加载文件: {file_path}")

        try:
            # TODO: 根据文件扩展名选择不同的加载器
            # 这里先用简单的文本读取作为占位
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            doc = Document(
                page_content=content,
                metadata={"source": file_path}
            )
            logger.info(f"文件加载成功: {file_path}，共 {len(content)} 字符")
            return [doc]

        except Exception as e:
            logger.error(f"文件加载失败: {file_path}, 错误: {e}")
            raise DocumentLoadError(f"加载文件失败: {file_path}", {"error": str(e)})

    def load_directory(self, directory: str) -> List[Document]:
        \"\"\"
        加载目录下的所有文件。

        Args:
            directory: 目录路径

        Returns:
            所有文件的 Document 对象列表
        \"\"\"
        import os

        logger.info(f"开始加载目录: {directory}")
        all_docs = []

        for root, _, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                try:
                    docs = self.load(file_path)
                    all_docs.extend(docs)
                except DocumentLoadError:
                    logger.warning(f"跳过无法加载的文件: {file_path}")

        logger.info(f"目录加载完成，共 {len(all_docs)} 个文档")
        return all_docs
"""

FILES["src/document_processing/splitter.py"] = """\"\"\"
文档切分模块

负责将长文档切成小块（chunk），方便后续向量化和检索。
切分策略影响检索质量，是 RAG 系统的关键环节。

类比：把一本书拆成一张张卡片，每张卡片记录一个知识点。
\"\"\"

from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DocumentSplitter:
    \"\"\"文档切分器，将长文档切成小块。\"\"\"

    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None
    ):
        \"\"\"
        初始化切分器。

        Args:
            chunk_size: 每个 chunk 的最大字符数，默认从配置读取
            chunk_overlap: 相邻 chunk 的重叠字符数，默认从配置读取
        \"\"\"
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\\n\\n", "\\n", "。", "！", "？", ".", " ", ""]
        )

        logger.info(
            f"切分器初始化完成: chunk_size={self.chunk_size}, "
            f"overlap={self.chunk_overlap}"
        )

    def split(self, documents: List[Document]) -> List[Document]:
        \"\"\"
        切分文档列表。

        Args:
            documents: 原始 Document 列表

        Returns:
            切分后的 Document 列表（每个 chunk 是一个 Document）
        \"\"\"
        logger.info(f"开始切分 {len(documents)} 个文档")

        chunks = self._splitter.split_documents(documents)

        logger.info(
            f"切分完成: {len(documents)} 个文档 → {len(chunks)} 个 chunks"
        )
        return chunks
"""

FILES["src/document_processing/cleaner.py"] = """\"\"\"
文档清洗模块

负责在切分前对文档内容进行清洗：
- 去除多余空白字符
- 去除特殊控制字符
- 标准化文本格式

类比：洗菜——把烂叶子摘掉、泥沙洗干净，再送去切。
\"\"\"

import re
from typing import List
from langchain.schema import Document
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DocumentCleaner:
    \"\"\"文档清洗器。\"\"\"

    def clean(self, documents: List[Document]) -> List[Document]:
        \"\"\"
        清洗文档列表。

        Args:
            documents: 原始 Document 列表

        Returns:
            清洗后的 Document 列表
        \"\"\"
        logger.info(f"开始清洗 {len(documents)} 个文档")
        cleaned_docs = []

        for doc in documents:
            cleaned_content = self._clean_text(doc.page_content)
            if cleaned_content.strip():  # 跳过清洗后为空的文档
                cleaned_doc = Document(
                    page_content=cleaned_content,
                    metadata=doc.metadata.copy()
                )
                cleaned_docs.append(cleaned_doc)

        logger.info(f"清洗完成: {len(documents)} → {len(cleaned_docs)} 个文档")
        return cleaned_docs

    def _clean_text(self, text: str) -> str:
        \"\"\"
        清洗单段文本。

        Args:
            text: 原始文本

        Returns:
            清洗后的文本
        \"\"\"
        # 1. 去除控制字符（保留换行和制表符）
        text = re.sub(r'[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]', '', text)

        # 2. 将多个连续空格替换为单个空格
        text = re.sub(r' +', ' ', text)

        # 3. 将多个连续换行替换为两个换行（保留段落分隔）
        text = re.sub(r'\\n{3,}', '\\n\\n', text)

        # 4. 去除每行首尾空白
        lines = [line.strip() for line in text.split('\\n')]
        text = '\\n'.join(lines)

        return text.strip()
"""


# ============================================================
# 向量存储模块
# ============================================================

FILES["src/vector_store/__init__.py"] = '"""向量存储模块：管理向量数据库。"""\n'

FILES["src/vector_store/store.py"] = """\"\"\"
向量存储模块

封装 Chroma 向量数据库的操作，提供统一的接口。
支持添加文档、相似度搜索、删除等操作。

类比：这是一个智能书架，你放书进去（add），告诉它你想找什么（search），
它就帮你找出最相关的几本书。
\"\"\"

from typing import List, Optional
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from config.settings import settings
from src.utils.logger import get_logger
from src.utils.exceptions import VectorStoreError

logger = get_logger(__name__)


class VectorStore:
    \"\"\"Chroma 向量数据库封装。\"\"\"

    def __init__(self):
        \"\"\"初始化向量存储。\"\"\"
        try:
            self._embeddings = OpenAIEmbeddings(
                model=settings.embedding_model,
                openai_api_key=settings.openai_api_key,
                openai_api_base=settings.openai_base_url,
            )

            self._store = Chroma(
                collection_name=settings.collection_name,
                embedding_function=self._embeddings,
                persist_directory=settings.chroma_persist_dir,
            )

            logger.info(
                f"向量存储初始化完成: "
                f"目录={settings.chroma_persist_dir}, "
                f"集合={settings.collection_name}"
            )
        except Exception as e:
            logger.error(f"向量存储初始化失败: {e}")
            raise VectorStoreError("向量存储初始化失败", {"error": str(e)})

    def add_documents(self, documents: List[Document]) -> List[str]:
        \"\"\"
        添加文档到向量存储。

        Args:
            documents: Document 列表

        Returns:
            添加的文档 ID 列表
        \"\"\"
        try:
            logger.info(f"开始添加 {len(documents)} 个文档到向量存储")
            ids = self._store.add_documents(documents)
            logger.info(f"文档添加成功，共 {len(ids)} 个")
            return ids
        except Exception as e:
            logger.error(f"文档添加失败: {e}")
            raise VectorStoreError("文档添加失败", {"error": str(e)})

    def search(self, query: str, top_k: int = None) -> List[Document]:
        \"\"\"
        相似度搜索。

        Args:
            query: 查询文本
            top_k: 返回结果数量，默认从配置读取

        Returns:
            最相关的 Document 列表
        \"\"\"
        k = top_k or settings.top_k
        try:
            logger.info(f"检索: query='{query[:50]}...', top_k={k}")
            results = self._store.similarity_search(query, k=k)
            logger.info(f"检索到 {len(results)} 个相关文档")
            return results
        except Exception as e:
            logger.error(f"检索失败: {e}")
            raise VectorStoreError("检索失败", {"error": str(e)})

    def delete(self, ids: List[str]) -> None:
        \"\"\"
        删除指定 ID 的文档。

        Args:
            ids: 要删除的文档 ID 列表
        \"\"\"
        try:
            self._store.delete(ids)
            logger.info(f"已删除 {len(ids)} 个文档")
        except Exception as e:
            logger.error(f"删除失败: {e}")
            raise VectorStoreError("删除失败", {"error": str(e)})

    def get_count(self) -> int:
        \"\"\"获取向量存储中的文档数量。\"\"\"
        try:
            collection = self._store._collection
            return collection.count()
        except Exception:
            return -1
"""


# ============================================================
# 检索模块
# ============================================================

FILES["src/retrieval/__init__.py"] = '"""检索模块：从向量数据库中检索相关文档。"""\n'

FILES["src/retrieval/retriever.py"] = """\"\"\"
检索器模块

封装检索逻辑，支持多种检索策略。
目前支持基本相似度检索，后续可扩展 MMR、混合检索等。

类比：图书管理员，听到你的问题后，去书架上找最相关的几本书。
\"\"\"

from typing import List
from langchain.schema import Document
from src.vector_store.store import VectorStore
from src.utils.logger import get_logger
from src.utils.exceptions import RetrievalError

logger = get_logger(__name__)


class Retriever:
    \"\"\"检索器，封装各种检索策略。\"\"\"

    def __init__(self, vector_store: VectorStore):
        \"\"\"
        初始化检索器。

        Args:
            vector_store: 向量存储实例
        \"\"\"
        self._vector_store = vector_store
        logger.info("检索器初始化完成")

    def retrieve(self, query: str, top_k: int = None) -> List[Document]:
        \"\"\"
        基本相似度检索。

        Args:
            query: 用户问题
            top_k: 返回数量

        Returns:
            最相关的文档列表
        \"\"\"
        try:
            logger.info(f"开始检索: {query[:50]}...")
            results = self._vector_store.search(query, top_k=top_k)
            logger.info(f"检索完成，返回 {len(results)} 个文档")
            return results
        except Exception as e:
            logger.error(f"检索失败: {e}")
            raise RetrievalError("检索失败", {"query": query, "error": str(e)})
"""


# ============================================================
# 生成模块
# ============================================================

FILES["src/generation/__init__.py"] = '"""生成模块：调用 LLM 生成回答。"""\n'

FILES["src/generation/generator.py"] = """\"\"\"
生成器模块

负责将检索到的文档和用户问题组装成 Prompt，调用 LLM 生成回答。
支持自定义 Prompt 模板。

类比：专家拿到管理员找来的资料后，写出一份通俗易懂的报告。
\"\"\"

from typing import List
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config.settings import settings
from src.utils.logger import get_logger
from src.utils.exceptions import GenerationError

logger = get_logger(__name__)

# 默认 Prompt 模板
DEFAULT_PROMPT_TEMPLATE = \"\"\"你是一个知识库助手。请根据以下参考资料回答用户的问题。

要求：
1. 只根据参考资料回答，不要编造信息
2. 如果参考资料中没有相关信息，请如实说明"根据现有资料，我无法回答这个问题"
3. 回答要简洁、准确、有条理

参考资料：
{context}

用户问题：{question}

请回答：\"\"\"


class Generator:
    \"\"\"LLM 回答生成器。\"\"\"

    def __init__(self, prompt_template: str = None):
        \"\"\"
        初始化生成器。

        Args:
            prompt_template: 自定义 Prompt 模板，包含 {context} 和 {question} 占位符
        \"\"\"
        self._llm = ChatOpenAI(
            model=settings.openai_model,
            openai_api_key=settings.openai_api_key,
            openai_api_base=settings.openai_base_url,
            temperature=0.3,  # 低温度，回答更稳定
        )

        self._prompt_template = prompt_template or DEFAULT_PROMPT_TEMPLATE
        self._prompt = ChatPromptTemplate.from_template(self._prompt_template)

        logger.info(f"生成器初始化完成，模型: {settings.openai_model}")

    def generate(self, question: str, context_docs: List[Document]) -> str:
        \"\"\"
        根据问题和参考资料生成回答。

        Args:
            question: 用户问题
            context_docs: 检索到的参考文档列表

        Returns:
            LLM 生成的回答文本
        \"\"\"
        try:
            # 1. 把文档内容拼接成上下文字符串
            context = "\\n\\n---\\n\\n".join(
                [doc.page_content for doc in context_docs]
            )

            logger.info(
                f"开始生成回答: 问题='{question[:50]}...', "
                f"参考资料={len(context_docs)} 个文档"
            )

            # 2. 构造 Prompt
            messages = self._prompt.format_messages(
                context=context,
                question=question
            )

            # 3. 调用 LLM
            response = self._llm.invoke(messages)
            answer = response.content

            logger.info(f"回答生成完成，长度: {len(answer)} 字符")
            return answer

        except Exception as e:
            logger.error(f"回答生成失败: {e}")
            raise GenerationError("回答生成失败", {"error": str(e)})
"""


# ============================================================
# API 模块
# ============================================================

FILES["src/api/__init__.py"] = '"""API 路由模块。"""\n'

FILES["src/api/query.py"] = """\"\"\"
查询 API 路由

提供用户提问的 HTTP 接口。
\"\"\"

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/query", tags=["查询"])


class QueryRequest(BaseModel):
    \"\"\"查询请求体\"\"\"
    question: str       # 用户问题
    top_k: int = 3      # 检索数量


class QueryResponse(BaseModel):
    \"\"\"查询响应体\"\"\"
    answer: str         # 回答内容
    sources: list = []  # 来源信息


@router.post("/", response_model=QueryResponse)
async def query(request: QueryRequest):
    \"\"\"
    用户提问接口。

    接收用户问题，检索相关文档，生成回答并返回。
    \"\"\"
    logger.info(f"收到查询请求: {request.question[:50]}...")

    try:
        # TODO: 实际实现——注入 retriever 和 generator
        # 1. 检索相关文档
        # docs = retriever.retrieve(request.question, top_k=request.top_k)
        # 2. 生成回答
        # answer = generator.generate(request.question, docs)

        # 占位返回
        return QueryResponse(
            answer="这是占位回答，后续接入实际的 RAG 管道。",
            sources=[]
        )
    except Exception as e:
        logger.error(f"查询处理失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
"""

FILES["src/api/upload.py"] = """\"\"\"
文档上传 API 路由

提供文档上传和入库的 HTTP 接口。
\"\"\"

from fastapi import APIRouter, UploadFile, File, HTTPException
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/upload", tags=["上传"])


@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    \"\"\"
    上传文档接口。

    接收上传的文件，保存到 data/raw/ 目录，然后触发入库流程。
    \"\"\"
    logger.info(f"收到文件上传: {file.filename}")

    try:
        # 1. 保存文件
        import os
        os.makedirs("data/raw", exist_ok=True)
        file_path = f"data/raw/{file.filename}"

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        logger.info(f"文件已保存: {file_path}")

        # TODO: 2. 触发入库流程（加载→清洗→切分→向量化→存储）

        return {
            "message": f"文件 {file.filename} 上传成功",
            "file_path": file_path
        }
    except Exception as e:
        logger.error(f"文件上传失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
"""


# ============================================================
# 应用入口
# ============================================================

FILES["src/main.py"] = """\"\"\"
应用入口

启动 FastAPI 服务，注册所有路由。
这是整个 RAG 系统的"总开关"。

用法：
    python -m src.main
    或
    uvicorn src.main:app --reload
\"\"\"

from fastapi import FastAPI
from src.utils.logger import setup_logging, get_logger
from src.api.query import router as query_router
from src.api.upload import router as upload_router
from config.settings import settings

# 初始化日志
setup_logging()
logger = get_logger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="RAG 知识库问答系统",
    description="基于检索增强生成的智能问答系统",
    version="1.0.0"
)

# 注册路由
app.include_router(query_router)
app.include_router(upload_router)


@app.get("/")
async def root():
    \"\"\"首页，返回系统信息。\"\"\"
    return {
        "system": "RAG 知识库问答系统",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    \"\"\"健康检查接口。\"\"\"
    return {"status": "healthy"}


# 启动事件
@app.on_event("startup")
async def startup():
    logger.info("RAG 系统启动中...")
    logger.info(f"模型: {settings.openai_model}")
    logger.info(f"向量数据库: {settings.chroma_persist_dir}")
    logger.info("RAG 系统启动完成!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
"""


# ============================================================
# 测试文件
# ============================================================

FILES["tests/__init__.py"] = '"""测试代码包。"""\n'

FILES["tests/test_loader.py"] = """\"\"\"
文档加载器测试

测试 DocumentLoader 的基本功能。
\"\"\"

import os
import tempfile
from src.document_processing.loader import DocumentLoader


def test_load_text_file():
    \"\"\"测试加载文本文件。\"\"\"
    # 创建临时文件
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.txt', delete=False, encoding='utf-8'
    ) as f:
        f.write("这是一个测试文档的内容。\\n用于验证加载器是否正常工作。")
        temp_path = f.name

    try:
        loader = DocumentLoader()
        docs = loader.load(temp_path)
        assert len(docs) == 1
        assert "测试文档" in docs[0].page_content
        assert docs[0].metadata["source"] == temp_path
        print("✓ 测试通过: 文本文件加载正常")
    finally:
        os.unlink(temp_path)


if __name__ == "__main__":
    test_load_text_file()
    print("所有测试通过!")
"""


# ============================================================
# 主函数：创建项目结构
# ============================================================

def create_project():
    """创建完整的项目目录结构和文件。"""

    base_path = os.path.join(os.getcwd(), PROJECT_NAME)

    print(f"{'='*60}")
    print(f"  创建 RAG 项目: {PROJECT_NAME}")
    print(f"{'='*60}")

    # 创建目录
    print("\n[1/3] 创建目录结构...")
    for directory in DIRECTORIES:
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"  📁 {directory}/")

    # 创建文件
    print("\n[2/3] 生成文件...")
    for file_path, content in FILES.items():
        full_path = os.path.join(base_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  📄 {file_path}")

    # 打印目录树
    print(f"\n[3/3] 项目结构:")
    print(f"  {PROJECT_NAME}/")
    print_tree(base_path, "  ")

    print(f"\n{'='*60}")
    print("  项目创建完成!")
    print(f"{'='*60}")
    print(f"""
  下一步操作:
  1. cd {PROJECT_NAME}
  2. 复制 .env.example 为 .env，填入你的 API Key
  3. pip install -r requirements.txt
  4. python -m src.main
  5. 打开 http://localhost:8000/docs 查看 API 文档
""")


def print_tree(base_path, prefix=""):
    """打印目录树。"""
    entries = sorted(os.listdir(base_path))
    for i, entry in enumerate(entries):
        entry_path = os.path.join(base_path, entry)
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "

        if os.path.isdir(entry_path):
            print(f"{prefix}{connector}{entry}/")
            extension = "    " if is_last else "│   "
            print_tree(entry_path, prefix + extension)
        else:
            print(f"{prefix}{connector}{entry}")


if __name__ == "__main__":
    create_project()
