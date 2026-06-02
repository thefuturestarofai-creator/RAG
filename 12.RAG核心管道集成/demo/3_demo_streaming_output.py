"""
Demo 3: 流式输出 - FastAPI + SSE

本 Demo 实现一个支持流式输出的 RAG 问答服务：
1. FastAPI 提供 HTTP 接口
2. SSE（Server-Sent Events）实现打字机效果
3. 前端页面实时显示回答

用法：
    python 3_demo_streaming_output.py

然后打开浏览器访问 http://localhost:8000 查看效果。

需要 API Key：
    - OPENAI_API_KEY：用于 Embedding 和 LLM
    - OPENAI_BASE_URL：API 地址
    - MODEL：使用的模型名称
"""

import os
import json
import asyncio
from typing import AsyncGenerator

# ============================================================
# 配置区域
# ============================================================

API_KEY = os.getenv("OPENAI_API_KEY", "sk-your-api-key-here")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


# ============================================================
# 第一步：创建示例知识库
# ============================================================

def create_knowledge_base():
    """创建示例知识库文件。"""

    data_dir = os.path.join(os.path.dirname(__file__), "streaming_data")
    os.makedirs(data_dir, exist_ok=True)

    documents = {
        "AI基础知识.txt": """\
人工智能（AI）基础知识

一、什么是人工智能？
人工智能是计算机科学的一个分支，致力于创建能够模拟人类智能的系统。
AI系统能够学习、推理、感知、理解语言和做出决策。

二、AI的主要分支：
1. 机器学习（ML）：让计算机从数据中学习规律，而不需要明确编程
2. 深度学习（DL）：使用多层神经网络处理复杂数据
3. 自然语言处理（NLP）：让计算机理解和生成人类语言
4. 计算机视觉（CV）：让计算机理解和分析图像
5. 语音识别：将语音转换为文本

三、大语言模型（LLM）：
大语言模型是深度学习的重要成果，代表模型包括：
- GPT系列（OpenAI）
- Claude系列（Anthropic）
- Llama系列（Meta）
- 文心一言（百度）
- 通义千问（阿里）

LLM的特点：
- 参数量巨大（数十亿到数万亿）
- 需要大量数据训练
- 具有涌现能力（Emergent Abilities）
- 支持多种任务（问答、写作、编程等）
""",
        "RAG技术详解.txt": """\
RAG（检索增强生成）技术详解

一、RAG的核心思想
RAG = 检索（Retrieval）+ 增强（Augmented）+ 生成（Generation）

核心流程：
1. 用户提问
2. 系统从知识库中检索相关文档
3. 将检索到的文档作为参考，与问题一起输入LLM
4. LLM基于参考文档生成回答

二、RAG的优势
1. 知识可更新：更新知识库即可，不需要重新训练模型
2. 减少幻觉：回答基于真实文档，减少编造
3. 可追溯：可以标注回答来源
4. 成本低：比微调大模型便宜得多

三、RAG的技术栈
- 文档加载：LangChain Document Loaders
- 文本切分：RecursiveCharacterTextSplitter
- 向量化：OpenAI Embeddings / Sentence Transformers
- 向量数据库：Chroma / Milvus / FAISS
- 大语言模型：GPT / Claude / Llama
- Web框架：FastAPI / Flask

四、RAG的挑战
1. 检索质量：检索不到好文档，回答就差
2. 切分策略：chunk大小和重叠影响效果
3. 上下文长度：LLM的token限制
4. 延迟：检索+生成的时间
""",
    }

    for filename, content in documents.items():
        file_path = os.path.join(data_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    return data_dir


# ============================================================
# 第二步：构建 RAG 管道
# ============================================================

class RAGSystem:
    """RAG 系统，支持流式输出。"""

    def __init__(self):
        self.vectorstore = None
        self._initialized = False

    def initialize(self, data_dir: str):
        """初始化 RAG 系统（加载文档、构建索引）。"""
        from langchain_community.document_loaders import DirectoryLoader, TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_openai import OpenAIEmbeddings
        from langchain_community.vectorstores import Chroma

        if self._initialized:
            return

        print("正在初始化 RAG 系统...")

        # 加载文档
        loader = DirectoryLoader(
            path=data_dir,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        documents = loader.load()

        # 切分
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
        )
        chunks = splitter.split_documents(documents)

        # 构建向量索引
        embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=API_KEY,
            openai_api_base=BASE_URL,
        )

        persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db_streaming")
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_dir,
            collection_name="streaming_demo",
        )

        self._initialized = True
        print(f"RAG 系统初始化完成! 共 {len(chunks)} 个文档片段")

    async def query_stream(self, question: str) -> AsyncGenerator[str, None]:
        """
        流式查询，逐步返回回答 token。

        Args:
            question: 用户问题

        Yields:
            SSE 格式的数据字符串
        """
        from langchain_openai import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate

        # 1. 检索相关文档
        results = self.vectorstore.similarity_search_with_score(question, k=3)

        # 2. 构造来源信息
        sources = []
        context_parts = []
        for i, (doc, score) in enumerate(results, 1):
            filename = os.path.basename(doc.metadata.get("source", "未知"))
            sources.append({
                "index": i,
                "filename": filename,
                "snippet": doc.page_content[:100],
            })
            context_parts.append(f"[来源{i}: {filename}]\n{doc.page_content}")

        # 先发送来源信息
        yield f"data: {json.dumps({'type': 'sources', 'sources': sources}, ensure_ascii=False)}\n\n"

        # 3. 构造 Prompt
        context = "\n\n---\n\n".join(context_parts)
        template = """请根据以下参考资料回答问题。回答要简洁准确。

参考资料：
{context}

问题：{question}
回答："""

        prompt = ChatPromptTemplate.from_template(template)
        messages = prompt.format_messages(context=context, question=question)

        # 4. 流式调用 LLM
        llm = ChatOpenAI(
            model=MODEL,
            openai_api_key=API_KEY,
            openai_api_base=BASE_URL,
            temperature=0.3,
            streaming=True,  # 启用流式输出
        )

        # 使用 astream 异步流式调用
        async for chunk in llm.astream(messages):
            token = chunk.content
            if token:
                yield f"data: {json.dumps({'type': 'token', 'token': token}, ensure_ascii=False)}\n\n"

        # 发送完成标记
        yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"


# ============================================================
# 第三步：FastAPI 应用
# ============================================================

def create_app():
    """创建 FastAPI 应用。"""
    from fastapi import FastAPI, Query
    from fastapi.responses import StreamingResponse, HTMLResponse

    app = FastAPI(title="RAG 流式问答系统")

    # 全局 RAG 系统实例
    rag = RAGSystem()

    @app.on_event("startup")
    async def startup():
        """应用启动时初始化 RAG 系统。"""
        data_dir = create_knowledge_base()
        rag.initialize(data_dir)

    @app.get("/stream-query")
    async def stream_query(question: str = Query(..., description="用户问题")):
        """
        流式问答接口。

        使用 SSE（Server-Sent Events）逐步返回回答。
        """
        return StreamingResponse(
            rag.query_stream(question),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )

    @app.get("/", response_class=HTMLResponse)
    async def index():
        """返回前端页面。"""
        html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAG 流式问答系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        .chat-box {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        .message {
            margin-bottom: 16px;
            padding: 12px 16px;
            border-radius: 8px;
            line-height: 1.6;
        }
        .user-message {
            background: #e3f2fd;
            margin-left: 60px;
            text-align: right;
        }
        .ai-message {
            background: #f5f5f5;
            margin-right: 60px;
        }
        .sources {
            background: #fff3e0;
            border-left: 3px solid #ff9800;
            padding: 8px 12px;
            margin-bottom: 8px;
            font-size: 13px;
            border-radius: 4px;
        }
        .sources-title { font-weight: bold; color: #e65100; }
        .source-item { margin: 4px 0; color: #555; }
        .input-area {
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus { border-color: #2196f3; }
        button {
            padding: 12px 24px;
            background: #2196f3;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover { background: #1976d2; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .loading { color: #999; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>RAG 流式问答系统</h1>
        <div class="chat-box" id="chatBox"></div>
        <div class="input-area">
            <input type="text" id="questionInput" placeholder="请输入问题..." onkeypress="if(event.key==='Enter')sendQuestion()">
            <button onclick="sendQuestion()" id="sendBtn">发送</button>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chatBox');
        const questionInput = document.getElementById('questionInput');
        const sendBtn = document.getElementById('sendBtn');

        function addMessage(content, isUser) {
            const div = document.createElement('div');
            div.className = 'message ' + (isUser ? 'user-message' : 'ai-message');
            div.innerHTML = content;
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
            return div;
        }

        async function sendQuestion() {
            const question = questionInput.value.trim();
            if (!question) return;

            // 显示用户消息
            addMessage(question, true);
            questionInput.value = '';
            sendBtn.disabled = true;

            // 创建 AI 回复容器
            const aiDiv = addMessage('<span class="loading">思考中...</span>', false);
            let answerText = '';
            let sourcesShown = false;

            try {
                const eventSource = new EventSource('/stream-query?question=' + encodeURIComponent(question));

                eventSource.onmessage = function(event) {
                    const data = JSON.parse(event.data);

                    if (data.type === 'sources') {
                        // 显示来源信息
                        let sourcesHtml = '<div class="sources"><span class="sources-title">参考来源：</span>';
                        data.sources.forEach(s => {
                            sourcesHtml += `<div class="source-item">[${s.index}] ${s.filename}: ${s.snippet}...</div>`;
                        });
                        sourcesHtml += '</div>';
                        aiDiv.innerHTML = sourcesHtml;
                        sourcesShown = true;
                    }
                    else if (data.type === 'token') {
                        // 追加 token
                        if (aiDiv.querySelector('.loading')) {
                            aiDiv.querySelector('.loading').remove();
                        }
                        answerText += data.token;
                        const sourcesDiv = aiDiv.querySelector('.sources');
                        const answerDiv = aiDiv.querySelector('.answer-text') || (() => {
                            const d = document.createElement('div');
                            d.className = 'answer-text';
                            aiDiv.appendChild(d);
                            return d;
                        })();
                        answerDiv.innerHTML = answerText.replace(/\\n/g, '<br>');
                        chatBox.scrollTop = chatBox.scrollHeight;
                    }
                    else if (data.type === 'done') {
                        eventSource.close();
                        sendBtn.disabled = false;
                    }
                };

                eventSource.onerror = function() {
                    eventSource.close();
                    if (!answerText) {
                        aiDiv.innerHTML = '<span style="color:red;">连接失败，请检查服务是否启动。</span>';
                    }
                    sendBtn.disabled = false;
                };
            } catch (e) {
                aiDiv.innerHTML = '<span style="color:red;">请求失败: ' + e.message + '</span>';
                sendBtn.disabled = false;
            }
        }
    </script>
</body>
</html>
        """
        return HTMLResponse(content=html_content)

    return app


# ============================================================
# 主函数
# ============================================================

def main():
    print("=" * 60)
    print("  Demo 3: 流式输出 - FastAPI + SSE")
    print("=" * 60)

    # 检查 API Key
    if API_KEY == "sk-your-api-key-here":
        print("\n⚠️  请先设置 API Key!")
        print("  方式一：修改脚本顶部的 API_KEY 变量")
        print("  方式二：设置环境变量 OPENAI_API_KEY")

        print("\n" + "=" * 60)
        print("  流式输出实现说明")
        print("=" * 60)
        print("""
  流式输出的实现分 3 部分：

  1. 后端（FastAPI + SSE）:
     @app.get("/stream-query")
     async def stream_query(question: str):
         return StreamingResponse(
             generate_stream(question),
             media_type="text/event-stream",
         )

     async def generate_stream(question):
         for chunk in llm.stream(messages):
             yield f"data: {json.dumps({'token': chunk.content})}\\n\\n"
         yield "data: [DONE]\\n\\n"

  2. 前端（JavaScript EventSource）:
     const es = new EventSource('/stream-query?question=...');
     es.onmessage = function(event) {
         const data = JSON.parse(event.data);
         document.getElementById('answer').innerHTML += data.token;
     };

  3. SSE 数据格式:
     data: {"type": "sources", "sources": [...]}\\n\\n
     data: {"type": "token", "token": "RAG"}\\n\\n
     data: {"type": "token", "token": "是"}\\n\\n
     data: {"type": "done"}\\n\\n
        """)

        # 创建示例文件（不需要 API Key）
        create_knowledge_base()
        return

    # 启动服务
    print("\n正在启动服务...")
    print(f"模型: {MODEL}")
    print(f"API 地址: {BASE_URL}")

    app = create_app()

    print("\n" + "=" * 60)
    print("  服务已启动!")
    print("  打开浏览器访问: http://localhost:8000")
    print("  API 文档: http://localhost:8000/docs")
    print("=" * 60)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
