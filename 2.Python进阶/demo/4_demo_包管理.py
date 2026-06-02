# ============================================================
# Demo 4: 包管理与虚拟环境
# 对应理论文档: 4.包管理与虚拟环境.md
# ============================================================
# 这个 Demo 用代码和注释演示 pip、requirements.txt、venv 的用法。
# 不依赖任何第三方库，纯 Python 代码说明包管理的概念。
# 不需要 API Key。
# ============================================================

import os
import sys
import subprocess

# ============================================================
# 1. 查看当前 Python 环境信息
# ============================================================
print("=" * 50)
print("1. 当前 Python 环境信息")
print("=" * 50)

print(f"Python 版本: {sys.version}")
print(f"Python 路径: {sys.executable}")
print(f"平台信息: {sys.platform}")

# 查看已安装的包（用 pkg_resources，不依赖第三方库）
print(f"\n已安装的包（部分）:")
try:
    import pkg_resources
    installed = sorted([d.project_name for d in pkg_resources.working_set])
    # 只显示前 20 个
    for pkg in installed[:20]:
        version = pkg_resources.get_distribution(pkg).version
        print(f"  {pkg} == {version}")
    print(f"  ... 共 {len(installed)} 个包")
except ImportError:
    print("  pkg_resources 不可用，请用 pip list 查看")
print()


# ============================================================
# 2. pip 常用命令说明
# ============================================================
print("=" * 50)
print("2. pip 常用命令说明（注释版）")
print("=" * 50)

pip_commands = """
# ========== 安装包 ==========
# 安装最新版
pip install langchain

# 安装指定版本
pip install langchain==0.1.0

# 安装多个包
pip install langchain openai chromadb

# 从 requirements.txt 安装
pip install -r requirements.txt

# ========== 升级和卸载 ==========
# 升级包
pip install --upgrade langchain

# 卸载包
pip uninstall langchain

# ========== 查看信息 ==========
# 查看已安装的包
pip list

# 查看某个包的详细信息
pip show langchain

# 导出当前环境的所有依赖
pip freeze > requirements.txt

# ========== 使用国内镜像源 ==========
# 临时使用清华源
pip install langchain -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久设置清华源（推荐）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 恢复默认源
pip config unset global.index-url
"""
print(pip_commands)


# ============================================================
# 3. requirements.txt 示例
# ============================================================
print("=" * 50)
print("3. requirements.txt 示例")
print("=" * 50)

# 模拟生成 requirements.txt
requirements = """# RAG 项目依赖
# 使用方法: pip install -r requirements.txt

# 核心框架
langchain>=0.1.0
openai>=1.0.0

# 向量数据库
chromadb>=0.4.0

# Token 计数
tiktoken>=0.5.0

# 环境变量管理
python-dotenv>=1.0.0

# 文档解析（可选）
# unstructured>=0.10.0

# 本地 Embedding 模型（可选）
# sentence-transformers>=2.0
"""

print("requirements.txt 内容:")
print(requirements)

# 写入一个示例 requirements.txt
req_path = "requirements_example.txt"
with open(req_path, "w", encoding="utf-8") as f:
    f.write(requirements)
print(f"已写入示例文件: {req_path}")

# 读取并解析 requirements.txt
print(f"\n解析 requirements.txt:")
with open(req_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue    # 跳过空行和注释
        # 解析包名和版本
        if ">=" in line:
            name, version = line.split(">=")
            print(f"  {name.strip()} (需要 >= {version.strip()})")
        elif "==" in line:
            name, version = line.split("==")
            print(f"  {name.strip()} (需要 == {version.strip()})")
        else:
            print(f"  {line} (不限版本)")

os.remove(req_path)
print()


# ============================================================
# 4. 虚拟环境操作演示
# ============================================================
print("=" * 50)
print("4. 虚拟环境操作说明")
print("=" * 50)

venv_guide = """
# ========== 创建虚拟环境 ==========
# 在项目目录下执行：
python -m venv venv

# 这会创建一个 venv/ 目录，包含：
# - 独立的 Python 解释器
# - 独立的 pip
# - 独立的已安装包

# ========== 激活虚拟环境 ==========
# Windows CMD:
venv\\Scripts\\activate.bat

# Windows PowerShell:
venv\\Scripts\\Activate.ps1

# macOS / Linux:
source venv/bin/activate

# 激活后命令行会出现 (venv) 前缀：
# (venv) C:\\Users\\你\\project>

# ========== 在虚拟环境中工作 ==========
# 此时 pip install 会安装到虚拟环境中，不影响全局
pip install langchain openai
pip freeze > requirements.txt

# ========== 退出虚拟环境 ==========
deactivate

# 前缀消失，回到全局环境

# ========== 从零恢复环境 ==========
# 别人拿到你的项目后：
python -m venv venv
venv\\Scripts\\activate          # Windows
pip install -r requirements.txt
"""
print(venv_guide)


# ============================================================
# 5. .gitignore 说明
# ============================================================
print("=" * 50)
print("5. .gitignore 说明")
print("=" * 50)

gitignore_content = """# Python 虚拟环境（不应该提交）
venv/
.venv/
env/

# Python 缓存文件
__pycache__/
*.pyc
*.pyo

# 环境变量文件（包含 API Key，绝对不能提交！）
.env

# IDE 配置
.vscode/
.idea/

# 系�载临时文件
*.log
dist/
build/
*.egg-info/

# 向量数据库数据（可能很大）
chroma_db/
.vectorstore/
"""

print(".gitignore 内容示例:")
print(gitignore_content)


# ============================================================
# 6. .env 文件说明
# ============================================================
print("=" * 50)
print("6. .env 文件说明")
print("=" * 50)

env_example = """# .env 文件示例
# 这个文件存放敏感配置，绝对不能提交到 Git！

# OpenAI API Key
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

# 向量数据库配置
CHROMA_PERSIST_DIR=./chroma_db

# 模型配置
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
"""

print(".env 文件内容示例:")
print(env_example)

print("在 Python 中读取 .env 的方法:")
print("""
# 方法1: 手动读取
import os
api_key = os.environ.get("OPENAI_API_KEY", "未设置")

# 方法2: 使用 python-dotenv（推荐）
from dotenv import load_dotenv
load_dotenv()                   # 加载 .env 文件
api_key = os.environ.get("OPENAI_API_KEY")
""")


# ============================================================
# 7. 综合示例：模拟项目初始化流程
# ============================================================
print("=" * 50)
print("综合示例：模拟 RAG 项目初始化流程")
print("=" * 50)


def simulate_project_init():
    """
    模拟一个 RAG 项目的初始化流程
    展示实际开发中包管理的完整步骤
    """
    project_steps = [
        {
            "step": "1. 创建项目目录",
            "commands": ["mkdir my_rag_project", "cd my_rag_project"],
            "explanation": "每个项目一个独立目录"
        },
        {
            "step": "2. 创建虚拟环境",
            "commands": ["python -m venv venv"],
            "explanation": "隔离项目依赖，避免版本冲突"
        },
        {
            "step": "3. 激活虚拟环境",
            "commands": ["venv\\Scripts\\activate  # Windows", "source venv/bin/activate  # macOS/Linux"],
            "explanation": "激活后 pip install 只影响当前项目"
        },
        {
            "step": "4. 安装依赖",
            "commands": [
                "pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \\",
                "    langchain openai chromadb tiktoken python-dotenv"
            ],
            "explanation": "使用国内镜像加速下载"
        },
        {
            "step": "5. 导出依赖列表",
            "commands": ["pip freeze > requirements.txt"],
            "explanation": "锁定版本，方便团队协作和部署"
        },
        {
            "step": "6. 创建 .gitignore",
            "commands": ["echo venv/ >> .gitignore", "echo .env >> .gitignore"],
            "explanation": "防止虚拟环境和敏感信息被提交"
        },
        {
            "step": "7. 创建 .env 文件",
            "commands": ["echo OPENAI_API_KEY=sk-xxx > .env"],
            "explanation": "存放 API Key，不要提交到 Git"
        },
        {
            "step": "8. 初始化 Git",
            "commands": ["git init", "git add .", "git commit -m 'Initial commit'"],
            "explanation": "开始版本控制"
        },
    ]

    for item in project_steps:
        print(f"\n{item['step']}")
        print(f"  说明: {item['explanation']}")
        for cmd in item["commands"]:
            print(f"  $ {cmd}")

    print(f"\n{'='*40}")
    print("项目结构:")
    print(f"{'='*40}")
    print("""
my_rag_project/
├── venv/                  # 虚拟环境（不提交到 Git）
├── .env                   # API Key（不提交到 Git）
├── .gitignore             # Git 忽略规则
├── requirements.txt       # 依赖列表
├── main.py                # 主程序
└── README.md              # 项目说明
""")


simulate_project_init()


# ============================================================
# 8. 常见问题排查
# ============================================================
print("=" * 50)
print("8. 常见问题排查")
print("=" * 50)

troubleshooting = """
问题1: pip install 很慢
解决: 使用国内镜像源
  pip install xxx -i https://pypi.tuna.tsinghua.edu.cn/simple
  或永久设置: pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

问题2: ModuleNotFoundError: No module named 'xxx'
解决: 检查是否激活了虚拟环境，是否安装了该包
  pip list | grep xxx
  pip install xxx

问题3: 版本冲突 (dependency resolution)
解决: 指定兼容的版本范围
  pip install langchain>=0.1.0,<0.2.0

问题4: pip install 报错 "Permission denied"
解决: 不要用 sudo pip install！用虚拟环境
  python -m venv venv
  source venv/bin/activate
  pip install xxx

问题5: requirements.txt 安装失败
解决: 逐个安装定位问题包
  pip install -r requirements.txt 2>&1 | head -50
"""
print(troubleshooting)
