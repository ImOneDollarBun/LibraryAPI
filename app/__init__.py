from fastapi import APIRouter
from app.endpoints.routes import router

rout = APIRouter()
rout.include_router(router)