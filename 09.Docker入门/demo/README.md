# 第9章 Demo 学习指南

## 学习顺序

建议按照以下顺序学习：

1. **先学习理论**：阅读 `1.Docker核心概念.md` 和 `2.Docker实战.md`
2. **再动手实践**：按照 Demo 编号顺序运行

## Demo 列表

### Demo 1: Dockerfile 示例 (`1_demo_dockerfile.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `1.Docker核心概念.md` + `2.Docker实战.md` |
| **功能** | 为 FastAPI 项目编写 Dockerfile，用 Python 脚本模拟构建过程 |
| **是否需要API Key** | 否 |
| **是否需要Docker** | 否（脚本用于教学说明，同时生成实际的 Dockerfile） |

**学习要点**：
- 理解 Dockerfile 的每一行指令
- 理解 Docker 的层缓存机制
- 掌握 Dockerfile 最佳实践

**生成的文件**：
- `Dockerfile` - Docker 构建文件
- `requirements.txt` - Python 依赖文件
- `.dockerignore` - Docker 忽略文件

### Demo 2: docker-compose 示例 (`2_demo_docker_compose.py`)

| 项目 | 说明 |
|------|------|
| **对应理论** | `2.Docker实战.md` |
| **功能** | 编写 docker-compose.yml 编排 FastAPI + Chroma |
| **是否需要API Key** | 否 |
| **是否需要Docker** | 否（脚本用于教学说明，同时生成实际的 docker-compose.yml） |

**学习要点**：
- 理解 Docker Compose 的服务定义
- 掌握服务之间的依赖关系
- 理解端口映射、数据卷、网络配置

**生成的文件**：
- `docker-compose.yml` - Docker Compose 配置文件
- `.env.example` - 环境变量模板

## 运行前准备

```bash
# 本章 Demo 不需要安装额外依赖
# 直接运行 Python 脚本即可

python 1_demo_dockerfile.py
python 2_demo_docker_compose.py
```

## 实际 Docker 操作（可选）

如果要实际构建和运行 Docker 容器，需要：

1. 安装 Docker Desktop（Windows/Mac）或 Docker Engine（Linux）
2. 运行 Demo 脚本生成 Dockerfile 和 docker-compose.yml
3. 按照脚本输出的说明执行 Docker 命令

## 常见问题

**Q: Docker 安装后报错 `docker: command not found`**
A: 确保 Docker 已正确安装并启动。Windows 用户需要开启 WSL2。

**Q: docker-compose 命令找不到**
A: 新版 Docker Desktop 已内置 `docker compose`（不带横杠）。旧版需要单独安装 docker-compose。

**Q: 构建镜像时网络超时**
A: 可以配置国内镜像源，在 Docker Desktop 的 Settings -> Docker Engine 中添加：
```json
{
  "registry-mirrors": ["https://mirror.ccs.tencentyun.com"]
}
```
