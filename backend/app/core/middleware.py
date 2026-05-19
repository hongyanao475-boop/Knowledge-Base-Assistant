import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


logger = logging.getLogger("request")


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start = time.perf_counter()
        request.state.request_id = request_id
        try:
            response = await call_next(request)
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            response.headers["X-Request-ID"] = request_id
            logger.info(
                "request_id=%s method=%s path=%s status=%s latency_ms=%s",
                request_id,
                request.method,
                request.url.path,
                response.status_code,
                latency_ms,
            )
            return response
        except Exception:
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.exception(
                "request_id=%s method=%s path=%s latency_ms=%s error=unhandled",
                request_id,
                request.method,
                request.url.path,
                latency_ms,
            )
            raise
