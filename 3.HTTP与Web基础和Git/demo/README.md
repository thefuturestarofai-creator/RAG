# 第3章 Demo：HTTP 与 Web 基础 + Git 版本控制

> 本章包含 3 个 Demo，对应 HTTP 协议、API 概念、Git 版本控制三大知识点。
> **所有 Demo 均不需要 API Key**，可以直接运行。

---

## 学习顺序

建议按以下顺序学习：

1. **先读理论文档**：`../1.HTTP协议.md` → `../2.API概念.md` → `../3.Git版本控制.md` → `../4.Linux终端操作.md`
2. **再跑 Demo 代码**：按下面的顺序依次运行和理解

---

## Demo 列表

### Demo 1: HTTP 请求
**文件**: `1_demo_HTTP请求.py`

用 Python 的 `urllib`（标准库，无需安装）发送 GET 和 POST 请求，调用公开免费 API（不需要 Key）。演示 HTTP 请求的完整流程：构造请求、发送、解析响应、处理状态码。

**不需要 API Key**
**注意**: 需要网络连接

---

### Demo 2: JSON 处理
**文件**: `2_demo_JSON处理.py`

演示 JSON 数据的解析、构造、转换。模拟处理 API 返回的 JSON 数据，提取有用信息，构造新的 JSON 请求。这是 RAG 系统中处理 API 数据的核心技能。

**不需要 API Key**

---

### Demo 3: Git 操作
**文件**: `3_demo_Git操作.sh`

一个 Bash 脚本，展示 Git 的常用命令流程。用注释详细说明每一步的作用。在 Git Bash 中运行。

**不需要 API Key**

---

### Demo 4: Linux 终端操作
**文件**: `4_demo_终端操作.sh`

一个 Bash 脚本，演示 Linux/Mac 终端的常用命令：文件导航（pwd/ls/cd）、文件操作（mkdir/rm/cp/mv）、内容查看（cat/tail/grep）、环境变量（export/echo $VAR）。每个命令都有详细的中文注释说明用途。

**不需要 API Key**
**运行方式**: 在 Git Bash 或 Linux/Mac 终端中执行 `bash 4_demo_终端操作.sh`

---

## 对应理论文档

| Demo | 对应理论文档 | 核心知识点 |
|------|-------------|-----------|
| Demo 1 | `../1.HTTP协议.md` | GET/POST 请求、状态码、请求头、响应体 |
| Demo 2 | `../2.API概念.md` | JSON 解析与构造、API 响应处理 |
| Demo 3 | `../3.Git版本控制.md` | init/add/commit/push/pull/branch |
| Demo 4 | `../4.Linux终端操作.md` | cd/ls/pwd、文件操作、grep、环境变量 |

---

## 核心要点

学完本章后，你应该能够：

1. **理解 HTTP 通信** —— 知道请求/响应的结构，看懂状态码
2. **处理 JSON 数据** —— 解析 API 响应，构造请求数据
3. **使用 Git 管理代码** —— 初始化仓库、提交代码、创建分支、推送到 GitHub
4. **掌握 Linux 终端操作** —— 文件导航、文件操作、内容查看、环境变量管理
