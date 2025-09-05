import logging
import time
from collections.abc import Callable

from fastapi.openapi.models import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("fastapi")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging all incoming HTTP requests in FastAPI.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """
        Processes an incoming request, logs its information,
        and returns the response.
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - Time: {process_time:.2f}ms"
        )
        return response
