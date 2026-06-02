"""
Demo 1: 基础对话 - Chat Completion API
========================================

功能：
- 5行代码让 GPT 回答问题
- 多轮对话，维护 history

前置条件：
- 安装 openai: pip install openai
- 需要 API Key

对应理论：1.Chat Completion API.md
"""

from openai import OpenAI

# ============================================================
# 请填写你的模型配置
# ============================================================
API_KEY = "your-api-key-here"       # 替换为你的 API Key
BASE_URL = "https://api.openai.com/v1"  # 替换为你的 Base URL（如使用代理）
MODEL = "gpt-4o-mini"               # 推荐：gpt-4o-mini（性价比高）或 gpt-4o（更强）

# ============================================================
# 第一部分：5行代码基础对话
# ============================================================
print("=" * 50)
print("第一部分：最简对话（5行代码）")
print("=" * 50)

# 1. 创建客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 2. 发送请求
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "用一句话解释什么是RAG？"}
    ]
)

# 3. 获取回复
answer = response.choices[0].message.content
print(f"\n问题：用一句话解释什么是RAG？")
print(f"回答：{answer}")

# ============================================================
# 第二部分：多轮对话（维护 history）
# ============================================================
print("\n" + "=" * 50)
print("第二部分：多轮对话")
print("=" * 50)

# 对话历史列表，从 system 消息开始
history = [
    {
        "role": "system",
        "content": "你是一个友好的Python老师，用简单的语言解释概念，并举生活中的例子。"
    }
]

def chat(user_message):
    """
    发送消息并获取回复，自动维护对话历史

    参数：
        user_message: 用户输入的消息

    返回：
        AI 的回复内容
    """
    # 1. 将用户消息添加到历史
    history.append({"role": "user", "content": user_message})

    # 2. 调用 API（传入完整的历史记录）
    response = client.chat.completions.create(
        model=MODEL,
        messages=history,        # 传入完整历史，实现上下文连贯
        temperature=0.7,         # 中等创造性
        max_tokens=500           # 限制最大输出长度
    )

    # 3. 获取 AI 回复
    ai_reply = response.choices[0].message.content

    # 4. 将 AI 回复也添加到历史（重要！）
    history.append({"role": "assistant", "content": ai_reply})

    return ai_reply


# 模拟多轮对话
questions = [
    "你好，我刚开始学Python，什么是变量？",
    "那列表和变量有什么区别呢？",
    "能给我一个综合的例子吗？"
]

for i, question in enumerate(questions, 1):
    print(f"\n--- 第{i}轮对话 ---")
    print(f"用户：{question}")

    reply = chat(question)
    print(f"AI：{reply}")

# 打印对话历史长度
print(f"\n--- 对话统计 ---")
print(f"对话历史共 {len(history)} 条消息（含 system 消息）")

# ============================================================
# 第三部分：Temperature 参数对比
# ============================================================
print("\n" + "=" * 50)
print("第三部分：Temperature 参数对比")
print("=" * 50)

test_prompt = "用一个比喻解释什么是机器学习"

for temp in [0, 0.7, 1.2]:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": test_prompt}],
        temperature=temp,
        max_tokens=200
    )
    print(f"\n[Temperature = {temp}]")
    print(response.choices[0].message.content)
