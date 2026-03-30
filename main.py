import os
from dotenv import load_dotenv
from fastapi import FastAPI

# 加载 .env 文件（本地开发用，云端环境变量会自动覆盖）
load_dotenv()
from openai import OpenAI
from pydantic import BaseModel

app = FastAPI()

# 初始化通义千问客户端，从环境变量读取 API Key
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# POST 请求的数据模型
class ChatRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "徐州工程学院 AI 助手 API 运行中 ✅"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/ai_chat")
def ai_chat(question: str):
    """GET 方式调用：/ai_chat?question=xxx"""
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
def ai_chat_post(req: ChatRequest):
    """POST 方式调用：body {"question": "xxx"}"""
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
