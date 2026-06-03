"""
Demo 1: 最简 Chain - PromptTemplate | LLM 的 LCEL 管道
======================================================

功能：
- 使用 LCEL 管道语法创建最简单的 Chain
- 演示 PromptTemplate 的使用

前置条件：
- pip install langchain langchain-openai langchain-core
- 需要 API Key

对应理论：1.Chain与LCEL.md

使用的版本（建议）：
- langchain>=0.2.0
- langchain-openai>=0.1.0
- langchain-core>=0.2.0
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ============================================================
# 请填写你的模型配置
# ============================================================
API_KEY = "your-api-key-here"       # 替换为你的 API Key
BASE_URL = "https://api.openai.com/v1"  # 替换为你的 Base URL
MODEL = "gpt-4o-mini"               # 推荐：gpt-4o-mini（性价比高）或 gpt-4o（更强）


# ============================================================
# 第一部分：最简 LCEL 管道
# ============================================================
print("=" * 50)
print("第一部分：最简 LCEL 管道")
print("=" * 50)

# 1. 创建模型
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    model=MODEL,
    temperature=0.7
)

# 2. 创建 PromptTemplate
prompt = PromptTemplate.from_template(
    "请用一句话解释什么是{concept}？"
)

# 3. 用 | 管道符连接：Prompt → LLM → 输出解析
chain = prompt | llm | StrOutputParser()

# 4. 运行 Chain
result = chain.invoke({"concept": "向量数据库"})
print(f"\n问题：什么是向量数据库？")
print(f"回答：{result}")


# ============================================================
# 第二部分：ChatPromptTemplate（多角色）
# ============================================================
print("\n" + "=" * 50)
print("第二部分：ChatPromptTemplate（多角色）")
print("=" * 50)

# 使用 ChatPromptTemplate 定义多角色提示
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{domain}领域的专家，请用通俗易懂的语言回答问题。"),
    ("user", "{question}")
])

# 组合成 Chain
expert_chain = chat_prompt | llm | StrOutputParser()

# 测试不同领域
result = expert_chain.invoke({
    "domain": "人工智能",
    "question": "RAG是什么？有什么用？"
})
print(f"\n[AI专家] RAG是什么？有什么用？")
print(f"回答：{result}")


# ============================================================
# 第三部分：链式组合（多步管道）
# ============================================================
print("\n" + "=" * 50)
print("第三部分：链式组合（多步管道）")
print("=" * 50)

# 第一步：生成大纲
outline_prompt = PromptTemplate.from_template(
    "请为'{topic}'这个主题列出3个要点，只列出要点，不要展开。"
)
outline_chain = outline_prompt | llm | StrOutputParser()

# 第二步：根据大纲展开
expand_prompt = PromptTemplate.from_template(
    "请根据以下大纲，为每个要点写一段简要说明：\n\n大纲：\n{outline}"
)
expand_chain = expand_prompt | llm | StrOutputParser()

# 执行多步链
topic = "Python虚拟环境"
print(f"\n主题：{topic}")

# 第一步
outline = outline_chain.invoke({"topic": topic})
print(f"\n第一步 - 生成大纲：\n{outline}")

# 第二步
expanded = expand_chain.invoke({"outline": outline})
print(f"\n第二步 - 展开说明：\n{expanded}")


# ============================================================
# 第四部分：流式输出
# ============================================================
print("\n" + "=" * 50)
print("第四部分：流式输出")
print("=" * 50)

simple_chain = PromptTemplate.from_template(
    "用100字左右介绍{topic}"
) | llm | StrOutputParser()

print("\n流式输出效果：")
# 使用 stream 方法，逐 token 输出
for chunk in simple_chain.stream({"topic": "LangChain框架"}):
    print(chunk, end="", flush=True)
print()  # 换行
