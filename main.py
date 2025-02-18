import logging

from fastapi import FastAPI
import uvicorn

from src.api.router import version_router

app = FastAPI(
    title='Customers API',
    description='A simple API to manage customers',
    version='0.1',
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json',
)
app.include_router(version_router)

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=8000,
    )
