import os
from typing import Optional

from langchain_core.embeddings import Embeddings
from zhipuai import ZhipuAI

from app.core.config import settings


class ZhipuAIEmbeddings(Embeddings):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.client = ZhipuAI(api_key=api_key or settings.ZHIPU_API_KEY or os.getenv("ZHIPU_API_KEY"))
        self.model = model or settings.EMBEDDING_MODEL_NAME

    def embed_documents(self, texts):
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text):
        response = self.client.embeddings.create(model=self.model, input=text)
        return response.data[0].embedding
