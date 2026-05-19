# RAGHub AI Knowledge Base

一个企业风格的私有知识库 RAG 问答系统，基于 FastAPI、Vue 3、LangChain、ChromaDB 和智谱 GLM 构建。项目展示了如何把一个基础 RAG Demo 工程化升级为更接近真实 AI 后端应用的系统，包括用户认证、用户级知识库隔离、后台向量化、日志、缓存设计和容器化部署。

## 项目亮点

- 基于 JWT 的注册、登录和接口鉴权
- 基于 `user_id` metadata filter 的多用户知识库隔离
- 支持 `txt`、`md`、`pdf`、`docx` 文档上传和管理
- 文档后台索引：解析、切块、Embedding、写入 ChromaDB
- RAG 问答链路：向量检索、Prompt 组装、GLM-4 生成、来源返回
- Redis 缓存和请求限流设计
- 请求日志中间件，记录路径、状态码、耗时等信息
- Vue 3 前端，包含登录、聊天、知识库管理页面
- 提供 Dockerfile 和 Docker Compose 部署配置

## 技术栈

### 前端

- Vue 3
- Vue Router
- Axios
- Vite

### 后端

- Python 3.11
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- JWT
- Passlib + bcrypt
- FastAPI BackgroundTasks

### AI / RAG

- LangChain
- ChromaDB
- 智谱 Embedding
- 智谱 GLM-4
- RecursiveCharacterTextSplitter
- Prompt Engineering

### 工程化

- `.env` 环境变量管理
- Dockerfile
- Docker Compose
- Redis 缓存和限流设计
- 请求日志中间件
- 后端分层架构

## 系统架构

```text
Vue 3 前端
  |
  | HTTP + JWT
  v
FastAPI 后端
  |
  |-- Auth API
  |-- Documents API
  |-- Knowledge Base API
  |-- Chat API
  |
  |-- SQLAlchemy / SQLite
  |-- ChromaDB
  |-- Redis 可选
  |-- 本地文件存储
  |
  v
智谱 Embedding + GLM-4
```

## RAG 流程

### 文档上传与索引

```text
上传文档
  -> 保存原始文件
  -> 创建文档记录
  -> 启动后台索引任务
  -> 解析文档
  -> 文本切块
  -> 调用 Embedding 模型
  -> 写入 ChromaDB，并携带 user_id/document_id metadata
```

### 问答流程

```text
用户提问
  -> 校验 JWT Token
  -> 用户级限流
  -> 按 user_id 过滤检索 ChromaDB
  -> 获取相关文档片段
  -> 组装 RAG Prompt
  -> 调用 GLM-4
  -> 返回答案和引用来源
```

## 项目结构

```text
backend/
  app/
    api/v1/              # FastAPI 路由
    core/                # 配置、安全、日志、中间件
    db/                  # SQLAlchemy 引擎和 Session
    models/              # ORM 数据模型
    schemas/             # Pydantic 接口模型
    services/            # 业务服务层
    rag/                 # 文档加载、切块、Embedding、Prompt、LLM
    tasks/               # 后台索引任务
  main.py
  requirements.txt
  Dockerfile

rag-vue-ui/
  src/
    api/                 # Axios 请求封装
    views/               # 登录、聊天、知识库页面
    components/          # 前端组件
    router/              # Vue Router
  package.json
  vite.config.js
  Dockerfile
  nginx.conf

docker-compose.yml
.env.example
README.md
README.zh-CN.md
```

## 环境变量

复制 `.env.example` 为 `.env`：

```powershell
copy .env.example .env
```

然后填写智谱 API Key：

```env
ZHIPU_API_KEY=your-zhipu-api-key
SECRET_KEY=replace-with-a-long-random-secret
REDIS_ENABLED=false
```

本地开发建议先保持：

```env
REDIS_ENABLED=false
```

如果本地安装了 Redis，或者使用 Docker Compose，可以再开启 Redis。

## 本地启动

### 后端

后端建议使用 Python 3.11。不要使用 Python 3.14，因为目前很多 AI/RAG 依赖还没有完整适配，可能出现依赖无法安装的问题。

如果使用本机已经创建好的 Conda 环境：

```powershell
cd D:\assistance\backend
C:\Users\name\.conda\envs\rag311\python.exe -m uvicorn main:app --reload --port 8080
```

通用 Python 3.11 启动方式：

```powershell
cd backend
python -m pip install -r requirements.txt -i https://pypi.org/simple
python -m uvicorn main:app --reload --port 8080
```

后端接口文档：

```text
http://localhost:8080/docs
```

### 前端

Windows PowerShell 可能会拦截 `npm.ps1`，建议使用 `npm.cmd`：

```powershell
cd rag-vue-ui
npm.cmd install
npm.cmd run dev
```

访问：

```text
http://localhost:5173
```

## Docker Compose 启动

如果本机已经安装 Docker：

```powershell
copy .env.example .env
docker compose up --build
```

访问：

```text
http://localhost:5173
```

## 核心接口

### 用户认证

- `POST /api/v1/auth/register`：注册
- `POST /api/v1/auth/login`：登录
- `GET /api/v1/auth/me`：获取当前用户

### 文档管理

- `POST /api/v1/documents/upload`：上传文档
- `GET /api/v1/documents`：获取文档列表
- `DELETE /api/v1/documents/{document_id}`：删除文档

### 知识库

- `GET /api/v1/knowledge-bases/status`：获取知识库状态

### 聊天问答

- `POST /api/v1/chat/ask`：RAG 问答

## 功能说明

### 1. 用户系统

系统支持用户注册、登录和 JWT Token 鉴权。用户登录后，前端会自动携带 Token 请求后端接口。

### 2. 用户知识库隔离

每个用户上传的文档都会绑定自己的 `user_id`。文档切块写入 ChromaDB 时，也会写入 `user_id` 和 `document_id`。用户提问时，系统只会检索当前登录用户自己的知识库。

### 3. 文档上传与后台索引

文档上传后，后端使用后台任务完成文档解析、文本切块、Embedding 向量化和 ChromaDB 持久化。前端可以看到 `pending`、`indexing`、`indexed`、`failed` 等状态。

### 4. RAG 智能问答

用户提问后，系统会先从当前用户的向量库中检索相关片段，再把片段和问题组装成 Prompt，调用 GLM-4 生成答案，并返回引用来源。

### 5. Redis 缓存和限流

系统设计了 Redis 问答缓存和用户级请求限流，用于降低重复问题下的大模型调用成本，并提升接口稳定性。本地开发可以关闭 Redis。

### 6. 日志系统

后端增加了请求日志中间件，记录请求路径、状态码、接口耗时和异常信息，便于排查 RAG 链路中的问题。
