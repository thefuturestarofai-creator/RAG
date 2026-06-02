"""
Demo 2: Gradio RAG 界面

本 Demo 用 Gradio 的 ChatInterface 实现 RAG 聊天界面。
功能包括：
1. 聊天界面（支持多轮对话）
2. 流式输出
3. 自定义设置

用法：
    python 2_demo_gradio_rag.py

需要 API Key：
    - OPENAI_API_KEY：用于 Embedding 和 LLM
    - OPENAI_BASE_URL：API 地址
    - MODEL：使用的模型名称
"""

import os
import sys
import time

# ============================================================
# 配置区域
# ============================================================

API_KEY = os.getenv("OPENAI_API_KEY", "sk-your-api-key-here")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# ============================================================
# 检查 Gradio 是否安装
# ============================================================

try:
    import gradio as gr
except ImportError:
    print("=" * 60)
    print("  需要安装 Gradio")
    print("=" * 60)
    print("""
  安装命令:
    pip install gradio

  运行命令:
    python 2_demo_gradio_rag.py
    """)
    sys.exit(0)


# ============================================================
# RAG 调用逻辑
# ============================================================

def call_rag_api(question: str, model: str = "gpt-3.5-turbo", top_k: int = 3) -> dict:
    """
    调用 RAG API（模拟实现）。

    实际项目中，这里应该调用后端的 RAG 服务。
    """
    # 模拟回答
    if "rag" in question.lower() or "RAG" in question:
        return {
            "answer": f"RAG（Retrieval-Augmented Generation，检索增强生成）"
                      f"是一种结合信息检索和文本生成的技术框架。\n\n"
                      f"核心流程：\n"
                      f"1. 将文档加载、切分、向量化后存入向量数据库\n"
                      f"2. 用户提问时，从向量数据库中检索相关文档\n"
                      f"3. 将检索到的文档与问题一起输入 LLM 生成回答\n\n"
                      f"优势：知识可更新、减少幻觉、可追溯、成本低。",
            "sources": [
                {"filename": "RAG技术白皮书.txt", "relevance": 0.95},
                {"filename": "向量数据库说明.txt", "relevance": 0.87},
            ]
        }
    else:
        return {
            "answer": f"这是关于「{question}」的回答。\n\n"
                      f"在实际项目中，这里会调用后端 RAG 服务。",
            "sources": [{"filename": "示例文档.txt", "relevance": 0.80}]
        }


# ============================================================
# 方式一：ChatInterface（最简洁）
# ============================================================

def create_chat_interface():
    """创建 ChatInterface 聊天界面。"""

    def chat(message, history):
        """
        ChatInterface 的处理函数。

        Args:
            message: 用户当前消息
            history: 聊天历史 [(用户消息, AI回复), ...]
        """
        result = call_rag_api(message)

        # 格式化回答（包含来源）
        answer = result["answer"]
        if result.get("sources"):
            answer += "\n\n---\n📎 参考来源："
            for source in result["sources"]:
                answer += f"\n- {source['filename']} (相关度: {source['relevance']:.2f})"

        return answer

    demo = gr.ChatInterface(
        fn=chat,
        title="🤖 RAG 知识库助手",
        description="基于检索增强生成的智能问答系统",
        examples=[
            "什么是RAG？",
            "向量数据库怎么选？",
            "LangChain 是什么？",
        ],
        retry_btn="🔄 重新生成",
        undo_btn="↩️ 撤销",
        clear_btn="🗑️ 清空对话",
    )

    return demo


# ============================================================
# 方式二：Blocks（自定义布局）
# ============================================================

def create_blocks_interface():
    """创建 Blocks 自定义界面。"""

    with gr.Blocks(title="RAG 知识库问答系统", theme=gr.themes.Soft()) as demo:
        # 标题
        gr.Markdown("# 🤖 RAG 知识库问答系统")
        gr.Markdown("基于检索增强生成的智能问答系统 | 支持多轮对话")

        with gr.Row():
            # 左侧：聊天区域
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    height=500,
                    show_label=False,
                    bubble_full_width=False,
                )
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="请输入问题...",
                        show_label=False,
                        scale=9,
                    )
                    submit_btn = gr.Button("发送", variant="primary", scale=1)

                with gr.Row():
                    retry_btn = gr.Button("🔄 重新生成")
                    undo_btn = gr.Button("↩️ 撤销")
                    clear_btn = gr.Button("🗑️ 清空")

            # 右侧：设置区域
            with gr.Column(scale=1):
                gr.Markdown("## ⚙️ 设置")

                model = gr.Dropdown(
                    choices=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
                    value="gpt-3.5-turbo",
                    label="模型",
                )
                top_k = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=3,
                    step=1,
                    label="检索数量 (top_k)",
                )
                temperature = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.3,
                    step=0.1,
                    label="温度",
                )

                gr.Markdown("## 📊 对话统计")
                stats = gr.Markdown("对话轮数: 0")

        # 状态管理
        chat_history = gr.State([])

        # 事件处理
        def respond(message, history, chat_hist, model_val, top_k_val):
            if not message:
                return "", history, chat_hist, f"对话轮数: {len(chat_hist)}"

            # 调用 RAG
            result = call_rag_api(message, model_val, top_k_val)
            answer = result["answer"]

            # 添加来源
            if result.get("sources"):
                answer += "\n\n---\n📎 参考来源："
                for source in result["sources"]:
                    answer += f"\n- {source['filename']} (相关度: {source['relevance']:.2f})"

            # 更新历史
            history.append((message, answer))
            chat_hist.append({"user": message, "assistant": answer})

            return "", history, chat_hist, f"对话轮数: {len(chat_hist)}"

        def undo(history, chat_hist):
            if history:
                history.pop()
                chat_hist.pop()
            return history, chat_hist, f"对话轮数: {len(chat_hist)}"

        def clear():
            return [], [], "对话轮数: 0"

        # 绑定事件
        msg.submit(
            respond,
            [msg, chatbot, chat_history, model, top_k],
            [msg, chatbot, chat_history, stats],
        )
        submit_btn.click(
            respond,
            [msg, chatbot, chat_history, model, top_k],
            [msg, chatbot, chat_history, stats],
        )
        undo_btn.click(undo, [chatbot, chat_history], [chatbot, chat_history, stats])
        clear_btn.click(clear, [], [chatbot, chat_history, stats])

    return demo


# ============================================================
# 流式输出版本
# ============================================================

def create_streaming_interface():
    """创建支持流式输出的聊天界面。"""

    def chat_stream(message, history):
        """流式返回回答。"""
        # 模拟流式输出（实际项目中用 LLM 的 stream 接口）
        result = call_rag_api(message)
        answer = result["answer"]

        # 逐字输出
        partial = ""
        for char in answer:
            partial += char
            time.sleep(0.02)  # 模拟延迟
            yield partial

    demo = gr.ChatInterface(
        fn=chat_stream,
        title="🤖 RAG 流式聊天",
        description="支持流式输出的 RAG 问答系统",
    )

    return demo


# ============================================================
# 主函数
# ============================================================

def main():
    print("=" * 60)
    print("  Demo 2: Gradio RAG 界面")
    print("=" * 60)

    print("""
  本 Demo 提供 3 种界面模式:

  1. ChatInterface - 最简洁的聊天界面
  2. Blocks - 自定义布局（带设置面板）
  3. Streaming - 流式输出版本

  请选择模式:
    """)

    # 默认使用 ChatInterface
    mode = input("  输入模式编号 (1/2/3，默认1): ").strip() or "1"

    if mode == "2":
        print("\n  启动 Blocks 界面...")
        demo = create_blocks_interface()
    elif mode == "3":
        print("\n  启动流式聊天界面...")
        demo = create_streaming_interface()
    else:
        print("\n  启动 ChatInterface 界面...")
        demo = create_chat_interface()

    print("\n  启动 Gradio 服务...")
    print("  打开浏览器访问: http://localhost:7860")
    print("=" * 60)

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # 设为 True 可以生成公网链接
    )


if __name__ == "__main__":
    main()
