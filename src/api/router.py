from fastapi import APIRouter

from src.api.customers import router as users_router
from src.api.auth import router as auth_router
from src.api.services import router as services_router

version_router = APIRouter(prefix='/api/v1')
version_router.include_router(users_router)
version_router.include_router(auth_router)
version_router.include_router(services_router)
