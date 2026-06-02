#!/bin/bash
# ============================================================
# Demo 3: Git 操作
# 对应理论文档: 3.Git版本控制.md
# ============================================================
# 这个脚本展示 Git 的常用命令流程。
# 用注释详细说明每一步的作用。
# 在 Git Bash 中运行：bash 3_demo_Git操作.sh
# 不需要 API Key。
# ============================================================

echo "=========================================="
echo "  Git 操作演示脚本"
echo "=========================================="
echo ""
echo "注意：这个脚本展示的是 Git 命令的用法。"
echo "建议手动逐条执行，理解每一步的含义。"
echo ""

# ============================================================
# 1. 初始化仓库
# ============================================================
echo "===== 1. 初始化仓库 ====="
echo ""

# 创建一个演示目录
DEMO_DIR="git_demo_project"
rm -rf $DEMO_DIR 2>/dev/null  # 清理之前的演示
mkdir -p $DEMO_DIR
cd $DEMO_DIR

echo "$ git init"
git init
echo "→ 初始化了一个空的 Git 仓库"
echo ""

echo "$ git status"
git status
echo "→ 查看当前状态"
echo ""

# ============================================================
# 2. 创建文件并提交
# ============================================================
echo "===== 2. 创建文件并提交 ====="
echo ""

# 创建一个 Python 文件
cat > main.py << 'EOF'
# 我的第一个 RAG 项目

def hello():
    print("Hello, RAG!")

if __name__ == "__main__":
    hello()
EOF

echo "$ git status"
git status
echo "→ main.py 是 Untracked（未跟踪）文件"
echo ""

echo "$ git add main.py"
git add main.py
echo "→ main.py 已添加到暂存区"
echo ""

echo "$ git status"
git status
echo "→ main.py 变成绿色（已暂存）"
echo ""

echo "$ git commit -m '初始化项目：添加 main.py'"
git commit -m "初始化项目：添加 main.py"
echo "→ 提交成功！"
echo ""

echo "$ git log --oneline"
git log --oneline
echo "→ 查看提交历史"
echo ""

# ============================================================
# 3. 修改文件并再次提交
# ============================================================
echo "===== 3. 修改文件并再次提交 ====="
echo ""

# 修改文件
cat > main.py << 'EOF'
# RAG 项目 - 添加检索功能

def retrieve(query, top_k=3):
    """模拟检索功能"""
    results = [f"结果{i}: {query}" for i in range(top_k)]
    return results

def hello():
    print("Hello, RAG!")
    results = retrieve("什么是RAG？")
    for r in results:
        print(f"  {r}")

if __name__ == "__main__":
    hello()
EOF

echo "$ git diff"
git diff
echo "→ 查看修改了什么（红色是旧的，绿色是新的）"
echo ""

echo "$ git add main.py"
git add main.py

echo "$ git commit -m '添加检索功能'"
git commit -m "添加检索功能"
echo ""

echo "$ git log --oneline"
git log --oneline
echo "→ 现在有 2 条提交记录"
echo ""

# ============================================================
# 4. 分支操作
# ============================================================
echo "===== 4. 分支操作 ====="
echo ""

echo "$ git branch"
git branch
echo "→ 当前只有一个 main 分支"
echo ""

echo "$ git checkout -b feature-vector-search"
git checkout -b feature-vector-search
echo "→ 创建并切换到新分支 feature-vector-search"
echo ""

echo "$ git branch"
git branch
echo "→ * 号表示当前分支"
echo ""

# 在新分支上添加代码
cat > vector_store.py << 'EOF'
# 向量存储模块

class VectorStore:
    def __init__(self):
        self.vectors = []

    def add(self, text, vector):
        self.vectors.append({"text": text, "vector": vector})

    def search(self, query_vector, top_k=3):
        # 简单模拟：返回所有数据
        return self.vectors[:top_k]
EOF

echo "$ git add vector_store.py"
git add vector_store.py

echo "$ git commit -m '添加向量存储模块'"
git commit -m "添加向量存储模块"
echo ""

echo "$ git log --oneline"
git log --oneline
echo "→ 新分支上有 3 条提交"
echo ""

# ============================================================
# 5. 合并分支
# ============================================================
echo "===== 5. 合并分支 ====="
echo ""

echo "$ git checkout main"
git checkout main
echo "→ 切换回 main 分支"
echo ""

echo "$ git merge feature-vector-search"
git merge feature-vector-search
echo "→ 把 feature-vector-search 合并到 main"
echo ""

echo "$ git log --oneline"
git log --oneline
echo "→ main 分支现在也有 3 条提交"
echo ""

echo "$ git branch -d feature-vector-search"
git branch -d feature-vector-search
echo "→ 删除已合并的分支"
echo ""

echo "$ git branch"
git branch
echo "→ 只剩下 main 分支"
echo ""

# ============================================================
# 6. 查看文件列表
# ============================================================
echo "===== 6. 当前项目文件 ====="
echo ""

echo "$ ls -la"
ls -la
echo ""

echo "项目结构:"
echo "  $DEMO_DIR/"
echo "  ├── .git/          (Git 数据)"
echo "  ├── main.py        (主程序)"
echo "  └── vector_store.py (向量存储模块)"
echo ""

# ============================================================
# 7. 创建 .gitignore
# ============================================================
echo "===== 7. 创建 .gitignore ====="
echo ""

cat > .gitignore << 'EOF'
# 虚拟环境
venv/
.venv/

# Python 缓存
__pycache__/
*.pyc

# 环境变量（包含 API Key）
.env

# 向量数据库数据
chroma_db/

# IDE 配置
.vscode/
.idea/
EOF

echo "$ git add .gitignore"
git add .gitignore

echo "$ git commit -m '添加 .gitignore'"
git commit -m "添加 .gitignore"
echo ""

echo "$ git log --oneline"
git log --oneline
echo ""

# ============================================================
# 8. 常用命令速查
# ============================================================
echo "=========================================="
echo "  Git 常用命令速查表"
echo "=========================================="
echo ""
echo "  初始化:    git init"
echo "  查看状态:  git status"
echo "  添加文件:  git add <file> 或 git add ."
echo "  提交:      git commit -m '说明'"
echo "  查看历史:  git log --oneline"
echo "  查看差异:  git diff"
echo "  创建分支:  git branch <name>"
echo "  切换分支:  git checkout <name>"
echo "  创建+切换: git checkout -b <name>"
echo "  合并分支:  git merge <name>"
echo "  删除分支:  git branch -d <name>"
echo "  添加远程:  git remote add origin <url>"
echo "  推送:      git push -u origin main"
echo "  拉取:      git pull"
echo ""

# 清理演示目录
echo "=========================================="
echo "  演示完毕！"
echo "=========================================="
echo ""
echo "提示：演示目录为 ./$DEMO_DIR"
echo "你可以手动进入查看: cd $DEMO_DIR"
echo ""
echo "如需清理: rm -rf $DEMO_DIR"
