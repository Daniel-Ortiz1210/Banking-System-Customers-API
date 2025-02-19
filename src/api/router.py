from fastapi import APIRouter

from src.api.customers import router as customers_router
from src.api.auth import router as auth_router

version_router = APIRouter(prefix='/api/v1')
version_router.include_router(customers_router)
version_router.include_router(auth_router)
