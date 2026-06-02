"""
Demo 2: 配置管理 - 使用 pydantic-settings

本 Demo 演示如何用 pydantic-settings 管理项目配置：
1. 从 .env 文件读取配置
2. 支持环境变量覆盖
3. 配置项的类型验证和默认值
4. 分组管理不同模块的配置

用法：
    python 2_demo_config_management.py

不需要 API Key，但会展示 API Key 的配置方式。
"""

import os
import tempfile


# ============================================================
# 第一步：创建示例 .env 文件
# ============================================================

def create_sample_env():
    """创建一个示例 .env 文件，演示各种配置项。"""

    env_content = """\
# ============================================================
# RAG 项目配置文件
# ============================================================

# ---- LLM 配置 ----
OPENAI_API_KEY=sk-demo-key-12345
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
TEMPERATURE=0.3

# ---- Embedding 配置 ----
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_DIMENSIONS=1536

# ---- 向量数据库配置 ----
CHROMA_PERSIST_DIR=./data/chroma_db
COLLECTION_NAME=my_rag_collection

# ---- 文档处理配置 ----
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# ---- 检索配置 ----
TOP_K=3
SEARCH_TYPE=similarity

# ---- 服务配置 ----
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
DEBUG=false
"""

    env_path = os.path.join(os.getcwd(), ".env.example_demo")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)

    print(f"✓ 已创建示例 .env 文件: {env_path}")
    return env_path


# ============================================================
# 第二步：定义配置类
# ============================================================

# 注意：这里为了演示，我们不依赖 pydantic-settings 的实际安装
# 而是用代码模拟其行为，同时展示 pydantic-settings 的写法

print("=" * 60)
print("  配置管理 Demo - pydantic-settings 用法演示")
print("=" * 60)

# 先创建 .env 文件
env_path = create_sample_env()


# ============================================================
# 第三步：演示 .env 文件的读取
# ============================================================

print("\n" + "=" * 60)
print("  方法一：使用 python-dotenv 手动读取 .env")
print("=" * 60)

# python-dotenv 可以把 .env 文件加载到环境变量中
try:
    from dotenv import load_dotenv

    # 加载 .env 文件到环境变量
    load_dotenv(env_path)

    # 读取配置
    config_from_dotenv = {
        "openai_api_key": os.getenv("OPENAI_API_KEY", "未设置"),
        "openai_base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        "chunk_size": int(os.getenv("CHUNK_SIZE", "500")),
        "top_k": int(os.getenv("TOP_K", "3")),
    }

    print("\n从 .env 文件读取到的配置:")
    for key, value in config_from_dotenv.items():
        # 隐藏 API Key 的中间部分
        if "key" in key.lower() and len(str(value)) > 10:
            display_value = value[:6] + "***" + value[-4:]
        else:
            display_value = value
        print(f"  {key}: {display_value}")

except ImportError:
    print("  python-dotenv 未安装，跳过此演示")
    print("  安装命令: pip install python-dotenv")


# ============================================================
# 第四步：展示 pydantic-settings 的标准写法
# ============================================================

print("\n" + "=" * 60)
print("  方法二：使用 pydantic-settings（推荐）")
print("=" * 60)

# 展示标准的 pydantic-settings 写法
print("""
# ---- 以下是 pydantic-settings 的标准写法 ----
# 文件位置: config/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    \"\"\"应用配置类\"\"\"

    # LLM 配置
    openai_api_key: str = Field(
        default="sk-placeholder",
        description="OpenAI API Key"
    )
    openai_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="API Base URL"
    )
    openai_model: str = Field(
        default="gpt-3.5-turbo",
        description="模型名称"
    )
    temperature: float = Field(
        default=0.3,
        ge=0.0,          # 最小值
        le=2.0,          # 最大值
        description="生成温度"
    )

    # 文档处理配置
    chunk_size: int = Field(
        default=500,
        gt=0,
        description="切分块大小"
    )
    chunk_overlap: int = Field(
        default=50,
        ge=0,
        description="重叠大小"
    )

    # 检索配置
    top_k: int = Field(
        default=3,
        gt=0,
        description="检索数量"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# 使用方式:
# from config.settings import settings
# print(settings.openai_model)
""")

# 尝试实际使用 pydantic-settings
try:
    from pydantic_settings import BaseSettings
    from pydantic import Field

    class Settings(BaseSettings):
        """应用配置类"""

        # LLM 配置
        openai_api_key: str = Field(default="sk-placeholder", description="OpenAI API Key")
        openai_base_url: str = Field(default="https://api.openai.com/v1", description="API Base URL")
        openai_model: str = Field(default="gpt-3.5-turbo", description="模型名称")
        temperature: float = Field(default=0.3, ge=0.0, le=2.0, description="生成温度")

        # 文档处理配置
        chunk_size: int = Field(default=500, gt=0, description="切分块大小")
        chunk_overlap: int = Field(default=50, ge=0, description="重叠大小")

        # 检索配置
        top_k: int = Field(default=3, gt=0, description="检索数量")

        class Config:
            env_file = env_path
            env_file_encoding = "utf-8"

    # 创建配置实例
    settings = Settings()

    print("\n✓ pydantic-settings 加载成功!")
    print("\n配置详情:")
    print(f"  openai_api_key:    {settings.openai_api_key[:6]}***")
    print(f"  openai_base_url:   {settings.openai_base_url}")
    print(f"  openai_model:      {settings.openai_model}")
    print(f"  temperature:       {settings.temperature}")
    print(f"  chunk_size:        {settings.chunk_size}")
    print(f"  chunk_overlap:     {settings.chunk_overlap}")
    print(f"  top_k:             {settings.top_k}")

    # 演示类型验证
    print("\n类型验证演示:")
    try:
        Settings(chunk_size="不是数字")  # 应该报错
    except Exception as e:
        print(f"  ✓ 输入非法值 '不是数字' 给 chunk_size: 验证失败（符合预期）")

    # 演示环境变量覆盖
    print("\n环境变量覆盖演示:")
    os.environ["OPENAI_MODEL"] = "gpt-4"
    settings2 = Settings()
    print(f"  设置环境变量 OPENAI_MODEL=gpt-4")
    print(f"  settings.openai_model = {settings2.openai_model}")
    print(f"  ✓ 环境变量优先级高于 .env 文件")

except ImportError:
    print("\n  pydantic-settings 未安装")
    print("  安装命令: pip install pydantic-settings")
    print("  但上面的代码展示了正确的用法")


# ============================================================
# 第五步：配置分组管理（高级用法）
# ============================================================

print("\n" + "=" * 60)
print("  高级用法：配置分组管理")
print("=" * 60)

print("""
# 当配置项很多时，可以按模块分组:

from pydantic import BaseModel

class LLMConfig(BaseModel):
    \"\"\"LLM 相关配置\"\"\"
    api_key: str = "sk-placeholder"
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.3

class VectorDBConfig(BaseModel):
    \"\"\"向量数据库相关配置\"\"\"
    persist_dir: str = "./data/chroma_db"
    collection_name: str = "rag_collection"

class RetrievalConfig(BaseModel):
    \"\"\"检索相关配置\"\"\"
    top_k: int = 3
    search_type: str = "similarity"

class Settings(BaseSettings):
    \"\"\"应用总配置\"\"\"
    llm: LLMConfig = LLMConfig()
    vector_db: VectorDBConfig = VectorDBConfig()
    retrieval: RetrievalConfig = RetrievalConfig()

    class Config:
        env_file = ".env"

# 使用: settings.llm.model, settings.vector_db.persist_dir
""")


# ============================================================
# 第六步：实际应用中的配置使用模式
# ============================================================

print("=" * 60)
print("  实际应用中的配置使用模式")
print("=" * 60)

print("""
最佳实践总结:

1. 单一来源：所有配置集中在 config/settings.py
2. 类型安全：用 pydantic 自动验证类型和范围
3. 环境优先：环境变量 > .env 文件 > 默认值
4. 安全存储：API Key 等敏感信息只放 .env，不入 Git
5. 文档化：Field 的 description 字段说明每个配置的用途

在代码中使用:
    from config.settings import settings

    # 创建 LLM
    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
    )

    # 创建切分器
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
""")


# ============================================================
# 清理临时文件
# ============================================================

# 清理演示用的 .env 文件
try:
    os.unlink(env_path)
    print(f"\n✓ 已清理临时文件: {env_path}")
except Exception:
    pass

# 清理环境变量
for key in ["OPENAI_MODEL"]:
    os.environ.pop(key, None)

print("\nDemo 运行完成!")
