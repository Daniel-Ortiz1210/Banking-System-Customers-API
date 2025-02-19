import logging

from fastapi import FastAPI
from fastapi_pagination import add_pagination
import uvicorn

from src.utils.config import Config
from src.api.router import version_router

settings = Config()

app = FastAPI(
    title=settings.app_name,
    description='A simple API to manage customers',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json',
)
app.include_router(version_router)
add_pagination(app)

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=settings.host,
        port=settings.port,
    )
