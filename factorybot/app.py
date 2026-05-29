from fastapi import FastAPI

from factorybot.api import api_router
from factorybot.core.agentscope import create_agentscope_app


def create_app() -> FastAPI:
    """Assemble AgentScope service with project API routes."""
    app = create_agentscope_app()
    app.include_router(api_router)
    return app
