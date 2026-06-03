# ============================================================
# Demo 2: JSON 处理
# 对应理论文档: 2.API概念.md
# ============================================================
# 演示 JSON 数据的解析、构造、转换。
# 模拟处理 API 返回的 JSON 数据，提取有用信息，构造新的 JSON 请求。
# 不需要 API Key，不需要网络。
# ============================================================

import json

# ============================================================
# 1. JSON 基础：Python 字典与 JSON 的转换
# ============================================================
print("=" * 50)
print("1. JSON 基础：字典与 JSON 的转换")
print("=" * 50)

# Python 字典
data = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "messages": [
        {"role": "user", "content": "什么是RAG？"}
    ],
    "stream": False
}

# 字典 → JSON 字符串
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(f"JSON 字符串:\n{json_str}\n")

# JSON 字符串 → 字典
parsed = json.loads(json_str)
print(f"解析后类型: {type(parsed)}")
print(f"模型: {parsed['model']}")
print(f"温度: {parsed['temperature']}")
print(f"消息: {parsed['messages'][0]['content']}")
print()


# ============================================================
# 2. 处理嵌套的 JSON 数据
# ============================================================
print("=" * 50)
print("2. 处理嵌套的 JSON 数据")
print("=" * 50)

# 模拟 OpenAI API 的响应
api_response = {
    "id": "chatcmpl-abc123",
    "object": "chat.completion",
    "created": 1700000000,
    "model": "gpt-3.5-turbo",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "RAG（检索增强生成）是一种结合信息检索和文本生成的技术。"
                           "它通过从外部知识库中检索相关文档，将其作为上下文提供给大语言模型，"
                           "从而生成更准确、更有依据的回答。"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 50,
        "completion_tokens": 80,
        "total_tokens": 130
    }
}

# 提取有用信息
print("从 API 响应中提取信息:")
content = api_response["choices"][0]["message"]["content"]
finish_reason = api_response["choices"][0]["finish_reason"]
total_tokens = api_response["usage"]["total_tokens"]

print(f"  回答内容: {content[:50]}...")
print(f"  结束原因: {finish_reason}")
print(f"  Token 消耗: {total_tokens}")
print()


# ============================================================
# 3. 安全地访问 JSON 数据（避免 KeyError）
# ============================================================
print("=" * 50)
print("3. 安全地访问 JSON 数据")
print("=" * 50)

# 不安全的访问方式
print("不安全的方式:")
try:
    value = api_response["choices"][0]["message"]["tool_calls"]
except KeyError as e:
    print(f"  KeyError: {e} —— 这个字段不存在\n")

# 安全的方式1: 使用 dict.get()
print("安全方式1: get() 方法")
tool_calls = api_response.get("choices", [{}])[0].get("message", {}).get("tool_calls", None)
print(f"  tool_calls: {tool_calls}")    # None（不会报错）

# 安全的方式2: 使用 try/except
print("\n安全方式2: try/except")
try:
    tool_calls = api_response["choices"][0]["message"]["tool_calls"]
    print(f"  tool_calls: {tool_calls}")
except (KeyError, IndexError):
    print("  字段不存在，使用默认值")

# 安全的方式3: 封装成函数
print("\n安全方式3: 封装成函数")


def safe_get(data, *keys, default=None):
    """
    安全地从嵌套字典中获取值
    用法: safe_get(data, "choices", 0, "message", "content")
    """
    current = data
    for key in keys:
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError):
            return default
    return current


# 使用示例
content = safe_get(api_response, "choices", 0, "message", "content", default="无内容")
model = safe_get(api_response, "model", default="未知模型")
missing = safe_get(api_response, "choices", 0, "message", "tool_calls", default="无")

print(f"  content: {content[:40]}...")
print(f"  model: {model}")
print(f"  tool_calls: {missing}")
print()


# ============================================================
# 4. 构造 JSON 请求
# ============================================================
print("=" * 50)
print("4. 构造 JSON 请求")
print("=" * 50)


def build_chat_request(question, context="", model="gpt-3.5-turbo", temperature=0.7):
    """
    构造 RAG 系统的 Chat API 请求
    这是 RAG 中构造 Prompt 的标准方式
    """
    system_prompt = "你是一个知识问答助手。请根据提供的上下文回答问题。"

    if context:
        system_prompt += f"\n\n参考上下文:\n{context}"

    request = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "max_tokens": 500
    }

    return request


# 构造请求
context = "RAG是检索增强生成技术，通过检索外部知识来增强大模型的回答。"
question = "RAG的核心思想是什么？"

request = build_chat_request(question, context=context)
print("构造的 API 请求:")
print(json.dumps(request, ensure_ascii=False, indent=2))
print()


# ============================================================
# 5. 批量处理 JSON 数据
# ============================================================
print("=" * 50)
print("5. 批量处理 JSON 数据")
print("=" * 50)

# 模拟多个 API 响应
responses = [
    {"choices": [{"message": {"content": "RAG是检索增强生成"}}], "usage": {"total_tokens": 100}},
    {"choices": [{"message": {"content": "向量数据库存储Embedding"}}], "usage": {"total_tokens": 120}},
    {"choices": [{"message": {"content": "LangChain是开发框架"}}], "usage": {"total_tokens": 90}},
]

# 提取所有回答
print("批量提取回答:")
answers = []
total_tokens = 0

for i, resp in enumerate(responses):
    answer = safe_get(resp, "choices", 0, "message", "content", default="无回答")
    tokens = safe_get(resp, "usage", "total_tokens", default=0)
    answers.append(answer)
    total_tokens += tokens
    print(f"  回答 {i+1}: {answer} (消耗 {tokens} tokens)")

print(f"\n总 Token 消耗: {total_tokens}")
print()


# ============================================================
# 6. JSON 文件读写
# ============================================================
print("=" * 50)
print("6. JSON 文件读写")
print("=" * 50)

# 写入 JSON 文件
config = {
    "rag_config": {
        "chunk_size": 500,
        "chunk_overlap": 50,
        "top_k": 3,
        "similarity_threshold": 0.7
    },
    "models": {
        "embedding": "text-embedding-ada-002",
        "llm": "gpt-3.5-turbo"
    },
    "vector_db": {
        "type": "chroma",
        "persist_dir": "./chroma_db"
    }
}

config_path = "demo_config.json"
with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
print(f"配置已写入: {config_path}")

# 读取 JSON 文件
with open(config_path, "r", encoding="utf-8") as f:
    loaded_config = json.load(f)

print(f"读取配置:")
print(f"  chunk_size: {loaded_config['rag_config']['chunk_size']}")
print(f"  embedding模型: {loaded_config['models']['embedding']}")
print(f"  向量数据库: {loaded_config['vector_db']['type']}")

# 清理
import os
os.remove(config_path)
print(f"\n已清理: {config_path}")
print()


# ============================================================
# 7. 综合示例：RAG 管道中的 JSON 数据流
# ============================================================
print("=" * 50)
print("综合示例：RAG 管道中的 JSON 数据流")
print("=" * 50)


def simulate_rag_data_flow():
    """
    模拟 RAG 系统中完整的 JSON 数据流：
    1. 构造 Embedding 请求
    2. 解析 Embedding 响应
    3. 构造检索请求
    4. 解析检索响应
    5. 构造 LLM 请求
    6. 解析 LLM 响应
    """
    print("\n--- 第1步：构造 Embedding 请求 ---")
    embedding_request = {
        "input": "什么是RAG？",
        "model": "text-embedding-ada-002"
    }
    print(f"请求: {json.dumps(embedding_request, ensure_ascii=False)}")

    print("\n--- 第2步：模拟 Embedding 响应 ---")
    embedding_response = {
        "data": [{"embedding": [0.1, 0.2, 0.3, 0.4, 0.5], "index": 0}],
        "model": "text-embedding-ada-002",
        "usage": {"prompt_tokens": 5, "total_tokens": 5}
    }
    query_vector = safe_get(embedding_response, "data", 0, "embedding", default=[])
    print(f"向量维度: {len(query_vector)}")
    print(f"向量前3维: {query_vector[:3]}")

    print("\n--- 第3步：构造检索请求 ---")
    search_request = {
        "vector": query_vector,
        "top_k": 3,
        "collection": "knowledge_base"
    }
    print(f"检索请求: top_k={search_request['top_k']}, collection={search_request['collection']}")

    print("\n--- 第4步：模拟检索响应 ---")
    search_response = {
        "results": [
            {"content": "RAG是检索增强生成技术", "score": 0.95, "source": "doc1.txt"},
            {"content": "向量数据库用于存储Embedding", "score": 0.87, "source": "doc2.txt"},
            {"content": "LangChain是大模型开发框架", "score": 0.82, "source": "doc3.txt"},
        ]
    }
    results = search_response["results"]
    print(f"检索到 {len(results)} 条结果:")
    for r in results:
        print(f"  [{r['score']}] {r['content']}")

    print("\n--- 第5步：构造 LLM 请求 ---")
    context = "\n".join([r["content"] for r in results])
    llm_request = build_chat_request(
        question="什么是RAG？",
        context=context,
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    print(f"LLM 请求: model={llm_request['model']}, 消息数={len(llm_request['messages'])}")

    print("\n--- 第6步：模拟 LLM 响应 ---")
    llm_response = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "RAG（检索增强生成）是一种通过检索外部知识库来增强大语言模型回答质量的技术。"
            },
            "finish_reason": "stop"
        }],
        "usage": {"total_tokens": 150}
    }
    final_answer = safe_get(llm_response, "choices", 0, "message", "content", default="无回答")
    total_tokens = safe_get(llm_response, "usage", "total_tokens", default=0)

    print(f"\n最终回答: {final_answer}")
    print(f"Token 消耗: {total_tokens}")

    # 保存完整对话记录为 JSON
    conversation_log = {
        "question": "什么是RAG？",
        "context": context,
        "answer": final_answer,
        "sources": [r["source"] for r in results],
        "tokens_used": total_tokens
    }
    print(f"\n对话记录（可保存为JSON）:")
    print(json.dumps(conversation_log, ensure_ascii=False, indent=2))


simulate_rag_data_flow()
