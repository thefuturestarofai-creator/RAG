# 第13章 Demo 学习指南

## 学习顺序

1. **先看配置文件** → 直接阅读 `docker-compose.yml` 和 `Dockerfile`，理解实际配置
2. **再学 Demo 1（docker-compose.yml 生成器）** → 理解 Docker Compose 的配置结构
3. **最后学 Demo 2（部署脚本）** → 了解完整的部署流程和生产环境考虑

## 可直接使用的配置文件

本目录包含可以直接使用的 Docker 配置文件：

- `docker-compose.yml` — 多容器编排配置（rag-app + chromadb）
- `Dockerfile` — RAG 应用镜像构建文件

使用方法：
```bash
# 复制到项目根目录
cp docker-compose.yml Dockerfile /path/to/your/project/

# 创建 .env 文件
cp .env.example .env
# 编辑 .env 填入 API Key

# 一键启动
docker-compose up -d
```

## Demo 说明

### Demo 1: docker-compose.yml (`1_demo_docker_compose.py`)

**作用**：生成完整的 Docker Compose 配置文件，包括 Dockerfile、docker-compose.yml、.env.example。

**学到什么**：
- Dockerfile 的编写（基础镜像选择、依赖安装、非 root 用户）
- docker-compose.yml 的配置（services、volumes、networks、healthcheck）
- 环境变量管理（.env 文件）
- 服务间通信（使用服务名作为主机名）

**是否需要 API Key**：不需要（只是生成配置文件）

**运行方式**：
```bash
python 1_demo_docker_compose.py
```

运行后会在 `docker_output/` 目录生成所有配置文件。

---

### Demo 2: 部署脚本 (`2_demo_deploy_script.py`)

**作用**：模拟完整的部署流程，同时生成实际可用的部署文件。

**学到什么**：
- 部署流程的 12 个步骤
- 健康检查的配置
- 资源限制的设置
- 一键部署脚本（deploy.sh）的写法

**是否需要 API Key**：不需要

**运行方式**：
```bash
python 2_demo_deploy_script.py
```

---

## 前置依赖

```bash
# 本章 Demo 不需要额外依赖
# 但如果要实际部署，需要安装 Docker 和 Docker Compose
```

## 学完本章你应该能回答

1. Docker Compose 是什么？和 Docker 有什么区别？
2. docker-compose.yml 中的 depends_on 和 healthcheck 有什么作用？
3. 为什么需要 volumes？数据持久化怎么做？
4. 生产环境部署需要考虑哪些方面？
5. 如何编写一个一键部署脚本？
