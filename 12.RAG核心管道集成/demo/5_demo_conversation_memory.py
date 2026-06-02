"""
============================================================
Demo 5: 多轮对话记忆 —— 三种记忆模式对比演示
============================================================

本 Demo 展示 RAG 系统中三种对话记忆模式的实现和对比：
1. ConversationBufferMemory（全量保存）
2. ConversationSummaryMemory（摘要压缩）
3. ConversationBufferWindowMemory（滑动窗口）

不需要 API Key，所有 LLM 调用都用模拟函数替代。
"""

from abc import ABC, abstractmethod
from typing import List, Tuple


# ============================================================
# 第一部分：基础组件定义
# ============================================================

def mock_llm(prompt: str) -> str:
    """
    模拟 LLM 调用（不需要 API Key）。
    实际项目中，这里会调用 OpenAI、Claude 等大模型。
    """
    # 根据 prompt 内容返回模拟回答
    if "摘要" in prompt or "总结" in prompt:
        # 模拟摘要生成
        if "用户在了解" in prompt:
            return "用户正在学习 RAG 技术，已讨论了 RAG 定义、核心流程和检索阶段。"
        return "对话摘要：用户在进行技术学习讨论。"
    elif "LangChain" in prompt and "安装" in prompt:
        return "LangChain 可以通过 pip install langchain 安装。建议同时安装 langchain-community 和 langchain-openai。"
    elif "RAG" in prompt and "流程" in prompt:
        return "RAG 的核心流程包括：1.文档加载 2.文本切分 3.Embedding向量化 4.向量存储 5.相似度检索 6.LLM生成回答。"
    elif "检索" in prompt:
        return "检索阶段主要使用向量相似度匹配。将用户问题转为向量，在向量数据库中找到最相似的文档片段。"
    elif "RAG" in prompt:
        return "RAG（检索增强生成）是一种结合检索和生成的AI技术，通过检索外部知识库来增强LLM的回答质量。"
    elif "它怎么安装" in prompt:
        return "抱歉，我不确定'它'指的是什么，请明确说明。"
    else:
        return "这是一个模拟回答。实际项目中会调用真实的 LLM。"


# 定义对话轮次的类型
ChatTurn = Tuple[str, str]  # (用户问题, AI回答)


# ============================================================
# 第二部分：三种记忆模式实现
# ============================================================

class BaseMemory(ABC):
    """记忆基类：定义统一接口"""

    def __init__(self):
        self.chat_history: List[ChatTurn] = []

    def add_turn(self, user_msg: str, ai_msg: str):
        """添加一轮对话"""
        self.chat_history.append((user_msg, ai_msg))

    @abstractmethod
    def get_history(self) -> str:
        """获取格式化的对话历史（子类实现）"""
        pass

    def get_turn_count(self) -> int:
        """获取对话轮次数"""
        return len(self.chat_history)

    def get_token_estimate(self) -> int:
        """估算 Token 消耗（中文按字符数估算）"""
        history_text = self.get_history()
        return len(history_text)


class ConversationBufferMemory(BaseMemory):
    """
    模式一：全量保存（ConversationBufferMemory）

    类比：记所有笔记 —— 每页都保留，一字不漏。
    特点：信息完整，但 Token 消耗随对话线性增长。
    适用：短对话场景（<10轮）。
    """

    def get_history(self) -> str:
        """将所有对话历史原封不动地格式化输出"""
        if not self.chat_history:
            return "（暂无对话历史）"

        lines = []
        for user_msg, ai_msg in self.chat_history:
            lines.append(f"用户：{user_msg}")
            lines.append(f"AI：{ai_msg}")
        return "\n".join(lines)


class ConversationSummaryMemory(BaseMemory):
    """
    模式二：摘要压缩（ConversationSummaryMemory）

    类比：每页写总结 —— 定期将对话压缩成摘要。
    特点：Token 消耗增长缓慢，但细节可能丢失。
    适用：长对话场景（>20轮）。

    实现原理：
    - 每次添加新对话时，用 LLM 将历史 + 新对话压缩成摘要
    - 摘要长度相对固定，不会随对话轮次无限增长
    """

    def __init__(self, llm_func=None):
        super().__init__()
        self.summary = ""  # 当前摘要
        self.llm_func = llm_func or mock_llm  # 用于生成摘要的 LLM

    def add_turn(self, user_msg: str, ai_msg: str):
        """添加对话并更新摘要"""
        super().add_turn(user_msg, ai_msg)
        # 每次添加对话后，重新生成摘要
        self._update_summary()

    def _update_summary(self):
        """用 LLM 将对话历史压缩成摘要"""
        # 构造摘要生成的 Prompt
        history_text = self._format_raw_history()
        prompt = f"""请将以下对话历史压缩成一段简短的摘要，保留关键信息：

{history_text}

摘要："""
        # 调用 LLM 生成摘要
        self.summary = self.llm_func(prompt)

    def _format_raw_history(self) -> str:
        """格式化原始对话历史"""
        lines = []
        if self.summary:
            lines.append(f"之前的摘要：{self.summary}")
            lines.append("")
        for user_msg, ai_msg in self.chat_history:
            lines.append(f"用户：{user_msg}")
            lines.append(f"AI：{ai_msg}")
        return "\n".join(lines)

    def get_history(self) -> str:
        """返回压缩后的摘要（而不是完整历史）"""
        if not self.summary:
            return "（暂无对话历史）"
        return f"[对话摘要] {self.summary}"


class ConversationBufferWindowMemory(BaseMemory):
    """
    模式三：滑动窗口（ConversationBufferWindowMemory）

    类比：只保留最近N页笔记 —— 早期的笔记全部丢弃。
    特点：Token 消耗固定，但早期信息完全丢失。
    适用：对话主题经常切换的场景。
    """

    def __init__(self, k: int = 3):
        """
        Args:
            k: 窗口大小，保留最近 k 轮对话
        """
        super().__init__()
        self.k = k

    def get_history(self) -> str:
        """只返回最近 k 轮对话"""
        if not self.chat_history:
            return "（暂无对话历史）"

        # 只取最近 k 轮
        recent_turns = self.chat_history[-self.k:]

        lines = []
        if len(self.chat_history) > self.k:
            lines.append(f"（注：已省略前 {len(self.chat_history) - self.k} 轮对话）")
            lines.append("")

        for user_msg, ai_msg in recent_turns:
            lines.append(f"用户：{user_msg}")
            lines.append(f"AI：{ai_msg}")
        return "\n".join(lines)


# ============================================================
# 第三部分：RAG 管道中的对话记忆集成
# ============================================================

class RAGWithMemory:
    """
    带对话记忆的 RAG 管道

    展示如何将对话记忆集成到 RAG 的 Prompt 中。
    核心流程：
    1. 用户提问
    2. 加载对话历史
    3. 构造带历史的 Prompt
    4. LLM 生成回答
    5. 存入记忆
    """

    def __init__(self, memory: BaseMemory, llm_func=None):
        self.memory = memory
        self.llm_func = llm_func or mock_llm

        # 模拟知识库（实际项目中是向量数据库）
        self.knowledge_base = {
            "RAG": "RAG（检索增强生成）是一种结合检索和生成的AI技术。核心流程包括文档加载、文本切分、Embedding向量化、向量存储、相似度检索和LLM生成回答。",
            "LangChain": "LangChain 是一个用于构建 LLM 应用的开源框架，核心组件包括 Model I/O、Retrieval、Memory、Chains 等模块。",
            "检索": "检索阶段主要使用向量相似度匹配。将用户问题转为向量，在向量数据库中找到最相似的文档片段返回给 LLM。",
        }

    def _retrieve(self, query: str) -> str:
        """模拟检索：根据关键词匹配知识库"""
        for key, value in self.knowledge_base.items():
            if key in query:
                return value
        return "未找到相关信息。"

    def chat(self, user_question: str) -> str:
        """
        处理用户提问（带对话记忆）

        这是 RAG + 对话记忆的核心集成方式：
        将对话历史注入到 Prompt 中，让 LLM 参考历史回答
        """
        # 步骤1：检索相关文档
        context = self._retrieve(user_question)

        # 步骤2：加载对话历史
        chat_history = self.memory.get_history()

        # 步骤3：构造带对话历史的 Prompt（核心！）
        prompt = f"""你是一个知识助手。根据以下参考资料和对话历史回答用户问题。

=== 对话历史 ===
{chat_history}

=== 参考资料 ===
{context}

=== 用户问题 ===
{user_question}

请回答："""

        # 步骤4：调用 LLM 生成回答
        answer = self.llm_func(prompt)

        # 步骤5：将本轮对话存入记忆
        self.memory.add_turn(user_question, answer)

        return answer


# ============================================================
# 第四部分：演示运行
# ============================================================

def print_separator(title: str):
    """打印分隔线"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_three_memories():
    """
    演示三种记忆模式的对比
    """
    print_separator("三种记忆模式对比演示")

    # 模拟一段多轮对话
    conversations = [
        ("你好，介绍一下 RAG", None),
        ("它的核心流程是什么？", None),
        ("能详细说说检索阶段吗？", None),
        ("它怎么安装？", None),       # 注意："它"指代不明
    ]

    # --- 模式1：全量保存 ---
    print("【模式1：ConversationBufferMemory（全量保存）】")
    print("类比：记所有笔记，一字不漏\n")

    buffer_memory = ConversationBufferMemory()
    for user_msg, _ in conversations:
        # 模拟 AI 回答
        ai_msg = mock_llm(user_msg)
        buffer_memory.add_turn(user_msg, ai_msg)
        print(f"  用户：{user_msg}")
        print(f"  AI：{ai_msg}")
        print(f"  当前记忆长度：{buffer_memory.get_token_estimate()} 字符")
        print()

    print(f"  最终对话历史：")
    print(f"  {buffer_memory.get_history()}")
    print(f"  Token 消耗估算：{buffer_memory.get_token_estimate()} 字符\n")

    # --- 模式2：摘要压缩 ---
    print("\n【模式2：ConversationSummaryMemory（摘要压缩）】")
    print("类比：每页写总结，定期压缩\n")

    summary_memory = ConversationSummaryMemory(llm_func=mock_llm)
    for user_msg, _ in conversations:
        ai_msg = mock_llm(user_msg)
        summary_memory.add_turn(user_msg, ai_msg)
        print(f"  用户：{user_msg}")
        print(f"  AI：{ai_msg}")
        print(f"  当前摘要：{summary_memory.summary}")
        print()

    print(f"  最终对话历史（摘要）：")
    print(f"  {summary_memory.get_history()}")
    print(f"  Token 消耗估算：{summary_memory.get_token_estimate()} 字符\n")

    # --- 模式3：滑动窗口 ---
    print("\n【模式3：ConversationBufferWindowMemory（滑动窗口 k=2）】")
    print("类比：只保留最近2页笔记\n")

    window_memory = ConversationBufferWindowMemory(k=2)
    for user_msg, _ in conversations:
        ai_msg = mock_llm(user_msg)
        window_memory.add_turn(user_msg, ai_msg)
        print(f"  用户：{user_msg}")
        print(f"  AI：{ai_msg}")
        print(f"  窗口内轮次：{min(window_memory.get_turn_count(), window_memory.k)}")
        print()

    print(f"  最终对话历史（最近2轮）：")
    print(f"  {window_memory.get_history()}")
    print(f"  Token 消耗估算：{window_memory.get_token_estimate()} 字符\n")


def demo_rag_with_memory():
    """
    演示 RAG 管道中集成对话记忆
    """
    print_separator("RAG 管道 + 对话记忆 集成演示")

    # 使用全量保存模式
    memory = ConversationBufferMemory()
    rag = RAGWithMemory(memory=memory, llm_func=mock_llm)

    # 多轮对话
    questions = [
        "介绍一下 RAG",
        "它的核心流程是什么？",
        "能详细说说检索吗？",
    ]

    for i, question in enumerate(questions, 1):
        print(f"--- 第{i}轮对话 ---")
        print(f"用户：{question}")
        answer = rag.chat(question)
        print(f"AI：{answer}")
        print(f"当前 Prompt 中的对话历史：")
        print(f"  {memory.get_history()}")
        print()


def demo_token_growth():
    """
    演示三种模式的 Token 增长曲线
    """
    print_separator("Token 增长对比")

    buffer = ConversationBufferMemory()
    summary = ConversationSummaryMemory(llm_func=mock_llm)
    window = ConversationBufferWindowMemory(k=3)

    print(f"{'轮次':<6} {'全量保存':<12} {'摘要压缩':<12} {'滑动窗口(k=3)':<14}")
    print("-" * 46)

    for i in range(1, 11):
        user_msg = f"第{i}轮用户问题"
        ai_msg = f"第{i}轮AI回答内容"

        buffer.add_turn(user_msg, ai_msg)
        summary.add_turn(user_msg, ai_msg)
        window.add_turn(user_msg, ai_msg)

        print(f"{i:<6} {buffer.get_token_estimate():<12} {summary.get_token_estimate():<12} {window.get_token_estimate():<14}")

    print()
    print("观察：全量保存线性增长，摘要压缩缓慢增长，滑动窗口趋于稳定。")


def demo_memory_in_prompt():
    """
    演示对话历史如何被注入到 RAG 的 Prompt 中
    """
    print_separator("对话历史注入 Prompt 演示")

    memory = ConversationBufferMemory()
    rag = RAGWithMemory(memory=memory, llm_func=mock_llm)

    # 先进行几轮对话建立历史
    rag.chat("介绍一下 RAG")
    rag.chat("它的核心流程是什么？")

    # 展示 Prompt 的构造过程
    chat_history = memory.get_history()
    context = rag._retrieve("能详细说说检索吗？")

    print("【构造的完整 Prompt 示例】\n")
    prompt = f"""你是一个知识助手。根据以下参考资料和对话历史回答用户问题。

=== 对话历史 ===
{chat_history}

=== 参考资料 ===
{context}

=== 用户问题 ===
能详细说说检索吗？

请回答："""

    print(prompt)
    print("\n---")
    print("可以看到，对话历史被完整地注入到了 Prompt 中，")
    print("LLM 可以参考之前的对话来理解用户的追问。")


# ============================================================
# 主程序入口
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  RAG 多轮对话记忆 Demo")
    print("  三种记忆模式对比 + RAG 管道集成")
    print("=" * 60)

    # 演示1：三种记忆模式对比
    demo_three_memories()

    # 演示2：RAG 管道集成对话记忆
    demo_rag_with_memory()

    # 演示3：Token 增长对比
    demo_token_growth()

    # 演示4：对话历史注入 Prompt
    demo_memory_in_prompt()

    print_separator("Demo 完成")
    print("关键要点：")
    print("1. ConversationBufferMemory：全量保存，适合短对话")
    print("2. ConversationSummaryMemory：摘要压缩，适合长对话")
    print("3. ConversationBufferWindowMemory：滑动窗口，适合主题切换")
    print("4. 核心集成方式：将对话历史注入到 RAG 的 Prompt 中")
    print("5. 配合查询改写技术，可以处理指代性问题")
