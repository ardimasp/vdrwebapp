from fastapi import APIRouter

from app.api.endpoints import file_management, login 

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])
api_router.include_router(file_management.router, tags=["Files"])