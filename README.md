# RAGHub AI Knowledge Base

An enterprise-style private knowledge base Q&A system built with FastAPI, Vue 3, LangChain, ChromaDB, and Zhipu GLM. It demonstrates how to turn a basic RAG demo into a more production-like AI backend application with authentication, user-level data isolation, background indexing, logging, cache design, and containerization.

## Highlights

- JWT-based register, login, and protected API access
- User-level knowledge base isolation with `user_id` metadata filtering in ChromaDB
- Document upload and management for `txt`, `md`, `pdf`, and `docx`
- Background document indexing: parse, split, embed, and persist to ChromaDB
- RAG chat pipeline: retrieval, prompt assembly, GLM-4 generation, and source return
- Redis-ready cache and rate limit design
- Request logging with request path, status code, and latency
- Vue 3 frontend with login, chat, and knowledge base management pages
- Docker Compose files for frontend, backend, and Redis deployment

## Tech Stack

### Frontend

- Vue 3
- Vue Router
- Axios
- Vite

### Backend

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
- ZhipuAI Embedding
- Zhipu GLM-4
- RecursiveCharacterTextSplitter
- Prompt Engineering

### Engineering

- Environment variables with `.env`
- Dockerfile
- Docker Compose
- Redis cache and rate limit design
- Request logging middleware
- Layered backend architecture

## Architecture

```text
Vue 3 Frontend
  |
  | HTTP + JWT
  v
FastAPI Backend
  |
  |-- Auth API
  |-- Documents API
  |-- Knowledge Base API
  |-- Chat API
  |
  |-- SQLAlchemy / SQLite
  |-- ChromaDB
  |-- Redis optional
  |-- Local file storage
  |
  v
Zhipu Embedding + GLM-4
```

## RAG Flow

```text
Upload document
  -> save original file
  -> create document record
  -> background indexing task
  -> load document
  -> split text into chunks
  -> call embedding model
  -> store vectors in ChromaDB with user_id/document_id metadata

Ask question
  -> verify JWT token
  -> apply user-level rate limit
  -> search ChromaDB with user_id filter
  -> build RAG prompt with retrieved chunks
  -> call GLM-4
  -> return answer and sources
```

## Project Structure

```text
backend/
  app/
    api/v1/              # FastAPI routes
    core/                # config, security, logging, middleware
    db/                  # SQLAlchemy engine and session
    models/              # ORM models
    schemas/             # Pydantic schemas
    services/            # business services
    rag/                 # loader, splitter, embeddings, prompt, LLM
    tasks/               # background indexing task
  main.py
  requirements.txt
  Dockerfile

rag-vue-ui/
  src/
    api/                 # Axios clients
    views/               # Login, Chat, Knowledge Base pages
    components/          # Chat UI components
    router/              # Vue Router
  package.json
  vite.config.js
  Dockerfile
  nginx.conf

docker-compose.yml
.env.example
README.md
```

## Environment Variables

Copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

Edit `.env` and fill in your Zhipu API key:

```env
ZHIPU_API_KEY=your-zhipu-api-key
SECRET_KEY=replace-with-a-long-random-secret
REDIS_ENABLED=false
```

For local development, `REDIS_ENABLED=false` is recommended unless Redis is installed locally.

## Local Development

### Backend

Use Python 3.11. Do not use Python 3.14 because many AI/RAG dependencies are not fully compatible yet.

If using the Conda environment created during development:

```powershell
cd D:\大四上\assistance\backend
C:\Users\ohhy\.conda\envs\rag311\python.exe -m uvicorn main:app --reload --port 8080
```

Generic Python 3.11 setup:

```powershell
cd backend
python -m pip install -r requirements.txt -i https://pypi.org/simple
python -m uvicorn main:app --reload --port 8080
```

Backend API docs:

```text
http://localhost:8080/docs
```

### Frontend

PowerShell may block `npm.ps1`. Use `npm.cmd`:

```powershell
cd rag-vue-ui
npm.cmd install
npm.cmd run dev
```

Open:

```text
http://localhost:5173
```

## Docker Compose

If Docker is installed:

```powershell
copy .env.example .env
docker compose up --build
```

Open:

```text
http://localhost:5173
```

## Main API Endpoints

### Auth

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

### Documents

- `POST /api/v1/documents/upload`
- `GET /api/v1/documents`
- `DELETE /api/v1/documents/{document_id}`

### Knowledge Base

- `GET /api/v1/knowledge-bases/status`

### Chat

- `POST /api/v1/chat/ask`

## Resume Description

Built an enterprise-style private knowledge base RAG Q&A system using FastAPI, Vue 3, LangChain, ChromaDB, and Zhipu GLM-4. The system supports user authentication, document upload, background vector indexing, user-level knowledge isolation, retrieval-augmented generation, source tracing, Redis-ready cache and rate limiting, and Docker-based deployment.

## Resume Bullet Points

- Implemented a complete RAG pipeline with document parsing, text splitting, ZhipuAI Embedding, ChromaDB vector storage, similarity retrieval, prompt assembly, and GLM-4 answer generation.
- Designed JWT authentication and user-level knowledge base isolation by storing `user_id` and `document_id` in ChromaDB metadata and filtering retrieval results per authenticated user.
- Added asynchronous document indexing with FastAPI BackgroundTasks to avoid blocking upload requests during parsing, embedding, and vector persistence.
- Introduced Redis-ready hot question cache and user-level request rate limiting to reduce repeated LLM calls and improve API stability.
- Containerized the frontend, backend, and Redis services with Docker Compose and added environment-based configuration for API keys, database path, upload storage, and Chroma persistence.

## Notes

- Never commit `.env`, uploaded documents, ChromaDB data, SQLite databases, logs, or `node_modules`.
- Use Python 3.11 for the backend.
- Use `npm.cmd` on Windows PowerShell if `npm run dev` is blocked by execution policy.
