# -*- coding: utf-8 -*-
"""AgentScope FastAPI application factory."""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Redis / AgentScope 完整服务（agents、sessions、chat、MCP 等）暂禁，恢复时需本地 Redis。
# from agentscope.app import (
#     LocalWorkspaceManager,
#     RedisStorage,
#     create_app,
# )
# from agentscope.mcp import HttpMCPConfig, MCPClient, StdioMCPConfig

# _PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
#
#
# def _default_mcps() -> list[MCPClient]:
#     mcps: list[MCPClient] = [
#         MCPClient(
#             name="browser-use",
#             mcp_config=StdioMCPConfig(
#                 command="npx",
#                 args=["@playwright/mcp@latest"],
#             ),
#             is_stateful=True,
#         ),
#     ]
#
#     amap_key = os.getenv("AMAP_API_KEY")
#     if amap_key:
#         mcps.append(
#             MCPClient(
#                 name="amap",
#                 mcp_config=HttpMCPConfig(
#                     url=f"https://mcp.amap.com/mcp?key={amap_key}",
#                 ),
#                 is_stateful=False,
#             ),
#         )
#
#     return mcps
#
#
# def _redis_storage() -> RedisStorage:
#     return RedisStorage(
#         host=os.getenv("REDIS_HOST", "localhost"),
#         port=int(os.getenv("REDIS_PORT", "6379")),
#         db=int(os.getenv("REDIS_DB", "0")),
#         password=os.getenv("REDIS_PASSWORD") or None,
#     )
#
#
# def _workspace_manager() -> LocalWorkspaceManager:
#     basedir = os.getenv(
#         "WORKSPACES_DIR",
#         str(_PROJECT_ROOT / "workspaces"),
#     )
#     return LocalWorkspaceManager(
#         basedir=basedir,
#         default_mcps=_default_mcps(),
#     )


def create_agentscope_app() -> FastAPI:
    """应用入口；AgentScope + Redis 完整服务恢复后改回 create_app(...)。"""
    cors_origins = os.getenv("CORS_ALLOW_ORIGINS", "*")
    app = FastAPI(title="factorybot")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in cors_origins.split(",")],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

    # cors_origins = os.getenv("CORS_ALLOW_ORIGINS", "*")
    # return create_app(
    #     _redis_storage(),
    #     workspace_manager=_workspace_manager(),
    #     extra_middlewares=[
    #         Middleware(
    #             CORSMiddleware,
    #             allow_origins=[o.strip() for o in cors_origins.split(",")],
    #             allow_methods=["*"],
    #             allow_headers=["*"],
    #         ),
    #     ],
    #     title="factorybot",
    # )
