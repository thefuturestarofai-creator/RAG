"""
Demo 1: Dockerfile 示例 - 为 FastAPI 项目编写 Dockerfile
=======================================================

功能：
- 演示如何为 FastAPI 项目编写 Dockerfile
- 用 Python 脚本模拟和说明 Docker 的构建过程
- 同时生成实际可用的 Dockerfile 文件

前置条件：
- 不需要 Docker 和 API Key（本脚本用于教学说明）
- 如果要实际构建镜像，需要安装 Docker

对应理论：1.Docker核心概念.md + 2.Docker实战.md
"""

import os

# ============================================================
# 第一部分：说明 Docker 构建流程
# ============================================================
print("=" * 60)
print("第一部分：Docker 构建流程说明")
print("=" * 60)

print("""
Docker 构建流程（以 FastAPI 项目为例）：

1. 编写 Dockerfile（构建说明）
2. 运行 docker build 命令（构建镜像）
3. 运行 docker run 命令（创建容器）

类比：
- Dockerfile = 菜谱
- docker build = 按照菜谱做菜
- docker run = 把菜端上桌
""")


# ============================================================
# 第二部分：模拟 Dockerfile 的每一层
# ============================================================
print("=" * 60)
print("第二部分：模拟 Dockerfile 构建过程")
print("=" * 60)

# 模拟 Docker 的层构建过程
layers = [
    {
        "instruction": "FROM python:3.11-slim",
        "description": "选择基础镜像（就像选择厨房）",
        "action": "下载 Python 3.11 轻量镜像"
    },
    {
        "instruction": "WORKDIR /app",
        "description": "设置工作目录（就像准备好料理台）",
        "action": "创建 /app 目录"
    },
    {
        "instruction": "COPY requirements.txt .",
        "description": "复制依赖文件（先把购物清单拿进来）",
        "action": "复制 requirements.txt 到 /app/"
    },
    {
        "instruction": "RUN pip install -r requirements.txt",
        "description": "安装依赖（按照购物清单采购食材）",
        "action": "执行 pip install"
    },
    {
        "instruction": "COPY . .",
        "description": "复制应用代码（把食材放进厨房）",
        "action": "复制所有文件到 /app/"
    },
    {
        "instruction": "EXPOSE 8000",
        "description": "声明端口（告诉外面从哪个窗口取餐）",
        "action": "声明容器使用 8000 端口"
    },
    {
        "instruction": "CMD [\"uvicorn\", \"main:app\"]",
        "description": "启动命令（开火做菜）",
        "action": "容器启动时执行 uvicorn"
    }
]

print("\n逐层构建过程：")
for i, layer in enumerate(layers, 1):
    print(f"\n--- 第 {i} 层 ---")
    print(f"指令：{layer['instruction']}")
    print(f"类比：{layer['description']}")
    print(f"动作：{layer['action']}")


# ============================================================
# 第三部分：生成实际的 Dockerfile
# ============================================================
print("\n" + "=" * 60)
print("第三部分：生成实际的 Dockerfile")
print("=" * 60)

dockerfile_content = '''# FastAPI RAG 应用 Dockerfile
# 使用 Python 轻量镜像作为基础
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \\
    PYTHONDONTWRITEBYTECODE=1

# 复制依赖文件（利用 Docker 缓存机制）
# 如果 requirements.txt 没变，这一层会使用缓存
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 创建非 root 用户（安全最佳实践）
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

# 写入 Dockerfile
dockerfile_path = "Dockerfile"
with open(dockerfile_path, "w", encoding="utf-8") as f:
    f.write(dockerfile_content)

print(f"已生成 Dockerfile：{dockerfile_path}")
print("\nDockerfile 内容预览：")
print("-" * 40)
for i, line in enumerate(dockerfile_content.strip().split('\n'), 1):
    print(f"{i:2d} | {line}")


# ============================================================
# 第四部分：生成示例 requirements.txt
# ============================================================
print("\n" + "=" * 60)
print("第四部分：生成示例 requirements.txt")
print("=" * 60)

requirements_content = '''# FastAPI RAG 应用依赖
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.2
langchain==0.0.350
langchain-openai==0.0.2
langchain-community==0.0.6
langchain-chroma==0.0.2
chromadb==0.4.18
'''

requirements_path = "requirements.txt"
with open(requirements_path, "w", encoding="utf-8") as f:
    f.write(requirements_content)

print(f"已生成 requirements.txt：{requirements_path}")


# ============================================================
# 第五部分：Docker 构建和运行命令
# ============================================================
print("\n" + "=" * 60)
print("第五部分：Docker 构建和运行命令")
print("=" * 60)

print("""
# 1. 构建镜像
docker build -t rag-api .

# 2. 查看构建的镜像
docker images | grep rag-api

# 3. 运行容器
docker run -d \\
    --name rag-app \\
    -p 8000:8000 \\
    -e API_KEY=your-api-key \\
    rag-api

# 4. 查看运行状态
docker ps

# 5. 查看日志
docker logs rag-app

# 6. 停止容器
docker stop rag-app

# 7. 删除容器
docker rm rag-app
""")


# ============================================================
# 第六部分：最佳实践说明
# ============================================================
print("=" * 60)
print("第六部分：Dockerfile 最佳实践")
print("=" * 60)

practices = [
    ("使用轻量基础镜像", "用 python:3.11-slim 而不是 python:3.11，镜像更小"),
    ("利用层缓存", "先 COPY requirements.txt，再 COPY 代码，依赖没变时用缓存"),
    ("合并 RUN 指令", "减少镜像层数，如 RUN apt-get update && apt-get install -y xxx"),
    ("使用 .dockerignore", "排除不需要的文件，如 .git、__pycache__、.env"),
    ("非 root 用户", "创建专用用户运行应用，提高安全性"),
    ("多阶段构建", "构建阶段和运行阶段分开，最终镜像更小"),
]

print("\nDockerfile 最佳实践：")
for i, (title, desc) in enumerate(practices, 1):
    print(f"\n{i}. {title}")
    print(f"   {desc}")


# ============================================================
# 生成 .dockerignore 文件
# ============================================================
print("\n" + "=" * 60)
print("生成 .dockerignore 文件")
print("=" * 60)

dockerignore_content = '''# Git
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
*.egg-info
dist
build
.eggs

# 虚拟环境
venv
.venv
env

# IDE
.vscode
.idea
*.swp

# 环境变量
.env
.env.*

# Docker
Dockerfile
docker-compose.yml
.dockerignore

# 数据目录
chroma_db
*.db
'''

dockerignore_path = ".dockerignore"
with open(dockerignore_path, "w", encoding="utf-8") as f:
    f.write(dockerignore_content)

print(f"已生成 .dockerignore：{dockerignore_path}")


# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("总结")
print("=" * 60)

print("""
已生成的文件：
1. Dockerfile          - Docker 构建文件
2. requirements.txt    - Python 依赖文件
3. .dockerignore       - Docker 忽略文件

如需实际构建镜像，请确保：
1. 已安装 Docker
2. 在文件所在目录运行：docker build -t rag-api .
3. 运行容器：docker run -d -p 8000:8000 rag-api
""")
