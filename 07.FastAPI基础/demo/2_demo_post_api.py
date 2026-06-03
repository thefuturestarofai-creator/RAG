"""
Demo 2: POST接口 - Pydantic数据校验
===================================

功能：
- 接收 JSON 请求体
- 用 Pydantic 模型校验数据
- 返回结构化响应

前置条件：
- pip install fastapi uvicorn pydantic
- 不需要 API Key

对应理论：2.Pydantic数据校验.md

运行方式：
- uvicorn 2_demo_post_api:app --reload
- 或 python 2_demo_post_api.py
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="Pydantic 数据校验演示")


# ============================================================
# 定义 Pydantic 模型
# ============================================================

class ChatMessage(BaseModel):
    """聊天消息模型"""
    role: str = Field(
        ...,
        description="消息角色：user 或 assistant",
        pattern="^(user|assistant)$"  # 正则验证
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="消息内容"
    )


class ChatRequest(BaseModel):
    """聊天请求模型"""
    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="用户的问题"
    )
    history: List[ChatMessage] = Field(
        default=[],
        description="对话历史"
    )
    temperature: float = Field(
        default=0.7,
        ge=0,        # 大于等于 0
        le=2,        # 小于等于 2
        description="创造性参数，0-2之间"
    )


class SourceInfo(BaseModel):
    """来源信息模型"""
    title: str
    page: Optional[int] = None  # 可选字段


class ChatResponse(BaseModel):
    """聊天响应模型"""
    answer: str = Field(..., description="AI的回答")
    sources: List[SourceInfo] = Field(default=[], description="参考来源")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str
    detail: Optional[str] = None


# ============================================================
# 模拟数据库
# ============================================================
fake_items_db = [
    {"id": 1, "name": "Python教程", "price": 99.9},
    {"id": 2, "name": "RAG实战", "price": 129.9},
    {"id": 3, "name": "FastAPI指南", "price": 79.9},
]


# ============================================================
# 路由定义
# ============================================================

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    聊天接口 - 演示 Pydantic 请求/响应模型

    接收问题和对话历史，返回结构化的回答
    """
    # 此时 request 已经过 Pydantic 验证，可以直接使用
    print(f"收到问题：{request.question}")
    print(f"历史消息数：{len(request.history)}")
    print(f"Temperature：{request.temperature}")

    # 模拟 RAG 回答
    answer = f"这是对「{request.question}」的回答（模拟）"

    # 构建响应
    return ChatResponse(
        answer=answer,
        sources=[
            SourceInfo(title="知识库文档1", page=1),
            SourceInfo(title="技术博客")
        ]
    )


@app.post("/items/")
async def create_item(name: str, price: float = Field(gt=0)):
    """
    创建物品 - 演示查询参数中的验证

    price 必须大于 0
    """
    new_item = {
        "id": len(fake_items_db) + 1,
        "name": name,
        "price": price
    }
    fake_items_db.append(new_item)
    return {"message": "创建成功", "item": new_item}


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """
    获取物品 - 演示路径参数和异常处理
    """
    for item in fake_items_db:
        if item["id"] == item_id:
            return item

    # 抛出 HTTP 异常
    raise HTTPException(
        status_code=404,
        detail=f"物品 {item_id} 不存在"
    )


@app.get("/items/")
async def list_items(
    skip: int = Field(default=0, ge=0),
    limit: int = Field(default=10, ge=1, le=100)
):
    """
    物品列表 - 演示查询参数验证

    skip >= 0, 1 <= limit <= 100
    """
    return {
        "total": len(fake_items_db),
        "items": fake_items_db[skip:skip + limit]
    }


# ============================================================
# 主程序入口
# ============================================================
if __name__ == "__main__":
    import uvicorn

    print("=" * 50)
    print("Pydantic 数据校验演示")
    print("=" * 50)
    print()
    print("测试接口：")
    print("  - POST /chat     - 聊天接口（带数据校验）")
    print("  - POST /items/   - 创建物品")
    print("  - GET /items/1   - 获取物品")
    print("  - GET /items/    - 物品列表（分页）")
    print()
    print("API 文档：http://127.0.0.1:8000/docs")
    print()
    print("测试 POST /chat 的请求体示例：")
    print("""
    {
        "question": "什么是RAG？",
        "history": [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！有什么可以帮你的？"}
        ],
        "temperature": 0.7
    }
    """)
    print("=" * 50)

    uvicorn.run(app, host="127.0.0.1", port=8000)
