import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    backend_dir = Path(__file__).resolve().parents[2]
    project_dir = backend_dir.parent
    load_dotenv(project_dir / ".env")
    load_dotenv(backend_dir / ".env")
except Exception:
    pass


class Settings:
    APP_NAME = os.getenv("APP_NAME", "RAGHub AI Knowledge Base")
    APP_ENV = os.getenv("APP_ENV", "dev")
    API_V1_PREFIX = "/api/v1"

    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    ALGORITHM = "HS256"

    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
    ZHIPU_BASE_URL = os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "glm-4")
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "embedding-2")

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_ENABLED = os.getenv("REDIS_ENABLED", "true").lower() == "true"

    BASE_DIR = Path(__file__).resolve().parents[2]
    DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
    UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", DATA_DIR / "uploads"))
    CHROMA_PATH = Path(os.getenv("CHROMA_PATH", DATA_DIR / "chroma"))

    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")

    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "20"))
    RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "3"))
    QA_CACHE_TTL_SECONDS = int(os.getenv("QA_CACHE_TTL_SECONDS", "600"))
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "20"))


settings = Settings()


def ensure_runtime_dirs() -> None:
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    settings.CHROMA_PATH.mkdir(parents=True, exist_ok=True)
