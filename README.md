# 徐州工程学院 AI 助手 API

基于 FastAPI + 阿里云通义千问的 AI 问答接口。

## 本地运行

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
# 复制 .env.example 为 .env，填入你的 API Key
cp .env.example .env

# 5. 启动服务
uvicorn main:app --reload
```

启动后访问：
- 接口文档：http://127.0.0.1:8000/docs
- GET 测试：http://127.0.0.1:8000/ai_chat?question=你好
- 健康检查：http://127.0.0.1:8000/ping

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 服务状态 |
| GET | `/ping` | 健康检查 |
| GET | `/ai_chat?question=xxx` | GET 方式提问 |
| POST | `/ai_chat` | POST 方式提问，body: `{"question": "xxx"}` |

## 环境变量

| 变量名 | 说明 |
|--------|------|
| `DASHSCOPE_API_KEY` | 阿里云通义千问 API Key |

## 部署到 Zeabur

1. 将代码推送到 GitHub
2. 登录 [Zeabur](https://zeabur.com)
3. 创建项目 → 关联 GitHub 仓库
4. 设置环境变量：`DASHSCOPE_API_KEY` = 你的 API Key
5. Zeabur 会自动识别 `pyproject.toml` 并部署
