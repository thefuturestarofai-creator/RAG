# FastAPI RAG 应用 Dockerfile
# ============================
#
# 构建命令：docker build -t rag-api .
# 运行命令：docker run -d -p 8000:8000 --name rag-app rag-api
#
# 使用 Python 轻量镜像作为基础
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
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
