# 第14章 Demo 学习指南

## 学习顺序

1. **先学 Demo 1（Streamlit RAG 界面）** → 掌握最常用的 RAG 前端方案
2. **再学 Demo 2（Gradio RAG 界面）** → 了解替代方案，特别是聊天界面

## Demo 说明

### Demo 1: Streamlit RAG 界面 (`1_demo_streamlit_rag.py`)

**作用**：一个完整的 RAG 聊天界面，包含侧边栏设置、多轮对话、来源展示。

**学到什么**：
- Streamlit 的核心组件（st.title、st.chat_input、st.chat_message）
- session_state 管理聊天历史
- 侧边栏设置面板
- 文件上传功能

**是否需要 API Key**：需要（但内置了模拟回答，可以直接体验界面）

**运行方式**：
```bash
# 安装 Streamlit
pip install streamlit

# 运行
streamlit run 1_demo_streamlit_rag.py

# 打开浏览器访问 http://localhost:8501
```

---

### Demo 2: Gradio RAG 界面 (`2_demo_gradio_rag.py`)

**作用**：用 Gradio 实现 RAG 聊天界面，提供 3 种模式（ChatInterface、Blocks、流式输出）。

**学到什么**：
- Gradio 的 ChatInterface 用法
- Blocks 自定义布局
- 流式输出的实现
- Streamlit 和 Gradio 的对比

**是否需要 API Key**：需要（但内置了模拟回答，可以直接体验界面）

**运行方式**：
```bash
# 安装 Gradio
pip install gradio

# 运行
python 2_demo_gradio_rag.py

# 打开浏览器访问 http://localhost:7860
```

---

## 前置依赖

```bash
pip install streamlit gradio
```

## 学完本章你应该能回答

1. Streamlit 的核心组件有哪些？
2. 如何用 session_state 管理聊天历史？
3. Gradio 的 ChatInterface 怎么用？
4. Streamlit 和 Gradio 怎么选？
5. 如何实现流式输出的聊天界面？
