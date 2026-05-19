from langchain_community.chat_models import ChatZhipuAI

from app.core.config import settings


_llm = None


def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatZhipuAI(
            model_name=settings.LLM_MODEL_NAME,
            api_key=settings.ZHIPU_API_KEY,
            base_url=settings.ZHIPU_BASE_URL,
        )
    return _llm
