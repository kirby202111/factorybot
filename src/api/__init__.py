from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="factorybot")

    from api.health import router as health_router
    from api.index import router as index_router
    from api.tool_test import router as tool_test_router

    app.include_router(index_router)
    app.include_router(health_router, prefix="/health")
    app.include_router(tool_test_router, prefix="/tool-test")

    return app
