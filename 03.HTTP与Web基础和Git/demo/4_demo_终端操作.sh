#!/bin/bash
# ============================================================
# Demo 4: Linux 终端操作
# 本脚本演示 Linux/Mac 终端的常用命令
# 每个命令都有详细的中文注释说明
#
# 运行方式：在 Git Bash 或 Linux/Mac 终端中执行
# bash 4_demo_终端操作.sh
# ============================================================

echo "=========================================="
echo "  Linux 终端操作 Demo"
echo "=========================================="
echo ""

# ============================================================
# 第一部分：文件导航命令
# ============================================================
echo "【第一部分：文件导航命令】"
echo ""

# 1. pwd - 显示当前工作目录（Print Working Directory）
# 用途：告诉你"你现在在哪里"
echo "1. pwd 命令 - 显示当前目录"
pwd
echo ""

# 2. ls - 列出目录内容（List）
# 用途：查看当前目录下有哪些文件和文件夹
echo "2. ls 命令 - 列出文件"
echo "   ls（基本用法）："
ls
echo ""
echo "   ls -l（详细信息）："
ls -l
echo ""
echo "   ls -lh（文件大小用人类可读格式）："
ls -lh 2>/dev/null || ls -l
echo ""

# 3. cd - 切换目录（Change Directory）
echo "3. cd 命令 - 切换目录"
echo "   当前目录：$(pwd)"

# 保存当前目录，以便后面回来
ORIGINAL_DIR=$(pwd)

# cd .. 回到上一级目录
cd .. 2>/dev/null
echo "   执行 cd .. 后：$(pwd)"

# cd - 回到上一次的目录
cd - 2>/dev/null
echo "   执行 cd - 后：$(pwd)"

# 回到原始目录
cd "$ORIGINAL_DIR"
echo ""

# ============================================================
# 第二部分：文件操作命令
# ============================================================
echo "【第二部分：文件操作命令】"
echo ""

# 创建一个临时目录用于演示
TEMP_DIR="temp_demo_$(date +%s)"
mkdir -p "$TEMP_DIR"
echo "创建临时目录：$TEMP_DIR"
echo ""

# 4. mkdir - 创建目录（Make Directory）
echo "4. mkdir 命令 - 创建目录"
mkdir -p "$TEMP_DIR/subdir1/subdir2"
echo "   创建多级目录：$TEMP_DIR/subdir1/subdir2"
ls -R "$TEMP_DIR"
echo ""

# 5. 创建一些测试文件
echo "5. 创建测试文件"
echo "Hello, World!" > "$TEMP_DIR/file1.txt"
echo "这是第二个文件的内容" > "$TEMP_DIR/file2.txt"
echo "RAG 系统学习笔记" > "$TEMP_DIR/notes.txt"
echo "   创建了 3 个文件"
ls -l "$TEMP_DIR"
echo ""

# 6. cp - 复制文件（Copy）
echo "6. cp 命令 - 复制文件"
cp "$TEMP_DIR/file1.txt" "$TEMP_DIR/file1_backup.txt"
echo "   复制 file1.txt 为 file1_backup.txt"
ls "$TEMP_DIR"
echo ""

# 7. mv - 移动/重命名文件（Move）
echo "7. mv 命令 - 重命名文件"
mv "$TEMP_DIR/file1_backup.txt" "$TEMP_DIR/file_renamed.txt"
echo "   将 file1_backup.txt 重命名为 file_renamed.txt"
ls "$TEMP_DIR"
echo ""

# ============================================================
# 第三部分：查看文件内容
# ============================================================
echo "【第三部分：查看文件内容】"
echo ""

# 8. cat - 查看文件全部内容（Concatenate）
echo "8. cat 命令 - 查看文件内容"
echo "   file1.txt 的内容："
cat "$TEMP_DIR/file1.txt"
echo ""
echo "   带行号显示："
cat -n "$TEMP_DIR/notes.txt"
echo ""

# 9. 创建一个较大的文件用于演示 tail 和 grep
echo "9. 创建测试日志文件"
for i in $(seq 1 20); do
    echo "[$(date +%H:%M:%S)] 日志行 $i: 这是第 $i 条日志记录" >> "$TEMP_DIR/app.log"
done
echo "   创建了 20 行日志"
echo ""

# 10. head - 查看文件开头
echo "10. head 命令 - 查看文件前几行"
echo "    日志文件前 5 行："
head -n 5 "$TEMP_DIR/app.log"
echo ""

# 11. tail - 查看文件末尾
echo "11. tail 命令 - 查看文件末尾"
echo "    日志文件最后 5 行："
tail -n 5 "$TEMP_DIR/app.log"
echo ""

# 12. grep - 搜索文件内容
echo "12. grep 命令 - 搜索内容"
echo "    搜索包含 '日志行 5' 的行："
grep "日志行 5" "$TEMP_DIR/app.log"
echo ""
echo "    搜索包含 '日志行 1' 的所有行（会匹配 1, 10-19）："
grep "日志行 1" "$TEMP_DIR/app.log"
echo ""
echo "    使用正则表达式搜索（只匹配单独的数字5）："
grep -E "日志行 [^1]*5[^0-9]" "$TEMP_DIR/app.log" || grep "日志行 5[^0-9]" "$TEMP_DIR/app.log"
echo ""

# ============================================================
# 第四部分：环境变量
# ============================================================
echo "【第四部分：环境变量】"
echo ""

# 13. 设置环境变量
echo "13. 设置和查看环境变量"
# 临时设置一个环境变量
export DEMO_API_KEY="sk-demo-1234567890"
export DEMO_BASE_URL="https://api.example.com/v1"
echo "    设置了 DEMO_API_KEY=$DEMO_API_KEY"
echo "    设置了 DEMO_BASE_URL=$DEMO_BASE_URL"
echo ""

# 14. 读取环境变量
echo "14. 读取环境变量"
echo "    DEMO_API_KEY = $DEMO_API_KEY"
echo "    DEMO_BASE_URL = $DEMO_BASE_URL"
echo "    HOME = $HOME"
echo "    PATH 的前 100 个字符 = ${PATH:0:100}..."
echo ""

# 15. 在实际项目中的用法示例
echo "15. 环境变量在 RAG 项目中的应用"
echo "    通常的做法是："
echo "    export OPENAI_API_KEY='sk-your-key-here'"
echo "    export OPENAI_BASE_URL='https://api.openai.com/v1'"
echo "    python main.py"
echo ""
echo "    在 Python 代码中读取："
echo "    import os"
echo "    api_key = os.environ.get('OPENAI_API_KEY')"
echo ""

# ============================================================
# 第五部分：实际应用场景
# ============================================================
echo "【第五部分：RAG 项目中的实际应用】"
echo ""

echo "16. 常用场景示例"
echo ""

echo "    场景1：查看项目目录结构"
echo "    命令：ls -la"
ls -la
echo ""

echo "    场景2：搜索代码中的关键词"
echo "    命令：grep -rn 'def' --include='*.py' .（搜索 Python 文件中的函数定义）"
# 演示搜索当前目录的 Python 文件
PY_FILES=$(find . -name "*.py" 2>/dev/null | head -3)
if [ -n "$PY_FILES" ]; then
    echo "    找到的 Python 文件："
    echo "$PY_FILES"
    echo "    在这些文件中搜索 'import'："
    grep -n "import" $PY_FILES 2>/dev/null | head -5
else
    echo "    （当前目录没有 Python 文件，跳过演示）"
fi
echo ""

echo "    场景3：查看日志文件"
echo "    命令：tail -f logs/app.log（实时监控日志）"
echo "    命令：grep 'ERROR' logs/app.log（搜索错误日志）"
echo ""

echo "    场景4：批量操作文件"
echo "    命令：cp data/*.txt backup/（复制所有 txt 文件到 backup 目录）"
echo "    命令：rm -rf __pycache__/（清理 Python 缓存）"
echo ""

# ============================================================
# 清理临时文件
# ============================================================
echo "=========================================="
echo "  清理临时文件"
echo "=========================================="
rm -rf "$TEMP_DIR"
echo "已删除临时目录：$TEMP_DIR"

# 清理环境变量
unset DEMO_API_KEY
unset DEMO_BASE_URL
echo "已清理临时环境变量"
echo ""

echo "=========================================="
echo "  Demo 完成！"
echo "=========================================="
echo ""
echo "总结："
echo "  - pwd/ls/cd：文件导航三件套"
echo "  - mkdir/rm/cp/mv：文件操作四天王"
echo "  - cat/tail/grep：查看文件内容三剑客"
echo "  - export/echo \$VAR：环境变量操作"
echo ""
echo "建议：把这些命令用到日常开发中，一周就能熟练掌握！"
