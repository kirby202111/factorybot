# -*- coding: utf-8 -*-
"""Application configuration loaded from environment variables."""
import os
from pathlib import Path


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "on")


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# 启用后使用 AgentScope 完整服务（agents、sessions、chat、MCP 等），需本地 Redis。
USE_REDIS = _env_bool("USE_REDIS", False)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None

WORKSPACES_DIR = os.getenv("WORKSPACES_DIR", str(PROJECT_ROOT / "workspaces"))
CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*")
