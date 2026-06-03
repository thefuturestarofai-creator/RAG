# ============================================================
# Demo 1: HTTP 请求
# 对应理论文档: 1.HTTP协议.md
# ============================================================
# 用 Python 标准库 urllib 发送 HTTP 请求，
# 调用公开免费 API（不需要 Key）。
# 演示 GET/POST 请求、状态码、请求头、响应解析。
# 需要网络连接，但不需要 API Key。
# ============================================================

import urllib.request
import urllib.parse
import json

# ============================================================
# 1. GET 请求 —— 获取数据
# ============================================================
print("=" * 50)
print("1. GET 请求")
print("=" * 50)

def http_get(url):
    """
    发送 GET 请求并返回响应
    用 urllib 标准库，无需安装第三方包
    """
    try:
        # 创建请求对象（可以自定义请求头）
        req = urllib.request.Request(url, headers={
            "User-Agent": "Python-RAG-Demo/1.0",
            "Accept": "application/json"
        })

        # 发送请求并获取响应
        with urllib.request.urlopen(req, timeout=10) as response:
            # 读取状态码
            status_code = response.getcode()
            # 读取响应头
            headers = dict(response.headers)
            # 读取响应体并解码
            body = response.read().decode("utf-8")

            return {
                "status_code": status_code,
                "headers": headers,
                "body": body
            }
    except urllib.error.HTTPError as e:
        return {"status_code": e.code, "error": f"HTTP Error: {e.code}"}
    except urllib.error.URLError as e:
        return {"status_code": None, "error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"status_code": None, "error": f"Unknown Error: {e}"}


# 示例1: 获取 GitHub 用户信息（免费，不需要 Key）
print("\n--- 请求 GitHub API ---")
url = "https://api.github.com/users/octocat"
print(f"URL: {url}")

result = http_get(url)

if result.get("status_code") == 200:
    data = json.loads(result["body"])
    print(f"状态码: {result['status_code']} OK")
    print(f"用户名: {data.get('login')}")
    print(f"昵称: {data.get('name')}")
    print(f"简介: {data.get('bio')}")
    print(f"公开仓库数: {data.get('public_repos')}")
else:
    print(f"请求失败: {result}")

# 示例2: 获取 GitHub 仓库列表
print("\n--- 请求 GitHub 仓库列表 ---")
url2 = "https://api.github.com/users/octocat/repos?per_page=3"
print(f"URL: {url2}")

result2 = http_get(url2)
if result2.get("status_code") == 200:
    repos = json.loads(result2["body"])
    print(f"状态码: {result2['status_code']} OK")
    print(f"返回了 {len(repos)} 个仓库:")
    for repo in repos:
        print(f"  - {repo['name']}: {repo.get('description', '无描述')[:50]}")
else:
    print(f"请求失败: {result2}")
print()


# ============================================================
# 2. POST 请求 —— 提交数据
# ============================================================
print("=" * 50)
print("2. POST 请求")
print("=" * 50)


def http_post(url, data, headers=None):
    """
    发送 POST 请求
    - url: 请求地址
    - data: 要发送的数据（字典）
    - headers: 请求头
    """
    try:
        # 将数据转为 JSON 字节
        json_data = json.dumps(data).encode("utf-8")

        # 默认请求头
        if headers is None:
            headers = {}
        headers.setdefault("Content-Type", "application/json")
        headers.setdefault("User-Agent", "Python-RAG-Demo/1.0")

        # 创建请求对象
        req = urllib.request.Request(url, data=json_data, headers=headers, method="POST")

        # 发送请求
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            body = response.read().decode("utf-8")
            return {"status_code": status_code, "body": body}

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"status_code": e.code, "error": f"HTTP Error: {e.code}", "body": error_body}
    except urllib.error.URLError as e:
        return {"status_code": None, "error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"status_code": None, "error": f"Unknown Error: {e}"}


# 使用 httpbin.org 测试 POST 请求（免费测试服务）
print("\n--- POST 请求测试（httpbin.org） ---")
post_url = "https://httpbin.org/post"
post_data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "什么是RAG？"}],
    "temperature": 0.7
}
print(f"URL: {post_url}")
print(f"发送数据: {json.dumps(post_data, ensure_ascii=False)[:80]}...")

post_result = http_post(post_url, post_data)
if post_result.get("status_code") == 200:
    response_data = json.loads(post_result["body"])
    print(f"状态码: {post_result['status_code']} OK")
    print(f"服务器收到的数据: {json.dumps(response_data.get('json', {}), ensure_ascii=False)[:100]}...")
    print(f"你的 IP: {response_data.get('origin', '未知')}")
else:
    print(f"请求失败: {post_result}")
print()


# ============================================================
# 3. 解析不同的状态码
# ============================================================
print("=" * 50)
print("3. 状态码演示")
print("=" * 50)

# 模拟不同状态码的处理（用注释说明）
status_code_examples = {
    200: "OK - 请求成功",
    201: "Created - 资源创建成功",
    400: "Bad Request - 请求参数错误",
    401: "Unauthorized - API Key 错误或缺失",
    403: "Forbidden - 没有权限访问",
    404: "Not Found - 资源不存在",
    429: "Too Many Requests - 请求太频繁，需要等待",
    500: "Internal Server Error - 服务器内部错误",
}

print("常见状态码及处理方式:")
for code, desc in status_code_examples.items():
    category = "成功" if 200 <= code < 300 else "客户端错误" if 400 <= code < 500 else "服务端错误" if 500 <= code < 600 else "其他"
    print(f"  [{code}] {desc}")
    print(f"       分类: {category}")
    if code == 401:
        print(f"       处理: 检查 API Key 是否正确")
    elif code == 429:
        print(f"       处理: 等待后重试（指数退避）")
    elif code == 500:
        print(f"       处理: 稍后重试，或联系服务方")
    print()


# ============================================================
# 4. 请求头详解
# ============================================================
print("=" * 50)
print("4. 请求头详解")
print("=" * 50)

headers_explanation = {
    "Content-Type": {
        "值": "application/json",
        "作用": "告诉服务器发送的是 JSON 数据",
        "RAG场景": "调用 API 时必须设置"
    },
    "Authorization": {
        "值": "Bearer sk-xxxxxxxxxx",
        "作用": "API Key 认证，证明你有权访问",
        "RAG场景": "调用 OpenAI API 时必须携带"
    },
    "Accept": {
        "值": "application/json",
        "作用": "告诉服务器你希望收到 JSON 格式的响应",
        "RAG场景": "确保 API 返回 JSON 而不是 HTML"
    },
    "User-Agent": {
        "值": "MyRAGApp/1.0",
        "作用": "告诉服务器你是谁（客户端信息）",
        "RAG场景": "用于日志记录和调试"
    }
}

print("RAG 项目中常用的请求头:")
for header, info in headers_explanation.items():
    print(f"\n  {header}:")
    print(f"    示例值: {info['值']}")
    print(f"    作用: {info['作用']}")
    print(f"    RAG场景: {info['RAG场景']}")
print()


# ============================================================
# 5. 综合示例：模拟 RAG 中的 API 调用流程
# ============================================================
print("=" * 50)
print("综合示例：模拟 RAG 中的 API 调用流程")
print("=" * 50)


def simulate_api_call_with_retry(url, data, max_retries=3):
    """
    模拟带重试的 API 调用（RAG 中的标准模式）
    """
    import time

    for attempt in range(max_retries):
        print(f"\n  第 {attempt + 1} 次尝试...")
        print(f"  请求: POST {url}")
        print(f"  数据: {json.dumps(data, ensure_ascii=False)[:60]}...")

        result = http_post(url, data)
        status = result.get("status_code")

        print(f"  响应状态码: {status}")

        if status == 200:
            print(f"  请求成功!")
            return json.loads(result["body"])
        elif status == 429:
            wait = 2 ** attempt
            print(f"  被限流，等待 {wait} 秒后重试...")
            time.sleep(wait)
        elif status and 400 <= status < 500:
            print(f"  客户端错误 ({status})，不重试")
            return None
        else:
            wait = 2 ** attempt
            print(f"  服务端错误，等待 {wait} 秒后重试...")
            time.sleep(wait)

    print(f"\n  重试 {max_retries} 次后仍然失败")
    return None


# 用 httpbin 模拟 API 调用
print("\n模拟 RAG 系统调用 LLM API:")
mock_api_data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "你是一个RAG技术专家"},
        {"role": "user", "content": "用一句话解释RAG"}
    ],
    "temperature": 0.7
}

response = simulate_api_call_with_retry("https://httpbin.org/post", mock_api_data)

if response:
    print(f"\n模拟 LLM 响应（httpbin 回显数据）:")
    sent_data = response.get("json", {})
    print(f"  模型: {sent_data.get('model')}")
    print(f"  消息: {sent_data.get('messages')}")
else:
    print("模拟 API 调用失败")
