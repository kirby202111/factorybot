from fastapi import APIRouter

from . import health, index, tool_test

api_router = APIRouter()
api_router.include_router(index.router)
api_router.include_router(health.router, prefix="/health")
api_router.include_router(tool_test.router, prefix="/tool-test")

__all__ = ["api_router"]
