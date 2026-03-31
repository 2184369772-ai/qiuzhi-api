import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# 加载 .env 文件（本地开发用，云端环境变量会自动覆盖）
load_dotenv()

from openai import OpenAI
from pydantic import BaseModel

app = FastAPI()

# 初始化通义千问客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 接口访问密钥（调用 /ai_chat 需要在 Header 带上 X-API-Key）
ACCESS_KEY = os.getenv("ACCESS_KEY", "")


def check_access_key(request: Request):
    """校验请求头里的 X-API-Key"""
    if not ACCESS_KEY:
        # 没有设置 ACCESS_KEY 则不鉴权（方便开发时测试）
        return
    key = request.headers.get("X-API-Key", "")
    if key != ACCESS_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: 无效的 API Key")


# POST 请求的数据模型
class ChatRequest(BaseModel):
    question: str


@app.get("/")
def root():
    """根路由：返回聊天页面"""
    return FileResponse("static/index.html")


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/ai_chat")
def ai_chat(question: str, request: Request):
    """GET 方式调用：/ai_chat?question=xxx（需要 Header: X-API-Key）"""
    check_access_key(request)
    try:
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个来自徐州工程学院的 AI 助手。"},
                {"role": "user", "content": question},
            ]
        )
        answer = response.choices[0].message.content
        return {"question": question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}


@app.post("/ai_chat")
def ai_chat_post(req: ChatRequest, request: Request):
    """POST 方式调用（需要 Header: X-API-Key）"""
    check_access_key(request)
    try:
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个来自徐州工程学院的 AI 助手。"},
                {"role": "user", "content": req.question},
            ]
        )
        answer = response.choices[0].message.content
        return {"question": req.question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}


# 挂载静态文件目录（放 HTML/CSS/JS）
app.mount("/static", StaticFiles(directory="static"), name="static")
