# ============================================================
# Demo 2: 文件操作
# 对应理论文档: 2.文件操作.md
# ============================================================
# 这个 Demo 演示读写 txt、csv、json 文件，路径处理，目录遍历。
# 最后综合示例：扫描目录下所有文档，读取内容，输出处理报告。
# 不需要 API Key。
# ============================================================

import os
import json
import csv
from pathlib import Path

# ----- 准备：创建测试文件 -----
# 为了让 Demo 能直接运行，先创建一些测试文件

TEST_DIR = "demo_test_files"

def setup_test_files():
    """创建测试用的文件和目录"""
    os.makedirs(TEST_DIR, exist_ok=True)

    # 创建 TXT 文件
    with open(os.path.join(TEST_DIR, "doc1.txt"), "w", encoding="utf-8") as f:
        f.write("RAG是检索增强生成技术\n")
        f.write("它通过检索外部知识来增强大模型的回答\n")
        f.write("核心组件包括：检索器、向量数据库、大语言模型\n")

    with open(os.path.join(TEST_DIR, "doc2.txt"), "w", encoding="utf-8") as f:
        f.write("LangChain是大模型应用开发框架\n")
        f.write("它提供了Document Loader、Text Splitter等组件\n")

    # 创建 JSON 文件
    config = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "chunk_size": 500,
        "top_k": 3
    }
    with open(os.path.join(TEST_DIR, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    # 创建 CSV 文件
    with open(os.path.join(TEST_DIR, "qa_pairs.csv"), "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["question", "answer"])
        writer.writeheader()
        writer.writerow({"question": "什么是RAG？", "answer": "检索增强生成技术"})
        writer.writerow({"question": "什么是向量数据库？", "answer": "存储Embedding的数据库"})
        writer.writerow({"question": "LangChain是什么？", "answer": "大模型应用开发框架"})

    # 创建子目录和文件
    sub_dir = os.path.join(TEST_DIR, "subdir")
    os.makedirs(sub_dir, exist_ok=True)
    with open(os.path.join(sub_dir, "doc3.txt"), "w", encoding="utf-8") as f:
        f.write("这是子目录中的文档\n")

    print(f"测试文件已创建在 ./{TEST_DIR}/ 目录下\n")


def cleanup_test_files():
    """清理测试文件"""
    import shutil
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    print(f"\n测试文件已清理")


# ============================================================
# 1. 读写 TXT 文件
# ============================================================
print("=" * 50)
print("1. 读写 TXT 文件")
print("=" * 50)

setup_test_files()

# 读取 TXT 文件
txt_path = os.path.join(TEST_DIR, "doc1.txt")

# 方法1：read() 读取全部内容
with open(txt_path, "r", encoding="utf-8") as f:
    content = f.read()
print(f"read() 读取:\n{content}")

# 方法2：readlines() 读取所有行到列表
with open(txt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"readlines() 结果 ({len(lines)} 行):")
for i, line in enumerate(lines):
    print(f"  第{i+1}行: {line.strip()}")

# 方法3：逐行遍历（内存最友好）
print("\n逐行遍历:")
with open(txt_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        print(f"  第{line_num}行: {line.strip()}")

# 写入 TXT 文件
output_path = os.path.join(TEST_DIR, "output.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("这是写入的第一行\n")
    f.write("这是写入的第二行\n")

# 追加写入
with open(output_path, "a", encoding="utf-8") as f:
    f.write("这是追加的内容\n")

print(f"\n写入完成，验证内容:")
with open(output_path, "r", encoding="utf-8") as f:
    print(f.read())
print()


# ============================================================
# 2. 读写 JSON 文件
# ============================================================
print("=" * 50)
print("2. 读写 JSON 文件")
print("=" * 50)

json_path = os.path.join(TEST_DIR, "config.json")

# 读取 JSON
with open(json_path, "r", encoding="utf-8") as f:
    config = json.load(f)

print(f"配置文件内容:")
for key, value in config.items():
    print(f"  {key}: {value} ({type(value).__name__})")

# 写入 JSON
search_results = [
    {"content": "RAG是检索增强生成", "score": 0.95, "source": "doc1.txt"},
    {"content": "向量数据库存储Embedding", "score": 0.87, "source": "doc2.txt"},
    {"content": "LangChain是开发框架", "score": 0.82, "source": "doc3.txt"},
]

results_path = os.path.join(TEST_DIR, "search_results.json")
with open(results_path, "w", encoding="utf-8") as f:
    json.dump(search_results, f, ensure_ascii=False, indent=2)

print(f"\n搜索结果已写入: {results_path}")
with open(results_path, "r", encoding="utf-8") as f:
    print(f.read())
print()


# ============================================================
# 3. 读写 CSV 文件
# ============================================================
print("=" * 50)
print("3. 读写 CSV 文件")
print("=" * 50)

csv_path = os.path.join(TEST_DIR, "qa_pairs.csv")

# 读取 CSV
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print(f"CSV 字段: {reader.fieldnames}")
    for row in reader:
        print(f"  问: {row['question']}  答: {row['answer']}")

# 写入 CSV
output_csv = os.path.join(TEST_DIR, "chunks.csv")
with open(output_csv, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["chunk_id", "content", "source", "score"])
    writer.writeheader()
    for i, result in enumerate(search_results):
        writer.writerow({
            "chunk_id": f"chunk_{i+1:03d}",
            "content": result["content"],
            "source": result["source"],
            "score": result["score"]
        })

print(f"\nCSV 已写入: {output_csv}")
with open(output_csv, "r", encoding="utf-8") as f:
    print(f.read())
print()


# ============================================================
# 4. 路径处理
# ============================================================
print("=" * 50)
print("4. 路径处理（os.path 和 pathlib）")
print("=" * 50)

# os.path 方式
file_path = os.path.join(TEST_DIR, "doc1.txt")
print(f"os.path 示例:")
print(f"  完整路径: {file_path}")
print(f"  文件存在: {os.path.exists(file_path)}")
print(f"  是否文件: {os.path.isfile(file_path)}")
print(f"  是否目录: {os.path.isdir(TEST_DIR)}")
print(f"  文件大小: {os.path.getsize(file_path)} 字节")
print(f"  文件名: {os.path.basename(file_path)}")
print(f"  目录名: {os.path.dirname(file_path)}")
print(f"  分离扩展名: {os.path.splitext(file_path)}")

# pathlib 方式（更现代）
p = Path(TEST_DIR) / "doc1.txt"
print(f"\npathlib 示例:")
print(f"  完整路径: {p}")
print(f"  文件存在: {p.exists()}")
print(f"  文件名: {p.name}")
print(f"  扩展名: {p.suffix}")
print(f"  不含扩展名: {p.stem}")
print(f"  父目录: {p.parent}")
print()


# ============================================================
# 5. 目录遍历
# ============================================================
print("=" * 50)
print("5. 目录遍历")
print("=" * 50)

# os.listdir() 列出目录内容
print(f"os.listdir('{TEST_DIR}'):")
for item in os.listdir(TEST_DIR):
    item_path = os.path.join(TEST_DIR, item)
    item_type = "目录" if os.path.isdir(item_path) else "文件"
    print(f"  [{item_type}] {item}")

# os.walk() 递归遍历
print(f"\nos.walk() 递归遍历:")
for root, dirs, files in os.walk(TEST_DIR):
    level = root.replace(TEST_DIR, "").count(os.sep)
    indent = "  " * level
    print(f"{indent}[目录] {os.path.basename(root)}/")
    for file in files:
        print(f"{indent}  [文件] {file}")

# pathlib 的 glob
print(f"\npathlib glob '*.txt':")
for txt_file in Path(TEST_DIR).rglob("*.txt"):
    print(f"  {txt_file}")
print()


# ============================================================
# 6. 综合示例：文档扫描和处理报告
# ============================================================
print("=" * 50)
print("综合示例：文档扫描和处理报告")
print("=" * 50)


def scan_documents(directory):
    """
    扫描目录下所有文档，读取内容，生成处理报告
    模拟 RAG 系统的文档加载阶段
    """
    results = {
        "total_files": 0,
        "total_chars": 0,
        "files_by_type": {},
        "files": []
    }

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1].lower()

            # 统计文件类型
            results["files_by_type"][ext] = results["files_by_type"].get(ext, 0) + 1
            results["total_files"] += 1

            # 读取文本文件
            if ext in [".txt", ".json", ".csv"]:
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    char_count = len(content)
                    results["total_chars"] += char_count
                    results["files"].append({
                        "path": filepath,
                        "type": ext,
                        "chars": char_count,
                        "lines": content.count("\n") + 1
                    })
                except Exception as e:
                    results["files"].append({
                        "path": filepath,
                        "type": ext,
                        "error": str(e)
                    })

    return results


def print_report(results):
    """打印处理报告"""
    print(f"\n{'='*40}")
    print(f"  文档扫描报告")
    print(f"{'='*40}")
    print(f"  扫描文件总数: {results['total_files']}")
    print(f"  文本字符总数: {results['total_chars']}")
    print(f"\n  文件类型分布:")
    for ext, count in sorted(results["files_by_type"].items()):
        print(f"    {ext or '(无扩展名)'}: {count} 个")
    print(f"\n  文件详情:")
    for f in results["files"]:
        if "error" in f:
            print(f"    [错误] {f['path']}: {f['error']}")
        else:
            print(f"    [{f['type']}] {f['path']} - {f['chars']} 字符, {f['lines']} 行")


# 运行扫描
results = scan_documents(TEST_DIR)
print_report(results)

# 保存报告为 JSON
report_path = os.path.join(TEST_DIR, "scan_report.json")
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n报告已保存到: {report_path}")

# 清理测试文件
cleanup_test_files()
