"""
Demo 2: docker-compose 示例 - 编排 FastAPI + Chroma
===================================================

功能：
- 编写 docker-compose.yml 编排多个服务
- 演示服务之间的依赖关系和网络配置

前置条件：
- 不需要 Docker 和 API Key（本脚本用于教学说明）
- 如果要实际运行，需要安装 Docker 和 Docker Compose

对应理论：2.Docker实战.md
"""

import os

# ============================================================
# 第一部分：Docker Compose 概念说明
# ============================================================
print("=" * 60)
print("第一部分：Docker Compose 概念说明")
print("=" * 60)

print("""
Docker Compose 用于定义和运行多容器应用。

类比：
- Dockerfile = 单道菜的菜谱
- docker-compose.yml = 整桌宴席的菜单

在 RAG 系统中，通常需要多个服务协同工作：
1. API 服务（FastAPI）- 处理用户请求
2. 向量数据库（Chroma）- 存储和检索文档
3. 缓存服务（Redis）- 缓存频繁查询结果（可选）
""")


# ============================================================
# 第二部分：生成 docker-compose.yml
# ============================================================
print("\n" + "=" * 60)
print("第二部分：生成 docker-compose.yml")
print("=" * 60)

compose_content = '''# RAG 系统 Docker Compose 配置
# 服务：FastAPI API + Chroma 向量数据库

version: '3.8'

services:
  # ====== API 服务 ======
  api:
    # 从当前目录的 Dockerfile 构建
    build:
      context: .
      dockerfile: Dockerfile

    # 容器名称
    container_name: rag-api

    # 端口映射：宿主机端口:容器端口
    ports:
      - "8000:8000"

    # 环境变量
    environment:
      - API_KEY=${API_KEY}              # 从 .env 文件读取
      - BASE_URL=${BASE_URL}
      - MODEL=${MODEL}
      - CHROMA_HOST=chroma              # Chroma 服务名（Docker 内部网络）
      - CHROMA_PORT=8000

    # 数据卷挂载
    volumes:
      - ./app:/app/app                  # 挂载代码目录（开发环境）
      - ./data:/app/data                # 挂载数据目录

    # 依赖的服务（先启动 chroma）
    depends_on:
      chroma:
        condition: service_healthy      # 等待 Chroma 健康检查通过

    # 重启策略
    restart: unless-stopped

    # 网络
    networks:
      - rag-network

    # 健康检查
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ====== Chroma 向量数据库 ======
  chroma:
    # 使用官方镜像
    image: chromadb/chroma:latest

    # 容器名称
    container_name: rag-chroma

    # 端口映射
    ports:
      - "8001:8000"                     # 宿主机 8001 -> 容器 8000

    # 数据卷（持久化向量数据）
    volumes:
      - chroma_data:/chroma/chroma      # 命名卷

    # 重启策略
    restart: unless-stopped

    # 网络
    networks:
      - rag-network

    # 健康检查
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 10s
      timeout: 5s
      retries: 5

# ====== 网络定义 ======
networks:
  rag-network:
    driver: bridge                      # 桥接网络

# ====== 命名卷定义 ======
volumes:
  chroma_data:
    driver: local
'''

compose_path = "docker-compose.yml"
with open(compose_path, "w", encoding="utf-8") as f:
    f.write(compose_content)

print(f"已生成 docker-compose.yml：{compose_path}")
print("\n文件内容预览：")
print("-" * 40)
for i, line in enumerate(compose_content.strip().split('\n')[:30], 1):
    print(f"{i:2d} | {line}")
print("    ... (更多内容)")


# ============================================================
# 第三部分：生成 .env 文件模板
# ============================================================
print("\n" + "=" * 60)
print("第三部分：生成 .env 文件模板")
print("=" * 60)

env_content = '''# RAG 系统环境变量配置
# 复制此文件为 .env 并填写你的配置

# OpenAI API 配置
API_KEY=your-api-key-here
BASE_URL=https://api.openai.com/v1
MODEL=gpt-3.5-turbo

# Chroma 配置
CHROMA_HOST=chroma
CHROMA_PORT=8000
'''

env_path = ".env.example"
with open(env_path, "w", encoding="utf-8") as f:
    f.write(env_content)

print(f"已生成 .env.example：{env_path}")


# ============================================================
# 第四部分：Docker Compose 命令说明
# ============================================================
print("\n" + "=" * 60)
print("第四部分：Docker Compose 常用命令")
print("=" * 60)

commands = [
    ("启动所有服务", "docker-compose up -d", "后台启动所有服务"),
    ("查看服务状态", "docker-compose ps", "查看运行中的服务"),
    ("查看日志", "docker-compose logs -f api", "实时查看 API 服务日志"),
    ("停止所有服务", "docker-compose down", "停止并删除容器"),
    ("重新构建", "docker-compose up -d --build", "重新构建镜像并启动"),
    ("进入容器", "docker exec -it rag-api bash", "进入 API 容器的终端"),
    ("扩展服务", "docker-compose up -d --scale api=3", "启动3个API实例"),
]

print("\n常用命令：")
for name, cmd, desc in commands:
    print(f"\n# {name}")
    print(f"$ {cmd}")
    print(f"# {desc}")


# ============================================================
# 第五部分：项目目录结构
# ============================================================
print("\n" + "=" * 60)
print("第五部分：推荐的项目目录结构")
print("=" * 60)

structure = """
my-rag-project/
├── app/                    # 应用代码
│   ├── __init__.py
│   ├── main.py            # FastAPI 入口
│   ├── rag_chain.py       # RAG 管道
│   └── config.py          # 配置文件
├── data/                   # 数据目录
│   └── documents/         # 知识库文档
├── Dockerfile             # Docker 构建文件
├── docker-compose.yml     # Docker Compose 配置
├── requirements.txt       # Python 依赖
├── .env                   # 环境变量（不提交到 Git）
├── .env.example           # 环境变量模板
└── .dockerignore          # Docker 忽略文件
"""

print(structure)


# ============================================================
# 第六部分：实际运行说明
# ============================================================
print("=" * 60)
print("第六部分：实际运行说明")
print("=" * 60)

print("""
如果要实际运行 Docker Compose：

1. 确保已安装 Docker 和 Docker Compose
2. 复制 .env.example 为 .env 并填写配置
3. 在项目目录运行：

   # 启动所有服务
   docker-compose up -d

   # 查看状态
   docker-compose ps

   # 访问 API
   curl http://localhost:8000/health

   # 访问 Chroma
   curl http://localhost:8001/api/v1/heartbeat

   # 查看日志
   docker-compose logs -f

   # 停止服务
   docker-compose down
""")


# ============================================================
# 总结
# ============================================================
print("=" * 60)
print("总结")
print("=" * 60)

print("""
已生成的文件：
1. docker-compose.yml  - Docker Compose 配置文件
2. .env.example        - 环境变量模板

Docker Compose 的优势：
1. 一条命令启动整个系统
2. 服务之间自动网络连接
3. 依赖关系自动管理
4. 数据持久化
5. 易于扩展和维护
""")
