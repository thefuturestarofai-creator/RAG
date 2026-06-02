"""
Demo 1: docker-compose.yml 编排

本 Demo 生成一个完整的 Docker Compose 配置文件，用于编排：
1. FastAPI RAG 服务
2. ChromaDB 向量数据库

同时生成配套的 Dockerfile 和 .env 文件。

用法：
    python 1_demo_docker_compose.py

不需要 API Key（只是生成配置文件）。
"""

import os


# ============================================================
# 生成的文件内容
# ============================================================

DOCKERFILE_CONTENT = """\
# ============================================================
# RAG 应用 Dockerfile
# ============================================================

# 使用 Python 3.11 slim 镜像（体积小）
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件（利用 Docker 缓存层）
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY src/ ./src/
COPY config/ ./config/

# 创建数据和日志目录
RUN mkdir -p /app/data /app/logs

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \\
    chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

DOCKER_COMPOSE_CONTENT = """\
# ============================================================
# Docker Compose 配置
# RAG 知识库问答系统
# ============================================================
#
# 使用方法:
#   启动: docker-compose up -d
#   停止: docker-compose down
#   查看日志: docker-compose logs -f rag-app
#   重新构建: docker-compose up -d --build
#
# ============================================================

version: "3.8"

services:
  # ---- RAG 应用服务 ----
  rag-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: rag-app
    ports:
      - "${APP_PORT:-8000}:8000"
    environment:
      # 从 .env 文件读取敏感配置
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_BASE_URL=${OPENAI_BASE_URL:-https://api.openai.com/v1}
      - OPENAI_MODEL=${OPENAI_MODEL:-gpt-3.5-turbo}
      # ChromaDB 连接配置（使用服务名作为主机名）
      - CHROMA_HOST=chromadb
      - CHROMA_PORT=8000
      # 日志级别
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    volumes:
      # 挂载数据目录（文档和向量数据）
      - ./data:/app/data
      # 挂载日志目录
      - ./logs:/app/logs
    depends_on:
      chromadb:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"
        reservations:
          memory: 512M
          cpus: "0.5"

  # ---- ChromaDB 向量数据库 ----
  chromadb:
    image: chromadb/chroma:latest
    container_name: chromadb
    ports:
      # 映射到 8001 避免与 rag-app 冲突
      - "${CHROMA_PORT:-8001}:8000"
    volumes:
      # 数据持久化
      - chroma_data:/chroma/chroma
    environment:
      - IS_PERSISTENT=TRUE
      - ANONYMIZED_TELEMETRY=FALSE
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1.0"

# ---- 数据卷定义 ----
volumes:
  chroma_data:
    driver: local
"""

ENV_CONTENT = """\
# ============================================================
# 环境变量配置
# 复制此文件为 .env 并填入实际值
# ============================================================

# OpenAI 配置
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# 应用端口
APP_PORT=8000

# ChromaDB 端口（宿主机映射）
CHROMA_PORT=8001

# 日志级别: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO
"""

REQUIREMENTS_TXT = """\
# Web 框架
fastapi==0.104.1
uvicorn==0.24.0

# LangChain
langchain==0.0.350
langchain-community==0.0.5
langchain-openai==0.0.2

# 向量数据库客户端
chromadb==0.4.22

# 配置管理
pydantic-settings==2.1.0
python-dotenv==1.0.0

# 工具库
tenacity==8.2.3
python-multipart==0.0.6
"""


# ============================================================
# 生成文件
# ============================================================

def generate_files():
    """生成所有 Docker 相关的配置文件。"""

    output_dir = os.path.join(os.path.dirname(__file__), "docker_output")
    os.makedirs(output_dir, exist_ok=True)

    files = {
        "Dockerfile": DOCKERFILE_CONTENT,
        "docker-compose.yml": DOCKER_COMPOSE_CONTENT,
        ".env.example": ENV_CONTENT,
        "requirements.txt": REQUIREMENTS_TXT,
    }

    print("=" * 60)
    print("  Docker Compose 配置生成器")
    print("=" * 60)

    print(f"\n输出目录: {output_dir}\n")

    for filename, content in files.items():
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ 已生成: {filename}")

    return output_dir


# ============================================================
# 展示配置说明
# ============================================================

def explain_config():
    """解释各个配置文件的作用。"""

    print("\n" + "=" * 60)
    print("  配置文件说明")
    print("=" * 60)

    print("""
  1. Dockerfile
     作用: 定义 RAG 应用的 Docker 镜像
     关键点:
     - 使用 python:3.11-slim 基础镜像（体积小）
     - 先复制 requirements.txt 再安装（利用缓存）
     - 创建非 root 用户运行（安全）
     - 添加健康检查

  2. docker-compose.yml
     作用: 编排 rag-app 和 chromadb 两个服务
     关键点:
     - rag-app 依赖 chromadb（depends_on）
     - chromadb 有健康检查（service_healthy）
     - 数据通过 volumes 持久化
     - 环境变量从 .env 文件读取
     - 资源限制防止资源耗尽

  3. .env.example
     作用: 环境变量模板
     使用: 复制为 .env 并填入实际的 API Key

  4. requirements.txt
     作用: Python 依赖列表
    """)


def explain_commands():
    """展示常用命令。"""

    print("=" * 60)
    print("  常用命令")
    print("=" * 60)

    print("""
  # 首次部署
  1. cp .env.example .env          # 创建配置文件
  2. 编辑 .env，填入 API Key
  3. docker-compose up -d --build   # 构建并启动

  # 日常操作
  docker-compose ps                 # 查看状态
  docker-compose logs -f rag-app    # 查看日志
  docker-compose restart rag-app    # 重启服务
  docker-compose down               # 停止所有服务

  # 更新部署
  git pull                          # 拉取新代码
  docker-compose up -d --build      # 重新构建并启动

  # 数据管理
  docker-compose exec chromadb ls /chroma/chroma  # 查看向量数据
  docker-compose down -v            # 停止并删除所有数据（谨慎!）
    """)


# ============================================================
# 主函数
# ============================================================

def main():
    # 生成文件
    output_dir = generate_files()

    # 展示说明
    explain_config()
    explain_commands()

    print("=" * 60)
    print("  生成完成!")
    print("=" * 60)
    print(f"""
  文件已生成到: {output_dir}/

  下一步:
  1. 进入输出目录: cd {output_dir}
  2. 复制配置文件: cp .env.example .env
  3. 编辑 .env，填入你的 API Key
  4. 启动服务: docker-compose up -d --build
  5. 访问: http://localhost:8000
    """)


if __name__ == "__main__":
    main()
