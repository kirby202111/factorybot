# -*- coding: utf-8 -*-
"""AgentScope FastAPI application factory."""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from factorybot.core import config as settings


def _cors_origins() -> list[str]:
    return [o.strip() for o in settings.CORS_ALLOW_ORIGINS.split(",")]


def _default_mcps():
    from agentscope.mcp import HttpMCPConfig, MCPClient, StdioMCPConfig

    mcps = [
        MCPClient(
            name="browser-use",
            mcp_config=StdioMCPConfig(
                command="npx",
                args=["@playwright/mcp@latest"],
            ),
            is_stateful=True,
        ),
    ]

    amap_key = os.getenv("AMAP_API_KEY")
    if amap_key:
        mcps.append(
            MCPClient(
                name="amap",
                mcp_config=HttpMCPConfig(
                    url=f"https://mcp.amap.com/mcp?key={amap_key}",
                ),
                is_stateful=False,
            ),
        )

    return mcps


def _redis_storage():
    from agentscope.app import RedisStorage

    return RedisStorage(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
    )


def _workspace_manager():
    from agentscope.app import LocalWorkspaceManager

    return LocalWorkspaceManager(
        basedir=settings.WORKSPACES_DIR,
        default_mcps=_default_mcps(),
    )


def _create_minimal_app() -> FastAPI:
    app = FastAPI(title="factorybot")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def _create_redis_app() -> FastAPI:
    from agentscope.app import create_app

    return create_app(
        _redis_storage(),
        workspace_manager=_workspace_manager(),
        extra_middlewares=[
            Middleware(
                CORSMiddleware,
                allow_origins=_cors_origins(),
                allow_methods=["*"],
                allow_headers=["*"],
            ),
        ],
        title="factorybot",
    )


def create_agentscope_app() -> FastAPI:
    """USE_REDIS=true 时启用 AgentScope + Redis 完整服务，否则为精简 FastAPI。"""
    if settings.USE_REDIS:
        return _create_redis_app()
    return _create_minimal_app()
