import uvicorn
from fastapi import FastAPI
from settings import settings
from app import rout
from app.middleware import LoggingMiddleware

app = FastAPI()
app.include_router(rout)
app.add_middleware(LoggingMiddleware)

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.App.APP_HOST, port=settings.App.APP_PORT)