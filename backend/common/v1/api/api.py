from fastapi import APIRouter

from app.api.endpoints import file_management 

api_router = APIRouter()

api_router.include_router(file_management.router, tags=["Files"])