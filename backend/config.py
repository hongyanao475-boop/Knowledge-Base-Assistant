import os


API_KEY = os.getenv("ZHIPU_API_KEY", "")
BASE_URL = os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
MODEL_NAME = os.getenv("LLM_MODEL_NAME", "glm-4")

PRIVATE_DOCS_DIR = os.getenv("UPLOAD_DIR", "./data/uploads")
VECTOR_DB_PATH = os.getenv("CHROMA_PATH", "./data/chroma")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL_NAME", "embedding-2")
