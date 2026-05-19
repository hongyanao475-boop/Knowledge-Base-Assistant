import hashlib
import json
import logging

from app.core.config import settings


logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self) -> None:
        self.client = None
        if not settings.REDIS_ENABLED:
            return
        try:
            import redis

            self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.client.ping()
        except Exception as exc:
            logger.warning("Redis unavailable, cache disabled: %s", exc)
            self.client = None

    @staticmethod
    def question_key(user_id: int, question: str) -> str:
        digest = hashlib.sha256(question.strip().lower().encode("utf-8")).hexdigest()
        return f"qa:{user_id}:{digest}"

    def get_json(self, key: str):
        if not self.client:
            return None
        raw = self.client.get(key)
        return json.loads(raw) if raw else None

    def set_json(self, key: str, value, ttl: int) -> None:
        if self.client:
            self.client.setex(key, ttl, json.dumps(value, ensure_ascii=False))

    def check_rate_limit(self, user_id: int) -> bool:
        if not self.client:
            return True
        key = f"rate:{user_id}"
        count = self.client.incr(key)
        if count == 1:
            self.client.expire(key, 60)
        return count <= settings.RATE_LIMIT_PER_MINUTE


cache_service = CacheService()
