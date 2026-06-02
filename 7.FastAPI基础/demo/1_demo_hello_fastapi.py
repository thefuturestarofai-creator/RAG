"""
Demo 1: Hello FastAPI - 10行代码启动API
=======================================

功能：
- 创建最简单的 FastAPI 应用
- 访问 /docs 查看自动生成的API文档

前置条件：
- pip install fastapi uvicorn
- 不需要 API Key

对应理论：1.路由与请求处理.md

运行方式：
- 在终端执行：uvicorn 1_demo_hello_fastapi:app --reload
- 或者直接运行本文件：python 1_demo_hello_fastapi.py
"""

from fastapi import FastAPI

# 创建 FastAPI 应用实例
app = FastAPI(
    title="我的第一个 FastAPI 应用",
    description="一个简单的演示应用",
    version="1.0.0"
)

# ============================================================
# 路由定义
# ============================================================

@app.get("/")
async def root():
    """根路由 - 返回欢迎信息"""
    return {"message": "Hello, FastAPI!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    """
    路径参数示例

    访问 /hello/小明 → {"message": "你好, 小明!"}
    """
    return {"message": f"你好, {name}!"}


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    """
    查询参数示例

    访问 /items/?skip=5&limit=20 → {"skip": 5, "limit": 20, "message": "获取物品列表"}
    """
    return {
        "skip": skip,
        "limit": limit,
        "message": f"获取物品列表，跳过{skip}个，返回{limit}个"
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "version": "1.0.0"}


# ============================================================
# 主程序入口
# ============================================================
if __name__ == "__main__":
    import uvicorn

    print("=" * 50)
    print("FastAPI 应用启动中...")
    print("=" * 50)
    print()
    print("访问地址：")
    print("  - 首页：http://127.0.0.1:8000/")
    print("  - 带参数：http://127.0.0.1:8000/hello/小明")
    print("  - 查询参数：http://127.0.0.1:8000/items/?skip=5&limit=20")
    print("  - 健康检查：http://127.0.0.1:8000/health")
    print()
    print("API 文档：")
    print("  - Swagger UI：http://127.0.0.1:8000/docs")
    print("  - ReDoc：http://127.0.0.1:8000/redoc")
    print()
    print("按 Ctrl+C 停止服务")
    print("=" * 50)

    # 启动服务器
    uvicorn.run(app, host="127.0.0.1", port=8000)
