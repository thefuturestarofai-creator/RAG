"""
Demo 2: 部署脚本

本 Demo 提供两部分内容：
1. Python 脚本模拟部署流程（不需要 Docker）
2. 实际的 Dockerfile 和 docker-compose.yml 文件

用法：
    python 2_demo_deploy_script.py

不需要 API Key（只是模拟和生成配置文件）。
"""

import os
import time
import json


# ============================================================
# 第一部分：模拟部署流程
# ============================================================

class DeploySimulator:
    """部署流程模拟器。"""

    def __init__(self, project_name: str = "rag-system"):
        self.project_name = project_name
        self.steps = []
        self.current_step = 0

    def add_step(self, name: str, duration: float = 1.0):
        """添加部署步骤。"""
        self.steps.append({"name": name, "duration": duration})

    def run(self):
        """运行部署流程。"""
        print(f"\n{'='*60}")
        print(f"  开始部署: {self.project_name}")
        print(f"{'='*60}")

        total_steps = len(self.steps)
        start_time = time.time()

        for i, step in enumerate(self.steps, 1):
            self.current_step = i
            print(f"\n[{i}/{total_steps}] {step['name']}")
            print("  " + "." * 40, end="", flush=True)

            # 模拟执行时间
            for _ in range(10):
                time.sleep(step['duration'] / 10)
                print(".", end="", flush=True)

            print(" ✓ 完成!")

        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"  部署完成! 耗时: {elapsed:.1f} 秒")
        print(f"{'='*60}")


def simulate_deployment():
    """模拟完整的部署流程。"""

    print("\n" + "=" * 60)
    print("  模拟部署流程（不需要 Docker）")
    print("=" * 60)

    deployer = DeploySimulator("RAG 知识库问答系统")

    # 添加部署步骤
    deployer.add_step("检查环境配置 (.env 文件)", 0.5)
    deployer.add_step("检查 Docker 和 Docker Compose 版本", 0.3)
    deployer.add_step("拉取最新代码 (git pull)", 0.8)
    deployer.add_step("构建 RAG 应用镜像 (docker build)", 2.0)
    deployer.add_step("拉取 ChromaDB 镜像 (docker pull)", 1.5)
    deployer.add_step("停止旧容器 (docker-compose down)", 0.5)
    deployer.add_step("创建数据卷", 0.2)
    deployer.add_step("启动 ChromaDB 服务", 0.8)
    deployer.add_step("等待 ChromaDB 健康检查通过", 1.0)
    deployer.add_step("启动 RAG 应用服务", 0.8)
    deployer.add_step("等待 RAG 应用健康检查通过", 1.0)
    deployer.add_step("验证服务状态", 0.5)

    deployer.run()

    # 显示部署结果
    print("\n部署结果:")
    print(f"  RAG 应用: http://localhost:8000")
    print(f"  API 文档: http://localhost:8000/docs")
    print(f"  ChromaDB: http://localhost:8001")


# ============================================================
# 第二部分：生成实际的部署文件
# ============================================================

DOCKERFILE = """\
# ============================================================
# RAG 应用 Dockerfile - 生产版本
# ============================================================

FROM python:3.11-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 安装系统依赖
RUN apt-get update && \\
    apt-get install -y --no-install-recommends curl && \\
    rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY src/ ./src/
COPY config/ ./config/

# 创建必要目录
RUN mkdir -p /app/data/raw /app/data/chroma_db /app/logs

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \\
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

DOCKER_COMPOSE = """\
# ============================================================
# RAG 系统 Docker Compose 配置 - 生产版本
# ============================================================

version: "3.8"

services:
  rag-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: rag-app
    ports:
      - "${APP_PORT:-8000}:8000"
    env_file:
      - .env
    environment:
      - CHROMA_HOST=chromadb
      - CHROMA_PORT=8000
    volumes:
      - ./data:/app/data
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
    networks:
      - rag-network

  chromadb:
    image: chromadb/chroma:latest
    container_name: chromadb
    ports:
      - "${CHROMA_PORT:-8001}:8000"
    volumes:
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
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1.0"
    networks:
      - rag-network

volumes:
  chroma_data:
    driver: local

networks:
  rag-network:
    driver: bridge
"""

DEPLOY_SCRIPT = """\
#!/bin/bash
# ============================================================
# RAG 系统部署脚本
# ============================================================

set -e

echo "=========================================="
echo "  RAG 系统部署脚本"
echo "=========================================="

# 颜色定义
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m'

# 检查 .env 文件
echo ""
echo "[1/6] 检查配置文件..."
if [ ! -f .env ]; then
    echo -e "${RED}错误: .env 文件不存在${NC}"
    echo "请先复制 .env.example 为 .env 并填入配置"
    exit 1
fi
echo -e "${GREEN}  ✓ .env 文件存在${NC}"

# 检查 Docker
echo ""
echo "[2/6] 检查 Docker 环境..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装${NC}"
    exit 1
fi
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: Docker Compose 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Docker 环境正常${NC}"

# 拉取最新代码
echo ""
echo "[3/6] 拉取最新代码..."
git pull origin main || echo -e "${YELLOW}  ⚠ git pull 失败，使用本地代码继续${NC}"

# 构建镜像
echo ""
echo "[4/6] 构建 Docker 镜像..."
docker-compose build

# 停止旧容器
echo ""
echo "[5/6] 停止旧容器..."
docker-compose down

# 启动服务
echo ""
echo "[6/6] 启动服务..."
docker-compose up -d

# 等待服务就绪
echo ""
echo "等待服务启动..."
sleep 10

# 检查状态
echo ""
echo "=========================================="
echo "  部署状态"
echo "=========================================="
docker-compose ps

# 健康检查
echo ""
echo "健康检查..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}  ✓ RAG 应用运行正常${NC}"
else
    echo -e "${YELLOW}  ⚠ RAG 应用可能还在启动中${NC}"
fi

echo ""
echo "=========================================="
echo -e "  ${GREEN}部署完成!${NC}"
echo "  RAG 应用: http://localhost:8000"
echo "  API 文档: http://localhost:8000/docs"
echo "=========================================="
"""

ENV_EXAMPLE = """\
# RAG 系统环境变量配置
# 复制此文件为 .env 并填入实际值

# OpenAI 配置
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# 端口配置
APP_PORT=8000
CHROMA_PORT=8001

# 日志级别
LOG_LEVEL=INFO
"""


def generate_deploy_files():
    """生成部署相关的所有文件。"""

    output_dir = os.path.join(os.path.dirname(__file__), "deploy_output")
    os.makedirs(output_dir, exist_ok=True)

    files = {
        "Dockerfile": DOCKERFILE,
        "docker-compose.yml": DOCKER_COMPOSE,
        "deploy.sh": DEPLOY_SCRIPT,
        ".env.example": ENV_EXAMPLE,
    }

    print("\n" + "=" * 60)
    print("  生成部署文件")
    print("=" * 60)

    for filename, content in files.items():
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ {filename}")

    # deploy.sh 设置可执行权限（Linux/Mac）
    try:
        os.chmod(os.path.join(output_dir, "deploy.sh"), 0o755)
    except Exception:
        pass  # Windows 下可能失败，忽略

    return output_dir


# ============================================================
# 第三部分：展示部署架构
# ============================================================

def show_architecture():
    """展示部署架构图。"""

    print("\n" + "=" * 60)
    print("  部署架构")
    print("=" * 60)

    print("""
  ┌─────────────────────────────────────────────┐
  │                  宿主机                      │
  │                                              │
  │   ┌──────────────┐    ┌──────────────┐      │
  │   │   rag-app    │    │   chromadb   │      │
  │   │  (FastAPI)   │───>│ (向量数据库)  │      │
  │   │  端口: 8000  │    │  端口: 8000  │      │
  │   └──────┬───────┘    └──────┬───────┘      │
  │          │                   │               │
  │   ┌──────┴───────┐    ┌──────┴───────┐      │
  │   │   data/      │    │ chroma_data  │      │
  │   │   logs/      │    │   (volume)   │      │
  │   └──────────────┘    └──────────────┘      │
  │                                              │
  │   Docker Network: rag-network                │
  └─────────────────────────────────────────────┘

  数据流:
  用户 → 8000 → rag-app → chromadb:8000 → 向量检索
                 ↓
              OpenAI API → LLM 生成回答
    """)


# ============================================================
# 主函数
# ============================================================

def main():
    print("=" * 60)
    print("  Demo 2: 部署脚本")
    print("=" * 60)

    # 展示架构
    show_architecture()

    # 模拟部署
    simulate_deployment()

    # 生成实际文件
    output_dir = generate_deploy_files()

    print("\n" + "=" * 60)
    print("  总结")
    print("=" * 60)
    print(f"""
  本 Demo 提供了:

  1. 部署流程模拟
     - 不需要 Docker 环境
     - 展示完整的 12 步部署流程
     - 了解每一步的作用

  2. 实际部署文件
     - Dockerfile: 应用镜像定义
     - docker-compose.yml: 服务编排
     - deploy.sh: 一键部署脚本
     - .env.example: 配置模板

  文件位置: {output_dir}/

  实际部署步骤:
  1. cd {output_dir}
  2. cp .env.example .env
  3. 编辑 .env 填入 API Key
  4. chmod +x deploy.sh  (Linux/Mac)
  5. ./deploy.sh
    """)


if __name__ == "__main__":
    main()
