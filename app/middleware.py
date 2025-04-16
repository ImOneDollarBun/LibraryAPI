from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from sqlalchemy.orm import Session
import time
from app.database.models import Logs
from app.database import SessionLocal


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        body = await request.body()
        response = await call_next(request)

        duration = round((time.time() - start_time) * 1000)
        session: Session = SessionLocal()

        log = Logs(
            level="INFO",
            message=f"{request.method} {request.url.path} - {response.status_code}",
            context={
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "status_code": response.status_code,
                "duration_ms": duration,
                "body": body.decode("utf-8") if body else None
            }
        )

        session.add(log)
        session.commit()
        session.close()

        return response
