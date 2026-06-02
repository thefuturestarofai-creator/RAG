"""
Demo 1: Streamlit RAG 界面

本 Demo 实现一个完整的 RAG 聊天界面，使用 Streamlit 构建。
功能包括：
1. 聊天界面（支持多轮对话）
2. 侧边栏设置（API Key、模型选择、检索数量）
3. 来源展示
4. 文件上传

用法：
    streamlit run 1_demo_streamlit_rag.py

需要 API Key：
    - OPENAI_API_KEY：用于 Embedding 和 LLM
    - OPENAI_BASE_URL：API 地址
    - MODEL：使用的模型名称
"""

import os
import sys

# ============================================================
# 配置区域 - 在这里填写你的 API Key
# ============================================================

API_KEY = os.getenv("OPENAI_API_KEY", "sk-your-api-key-here")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# ============================================================
# Streamlit 应用代码
# ============================================================

# 注意：以下代码需要安装 streamlit 才能运行
# pip install streamlit

# 检查是否在 Streamlit 环境中运行
try:
    import streamlit as st
except ImportError:
    print("=" * 60)
    print("  需要安装 Streamlit")
    print("=" * 60)
    print("""
  安装命令:
    pip install streamlit

  运行命令:
    streamlit run 1_demo_streamlit_rag.py
    """)
    sys.exit(0)


# ============================================================
# 页面配置
# ============================================================

st.set_page_config(
    page_title="RAG 知识库问答系统",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 侧边栏设置
# ============================================================

def render_sidebar():
    """渲染侧边栏设置。"""
    with st.sidebar:
        st.title("⚙️ 设置")
        st.divider()

        # API 配置
        st.subheader("API 配置")
        api_key = st.text_input(
            "OpenAI API Key",
            value=API_KEY,
            type="password",
            help="输入你的 API Key"
        )
        base_url = st.text_input(
            "API Base URL",
            value=BASE_URL,
            help="API 服务地址"
        )

        st.divider()

        # 模型配置
        st.subheader("模型配置")
        model = st.selectbox(
            "选择模型",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            index=0,
        )
        top_k = st.slider(
            "检索数量 (top_k)",
            min_value=1,
            max_value=10,
            value=3,
            help="从知识库中检索的文档数量"
        )
        temperature = st.slider(
            "温度 (temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="值越低回答越确定"
        )

        st.divider()

        # 知识库管理
        st.subheader("📚 知识库管理")
        uploaded_files = st.file_uploader(
            "上传文档",
            type=["txt", "md"],
            accept_multiple_files=True,
            help="支持 TXT 和 Markdown 格式"
        )

        if uploaded_files:
            st.write(f"已上传 {len(uploaded_files)} 个文件:")
            for f in uploaded_files:
                st.write(f"  - {f.name}")

        st.divider()

        # 操作按钮
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        return {
            "api_key": api_key,
            "base_url": base_url,
            "model": model,
            "top_k": top_k,
            "temperature": temperature,
            "uploaded_files": uploaded_files,
        }


# ============================================================
# RAG 调用逻辑
# ============================================================

def call_rag_api(question: str, config: dict) -> dict:
    """
    调用 RAG API（这里是模拟实现）。

    实际项目中，这里应该调用后端的 RAG 服务。
    """

    # 模拟 API 调用
    # 实际实现:
    # import requests
    # response = requests.post(
    #     "http://localhost:8000/query",
    #     json={"question": question, "top_k": config["top_k"]}
    # )
    # return response.json()

    # 模拟回答
    if "rag" in question.lower() or "RAG" in question:
        return {
            "answer": f"RAG（检索增强生成）是一种结合信息检索和文本生成的技术框架。\n\n"
                      f"核心流程：\n"
                      f"1. 将文档加载、切分、向量化后存入向量数据库\n"
                      f"2. 用户提问时，从向量数据库中检索相关文档\n"
                      f"3. 将检索到的文档与问题一起输入 LLM 生成回答\n\n"
                      f"优势：知识可更新、减少幻觉、可追溯、成本低。\n\n"
                      f"（模型: {config['model']}, 检索数量: {config['top_k']}）",
            "sources": [
                {"filename": "RAG技术白皮书.txt", "relevance": 0.95},
                {"filename": "向量数据库说明.txt", "relevance": 0.87},
            ]
        }
    else:
        return {
            "answer": f"这是关于「{question}」的回答。\n\n"
                      f"在实际项目中，这里会调用后端 RAG 服务，"
                      f"从知识库中检索相关文档后生成回答。\n\n"
                      f"当前配置：模型={config['model']}, top_k={config['top_k']}",
            "sources": [
                {"filename": "示例文档.txt", "relevance": 0.80},
            ]
        }


# ============================================================
# 主界面
# ============================================================

def main():
    """主界面渲染。"""

    # 标题
    st.title("🤖 RAG 知识库问答系统")
    st.caption("基于检索增强生成的智能问答系统 | 支持多轮对话")

    # 侧边栏设置
    config = render_sidebar()

    # 初始化聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示欢迎消息
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.write("你好！我是 RAG 知识库助手。")
            st.write("你可以问我任何问题，我会从知识库中检索相关信息来回答你。")
            st.write("试试问：「什么是 RAG？」")

    # 显示历史消息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            # 显示来源信息
            if "sources" in message and message["sources"]:
                with st.expander("📎 参考来源"):
                    for source in message["sources"]:
                        st.write(f"- {source['filename']} (相关度: {source['relevance']:.2f})")

    # 用户输入
    if prompt := st.chat_input("请输入你的问题..."):
        # 显示用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # 生成回答
        with st.chat_message("assistant"):
            with st.spinner("正在检索知识库并生成回答..."):
                result = call_rag_api(prompt, config)
                st.write(result["answer"])

                # 显示来源
                if result.get("sources"):
                    with st.expander("📎 参考来源"):
                        for source in result["sources"]:
                            st.write(f"- {source['filename']} (相关度: {source['relevance']:.2f})")

        # 保存回答到历史
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result.get("sources", []),
        })

    # 底部信息
    st.divider()
    st.caption("💡 提示：在左侧设置中可以调整模型、检索数量等参数")


# ============================================================
# 运行
# ============================================================

if __name__ == "__main__":
    main()
