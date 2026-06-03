# ============================================================
# Demo 3: 异常处理
# 对应理论文档: 3.异常处理.md
# ============================================================
# 这个 Demo 演示 try/except/finally、常见异常类型、
# 自定义异常、重试机制。
# 最后综合示例：模拟 RAG 管道中的异常处理。
# 不需要 API Key。
# ============================================================

import os
import json
import random
import time

# 固定随机种子，保证结果可复现
random.seed(42)

# ============================================================
# 1. 基本语法：try/except/else/finally
# ============================================================
print("=" * 50)
print("1. 基本语法：try/except/else/finally")
print("=" * 50)

# 示例1：捕获除零错误
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"捕获到错误: {type(e).__name__}: {e}")
else:
    print(f"计算结果: {result}")    # 出错时不会执行
finally:
    print("finally 块总是执行\n")

# 示例2：正常执行的情况
try:
    result = 10 / 2
except ZeroDivisionError:
    print("出错了")
else:
    print(f"正常结果: {result}")    # 没出错时执行
finally:
    print("finally 块总是执行\n")


# ============================================================
# 2. 常见异常类型演示
# ============================================================
print("=" * 50)
print("2. 常见异常类型演示")
print("=" * 50)

# FileNotFoundError —— 文件不存在
print(">>> FileNotFoundError:")
try:
    with open("不存在的文件.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("  文件不存在，请检查路径\n")

# KeyError —— 字典键不存在
print(">>> KeyError:")
try:
    data = {"name": "RAG", "version": "1.0"}
    value = data["age"]
except KeyError as e:
    print(f"  键 {e} 不存在，可用的键: {list(data.keys())}\n")

# IndexError —— 列表索引越界
print(">>> IndexError:")
try:
    items = ["a", "b", "c"]
    value = items[10]
except IndexError:
    print(f"  索引越界，列表长度只有 {len(items)}\n")

# TypeError —— 类型不匹配
print(">>> TypeError:")
try:
    score = 0.95
    message = "分数: " + score    # 字符串不能和数字拼接
except TypeError:
    message = "分数: " + str(score)
    print(f"  类型转换后: {message}\n")

# ValueError —— 值不合法
print(">>> ValueError:")
try:
    num = int("abc")
except ValueError:
    print("  'abc' 无法转换为整数\n")

# AttributeError —— 对象没有该属性
print(">>> AttributeError:")
try:
    text = "hello"
    text.append("world")    # 字符串没有 append 方法
except AttributeError:
    print("  字符串没有 append 方法（那是列表的方法）\n")


# ============================================================
# 3. 同时捕获多种异常
# ============================================================
print("=" * 50)
print("3. 同时捕获多种异常")
print("=" * 50)


def safe_read_json(filepath):
    """安全地读取 JSON 文件，处理各种可能的错误"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  文件不存在: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"  JSON 解析错误: {e}")
        return None
    except PermissionError:
        print(f"  没有权限读取: {filepath}")
        return None
    except Exception as e:
        print(f"  未知错误: {type(e).__name__}: {e}")
        return None


# 测试不同情况
print("测试1: 文件不存在")
safe_read_json("not_exist.json")

print("\n测试2: 创建一个无效 JSON 文件")
with open("bad.json", "w") as f:
    f.write("{invalid json content}")
safe_read_json("bad.json")
os.remove("bad.json")

print("\n测试3: 正常 JSON 文件")
with open("good.json", "w") as f:
    json.dump({"key": "value"}, f)
result = safe_read_json("good.json")
print(f"  读取成功: {result}")
os.remove("good.json")
print()


# ============================================================
# 4. 自定义异常
# ============================================================
print("=" * 50)
print("4. 自定义异常")
print("=" * 50)


class RAGError(Exception):
    """RAG 系统基础异常"""
    pass


class DocumentLoadError(RAGError):
    """文档加载异常"""
    def __init__(self, filepath, message="文档加载失败"):
        self.filepath = filepath
        super().__init__(f"{message}: {filepath}")


class RetrievalError(RAGError):
    """检索异常"""
    def __init__(self, query, message="检索失败"):
        self.query = query
        super().__init__(f"{message}: 查询='{query}'")


class APIError(RAGError):
    """API 调用异常"""
    def __init__(self, message="API 调用失败", status_code=None):
        self.status_code = status_code
        super().__init__(message)


class RateLimitError(APIError):
    """API 限流异常"""
    def __init__(self, retry_after=60):
        self.retry_after = retry_after
        super().__init__(f"请求被限流，请 {retry_after} 秒后重试", status_code=429)


# 使用自定义异常
def load_document(filepath):
    """模拟文档加载"""
    if not os.path.exists(filepath):
        raise DocumentLoadError(filepath, "文件不存在")
    return f"文档内容: {filepath}"


def search(query):
    """模拟检索"""
    if not query.strip():
        raise RetrievalError(query, "查询不能为空")
    if random.random() < 0.3:
        raise RetrievalError(query, "向量数据库连接失败")
    return [f"结果1: {query}", f"结果2: {query}"]


# 测试自定义异常
print("测试自定义异常:")
try:
    load_document("不存在.txt")
except DocumentLoadError as e:
    print(f"  捕获: {e}")
    print(f"  文件路径: {e.filepath}")

try:
    search("")
except RetrievalError as e:
    print(f"  捕获: {e}")
    print(f"  查询: {e.query}")

try:
    raise RateLimitError(retry_after=30)
except RateLimitError as e:
    print(f"  捕获: {e}")
    print(f"  状态码: {e.status_code}, 重试等待: {e.retry_after}秒")
except APIError as e:
    print(f"  这不会执行，因为 RateLimitError 先被捕获")
print()


# ============================================================
# 5. 重试机制（RAG 中非常重要）
# ============================================================
print("=" * 50)
print("5. 重试机制")
print("=" * 50)


def call_with_retry(func, *args, max_retries=3, delay=0.5, **kwargs):
    """
    带重试的函数调用
    - func: 要执行的函数
    - max_retries: 最大重试次数
    - delay: 基础等待时间（秒）
    使用指数退避策略：1x, 2x, 4x...
    """
    for attempt in range(max_retries):
        try:
            result = func(*args, **kwargs)
            if attempt > 0:
                print(f"    第 {attempt + 1} 次尝试成功!")
            return result
        except (ConnectionError, APIError, RateLimitError) as e:
            if attempt < max_retries - 1:
                wait_time = delay * (2 ** attempt)    # 指数退避
                print(f"    第 {attempt + 1} 次失败: {e}")
                print(f"    等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"    第 {attempt + 1} 次失败: {e}")
                print(f"    已达到最大重试次数 ({max_retries})")
                raise


# 模拟一个不稳定的 API
def unstable_api(query):
    """模拟一个概率失败的 API"""
    if random.random() < 0.6:    # 60% 概率失败
        raise ConnectionError("API 超时")
    return f"API 返回: {query} 的回答"


# 测试重试机制
print("测试重试机制（模拟不稳定的 API）:")
random.seed(42)
try:
    result = call_with_retry(unstable_api, "什么是RAG？", max_retries=3, delay=0.1)
    print(f"  最终结果: {result}")
except ConnectionError:
    print(f"  所有重试都失败了，使用备用方案")
print()


# ============================================================
# 6. 综合示例：RAG 管道的异常处理
# ============================================================
print("=" * 50)
print("综合示例：RAG 管道的异常处理")
print("=" * 50)

# 模拟文件系统
MOCK_FILES = {
    "doc1.txt": "RAG是检索增强生成技术",
    "doc2.txt": "向量数据库用于存储Embedding",
    "doc3.txt": "",              # 空文件
    # doc4.txt 不存在
}

MOCK_API_LATENCY = 0.01    # 模拟 API 延迟


def load_documents(file_list):
    """
    批量加载文档，单个失败不影响整体
    这是 RAG 系统中常见的"容错"模式
    """
    loaded = []
    errors = []

    for filename in file_list:
        try:
            # 模拟文件读取
            if filename not in MOCK_FILES:
                raise FileNotFoundError(f"文件不存在: {filename}")

            content = MOCK_FILES[filename]
            if not content.strip():
                raise ValueError(f"文件内容为空: {filename}")

            loaded.append({"filename": filename, "content": content})
            print(f"  [成功] {filename}: {content[:20]}...")

        except FileNotFoundError as e:
            errors.append({"filename": filename, "error": "文件不存在"})
            print(f"  [跳过] {filename}: 文件不存在")

        except ValueError as e:
            errors.append({"filename": filename, "error": "内容为空"})
            print(f"  [跳过] {filename}: 内容为空")

        except Exception as e:
            errors.append({"filename": filename, "error": str(e)})
            print(f"  [错误] {filename}: {e}")

    return loaded, errors


def mock_embed(text):
    """模拟 Embedding API（有概率失败）"""
    time.sleep(MOCK_API_LATENCY)
    if random.random() < 0.2:
        raise APIError("Embedding API 超时")
    return [0.1, 0.2, 0.3]    # 模拟向量


def mock_search(query, documents):
    """模拟检索（有概率失败）"""
    if random.random() < 0.1:
        raise RetrievalError(query, "检索服务不可用")
    # 简单模拟：返回所有文档
    return documents


def rag_pipeline(file_list, query):
    """
    完整的 RAG 管道，每一步都有异常处理
    """
    print(f"\n{'='*40}")
    print(f"  RAG 管道开始运行")
    print(f"  查询: {query}")
    print(f"{'='*40}")

    # 第1步：加载文档（容错模式）
    print(f"\n--- 第1步：加载文档 ---")
    documents, load_errors = load_documents(file_list)
    print(f"  成功: {len(documents)} 个，失败: {len(load_errors)} 个")

    if not documents:
        print("  没有可用文档，管道终止")
        return None

    # 第2步：向量化（带重试）
    print(f"\n--- 第2步：文档向量化 ---")
    embedded_docs = []
    for doc in documents:
        try:
            vector = call_with_retry(mock_embed, doc["content"], max_retries=2, delay=0.05)
            embedded_docs.append({**doc, "vector": vector})
            print(f"  [成功] {doc['filename']} 已向量化")
        except APIError:
            print(f"  [跳过] {doc['filename']} 向量化失败，跳过该文档")

    print(f"  向量化完成: {len(embedded_docs)}/{len(documents)} 个")

    # 第3步：检索（带重试）
    print(f"\n--- 第3步：检索 ---")
    try:
        results = call_with_retry(mock_search, query, embedded_docs, max_retries=2, delay=0.05)
        print(f"  检索到 {len(results)} 个结果")
    except RetrievalError:
        print(f"  检索失败，返回所有文档作为备用")
        results = embedded_docs

    # 第4步：构造上下文
    print(f"\n--- 第4步：构造上下文 ---")
    context = "\n".join([doc["content"] for doc in results])
    print(f"  上下文长度: {len(context)} 字符")

    # 汇总
    print(f"\n{'='*40}")
    print(f"  管道执行完毕")
    print(f"  加载: {len(documents)} | 向量化: {len(embedded_docs)} | 检索: {len(results)}")
    print(f"  加载失败: {len(load_errors)} 个")
    print(f"{'='*40}")

    return results


# 运行管道
random.seed(42)
file_list = ["doc1.txt", "doc2.txt", "doc3.txt", "doc4.txt"]
results = rag_pipeline(file_list, "什么是RAG？")
