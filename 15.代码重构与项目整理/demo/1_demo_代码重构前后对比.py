# ============================================================
# Demo 1: 代码重构前后对比
# 对应理论文档: 1.代码重构原则.md
# ============================================================
# 这个 Demo 用一个真实的 RAG 文档处理场景，
# 展示"重构前"和"重构后"的代码差异。
# 不需要 API Key。
# ============================================================

import re
import os

print("=" * 60)
print("重构前 vs 重构后：RAG 文档处理代码")
print("=" * 60)

# ================================================================
#                    ❌ 重构前的代码（反面教材）
# ================================================================
# 问题：重复代码多、函数职责不单一、命名不规范、没有类型注解

def load_and_process_txt(fp):
    """加载并处理 txt 文件"""
    f = open(fp, "r", encoding="utf-8")
    c = f.read()
    f.close()
    # 清洗
    c = c.strip()
    c = re.sub(r'\s+', ' ', c)
    # 切分
    chunks = []
    for i in range(0, len(c), 500):
        chunks.append(c[i:i+500])
    # 构造结果
    results = []
    for chunk in chunks:
        results.append({"content": chunk, "source": fp})
    return results

def load_and_process_md(fp):
    """加载并处理 md 文件"""
    f = open(fp, "r", encoding="utf-8")
    c = f.read()
    f.close()
    # 清洗（和上面完全一样！）
    c = c.strip()
    c = re.sub(r'\s+', ' ', c)
    # 切分（和上面完全一样！）
    chunks = []
    for i in range(0, len(c), 500):
        chunks.append(c[i:i+500])
    # 构造结果（和上面完全一样！）
    results = []
    for chunk in chunks:
        results.append({"content": chunk, "source": fp})
    return results

print("\n【重构前】的问题：")
print("  1. load_and_process_txt 和 load_and_process_md 有 90% 的重复代码")
print("  2. 一个函数做了太多事：加载 + 清洗 + 切分 + 构造结果")
print("  3. 变量名太短（fp, c），看不懂含义")
print("  4. 没有类型注解，不知道参数和返回值是什么类型")
print("  5. 没有异常处理，文件不存在就直接崩溃")
print("  6. 文件没有用 with 语句，可能泄露资源")


# ================================================================
#                    ✅ 重构后的代码（正面教材）
# ================================================================
# 改进：DRY、单一职责、类型注解、异常处理、文档字符串

from typing import List, Dict
from dataclasses import dataclass


# --- 数据结构定义 ---
@dataclass
class ProcessedChunk:
    """处理后的文本块"""
    content: str
    source: str
    chunk_index: int


# --- 每个函数只做一件事（单一职责） ---

def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """
    读取文件内容。

    Args:
        file_path: 文件路径
        encoding: 文件编码，默认 utf-8

    Returns:
        文件内容字符串

    Raises:
        FileNotFoundError: 文件不存在
    """
    with open(file_path, "r", encoding=encoding) as f:
        return f.read()


def clean_text(text: str) -> str:
    """
    清洗文本：去除首尾空白，合并连续空白字符。

    Args:
        text: 原始文本

    Returns:
        清洗后的文本
    """
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def split_text(text: str, chunk_size: int = 500) -> List[str]:
    """
    将文本按指定大小切分。

    Args:
        text: 要切分的文本
        chunk_size: 每个块的最大字符数

    Returns:
        切分后的文本片段列表
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def create_chunks(text: str, source: str, chunk_size: int = 500) -> List[ProcessedChunk]:
    """
    将文本切分为带元数据的块。

    Args:
        text: 原始文本
        source: 来源标识
        chunk_size: 每个块的最大字符数

    Returns:
        ProcessedChunk 列表
    """
    raw_chunks = split_text(text, chunk_size)
    return [
        ProcessedChunk(content=chunk, source=source, chunk_index=i)
        for i, chunk in enumerate(raw_chunks)
    ]


def load_document(file_path: str, chunk_size: int = 500) -> List[ProcessedChunk]:
    """
    加载并处理文档（完整的文档处理管道）。

    流程：读取 → 清洗 → 切分 → 构造结果

    Args:
        file_path: 文件路径
        chunk_size: 每个块的最大字符数

    Returns:
        ProcessedChunk 列表

    Raises:
        FileNotFoundError: 文件不存在
    """
    content = read_file(file_path)
    cleaned = clean_text(content)
    chunks = create_chunks(cleaned, source=file_path, chunk_size=chunk_size)
    return chunks


# --- 运行对比 ---

print("\n" + "=" * 60)
print("【重构后】的改进：")
print("=" * 60)

print("""
  ✅ 1. DRY 原则：公共逻辑提取为 read_file、clean_text、split_text
     - 所有文件类型共用同一套处理逻辑
     - 新增文件类型只需一行代码

  ✅ 2. 单一职责：每个函数只做一件事
     - read_file: 只负责读文件
     - clean_text: 只负责清洗
     - split_text: 只负责切分
     - load_document: 只负责串联流程

  ✅ 3. 类型注解：参数和返回值类型清晰
     - file_path: str
     - 返回值: List[ProcessedChunk]

  ✅ 4. 文档字符串：每个函数都有详细的说明
     - Args、Returns、Raises 都写清楚了

  ✅ 5. 异常处理：用 with 语句管理文件资源
     - 不会泄露文件句柄

  ✅ 6. 数据类：用 @dataclass 定义数据结构
     - 比裸字典更清晰、更安全
""")

# 实际运行示例
print("=" * 60)
print("实际运行：创建测试文件并处理")
print("=" * 60)

# 创建测试文件
test_content = """RAG（检索增强生成）是一种AI技术架构。
它通过检索外部知识库来增强大语言模型的回答能力。
核心流程包括：用户提问、检索相关文档、将文档作为上下文、LLM生成回答。
这种技术可以有效减少大模型的幻觉问题，并且知识可以随时更新。
向量数据库是RAG系统的核心组件，用于存储和检索文本的Embedding向量。"""

test_file = "test_document.txt"
with open(test_file, "w", encoding="utf-8") as f:
    f.write(test_content)

print(f"\n创建测试文件: {test_file}")
print(f"文件大小: {len(test_content)} 字符")

# 用重构后的代码处理
chunks = load_document(test_file, chunk_size=60)

print(f"\n处理结果：切分成 {len(chunks)} 个块")
for chunk in chunks:
    print(f"  [块{chunk.chunk_index}] ({len(chunk.content)}字) {chunk.content}")

# 清理测试文件
os.remove(test_file)
print(f"\n已清理测试文件: {test_file}")


# ================================================================
#                    重构检查清单
# ================================================================

print("\n" + "=" * 60)
print("重构检查清单（自查用）")
print("=" * 60)

checklist = [
    ("DRY 原则", "是否有重复代码出现 3 次以上？", "提取公共函数"),
    ("单一职责", "一个函数是否做了 3 件以上的事？", "拆分成多个函数"),
    ("命名规范", "变量名是否能看懂含义？", "用有意义的英文单词"),
    ("类型注解", "函数参数和返回值是否有类型？", "添加 type hints"),
    ("文档字符串", "函数是否有 docstring？", "写 Args/Returns/Raises"),
    ("异常处理", "文件操作/API调用是否有 try/except？", "添加异常处理"),
    ("资源管理", "文件操作是否用 with 语句？", "改用 with open(...)"),
]

for i, (name, check, fix) in enumerate(checklist, 1):
    print(f"\n  {i}. {name}")
    print(f"     检查：{check}")
    print(f"     修复：{fix}")
