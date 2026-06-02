chunks = [
    "RAG（检索增强生成）是一种AI技术架构。",
    "它通过检索外部知识库来增强大语言模型的回答。",
    "核心流程：用户提问 → 检索相关文档 → 将文档作为上下文 → LLM生成回答。",
    "优势：减少幻觉、知识可更新、回答可溯源。",
]
print("\n遍历所有文档块:")
for i, chunk in enumerate(chunks):
    print(f"  [块 {i}] {chunk}")
