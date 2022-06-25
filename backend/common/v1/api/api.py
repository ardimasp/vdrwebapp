from fastapi import APIRouter

from app.api.endpoints import file_management, login, showcase, vtpviewer 

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])
api_router.include_router(file_management.router, tags=["Files"])
api_router.include_router(showcase.router, tags=["Showcase"])
api_router.include_router(vtpviewer.router, tags=["VTP Viewer"])