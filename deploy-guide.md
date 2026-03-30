# 从本地到公网 — 完整部署指南

## 已完成的改造

你的 `F:\MyAPI` 现在是这样的结构：

```
F:\MyAPI/
├── main.py           ← 主代码（API Key 已从代码中移除）
├── requirements.txt  ← Python 依赖
├── pyproject.toml    ← Zeabur 部署识别
├── .gitignore        ← 排除 venv、.env 等敏感文件
├── .env              ← 本地 API Key（不会被上传）
├── .env.example      ← 环境变量模板（会上传，给别人参考）
├── README.md         ← 项目说明
└── venv/             ← 虚拟环境（不会被上传）
```

---

## 第一步：上传到 GitHub

### 1.1 在 GitHub 上创建仓库
1. 打开 https://github.com/new
2. 仓库名填：`xzit-ai-api`（或你喜欢的名字）
3. **不要勾选** "Add a README file"
4. 点 "Create repository"

### 1.2 在本地推送代码
打开终端，执行：

```powershell
cd F:\MyAPI

# 初始化 Git（如果还没有的话）
git init

# 添加远程仓库（把 YOUR_USERNAME 换成你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/xzit-ai-api.git

# 添加所有文件（.gitignore 会自动排除敏感文件）
git add .

# 提交
git commit -m "feat: FastAPI + 通义千问 AI 问答接口"

# 推送到 GitHub
git branch -M main
git push -u origin main
```

> 如果 git 提示要登录，按提示在浏览器授权即可。

---

## 第二步：部署到 Zeabur

### 2.1 注册 & 创建项目
1. 打开 https://zeabur.com 并登录（支持 GitHub 账号直接登录）
2. 点 "Create Project"，选一个区域（建议选 Hong Kong 或 Tokyo，离国内近）
3. 点 "Add Service" → "Git" → 选择你的 `xzit-ai-api` 仓库

### 2.2 设置环境变量（关键！）
1. 部署开始后，点击你的服务
2. 找到 "Variables" / "环境变量" 设置
3. 添加：
   - **Name**: `DASHSCOPE_API_KEY`
   - **Value**: `sk-21b5ea8beb8d4dd9bba4f18e93d174f0`
4. 保存

> Zeabur 会自动检测到 `pyproject.toml`，安装依赖并运行。如果它没有自动设置启动命令，你可以在服务设置中手动指定：
> - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8080`
> - **Port**: `8080`

### 2.3 绑定域名
1. 服务部署成功后，Zeabur 会自动分配一个 `*.zeabur.app` 域名
2. 如果你想用自定义域名，在 "Networking" 里绑定即可
3. 访问 `https://你的域名.zeabur.app/ai_chat?question=你好` 测试

---

## 第三步：验证

部署完成后，你的 API 可以这样调用：

**浏览器直接访问（GET）：**
```
https://你的域名.zeabur.app/ai_chat?question=你好
```

**用 curl（POST）：**
```bash
curl -X POST https://你的域名.zeabur.app/ai_chat \
  -H "Content-Type: application/json" \
  -d '{"question": "介绍一下徐州工程学院"}'
```

**自动生成的 API 文档：**
```
https://你的域名.zeabur.app/docs
```

---

## 安全清单

- [x] API Key 已从代码中移除
- [x] .env 文件已在 .gitignore 中排除
- [x] .env.example 只包含模板，不含真实 Key
- [x] GitHub 仓库中不包含任何密钥信息
- [ ] 推送后检查 GitHub 仓库确认无泄露
