from fastapi import FastAPI

from app.api.routes import health, samples
from app.core.config import settings


def create_app() -> FastAPI:
    """创建 FastAPI 应用并注册所有 API 路由。"""
    app = FastAPI(title=settings.app_name)
    app.include_router(health.router, prefix="/api")
    app.include_router(samples.router, prefix="/api")
    return app


app = create_app()
