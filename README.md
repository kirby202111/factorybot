# factorybot

基于 [AgentScope](https://github.com/agentscope-ai/agentscope) 的 Agent 服务（Agent / Session / Chat / MCP / 定时任务等 API）。

## 项目结构

```
factorybot/                 # 项目根
├── factorybot/             # Python 包
│   ├── app.py              # FastAPI 应用组装
│   ├── core/
│   │   ├── config.py       # 环境变量配置
│   │   └── agentscope.py   # AgentScope 应用工厂
│   ├── api/                # API 路由
│   ├── agents/             # Agent 业务逻辑
│   ├── tools/              # AgentScope 工具
│   └── schemas/            # Pydantic 模型
├── main.py                 # 本地开发入口
└── pyproject.toml
```

## 前置条件

- Python ≥ 3.12，[uv](https://docs.astral.sh/uv/)
- **Redis**（`USE_REDIS=true` 时需要）
- `DASHSCOPE_API_KEY`（对话模型）

## 启动

```bash
uv sync
cp .env.example .env
uv run factorybot
# 或
uv run uvicorn factorybot.app:create_app --factory --port 8100 --reload
# 或
uv run python main.py
```

- API 文档：http://127.0.0.1:8100/docs

### 环境变量

| 变量 | 说明 |
|------|------|
| `DASHSCOPE_API_KEY` | 通义 / DashScope API Key |
| `USE_REDIS` | 启用 AgentScope 完整服务（默认 `false`） |
| `REDIS_HOST` / `REDIS_PORT` / `REDIS_DB` | Redis 连接（默认 `localhost:6379/0`） |
| `AMAP_API_KEY` | 可选，配置后自动注册高德 MCP |
| `WORKSPACES_DIR` | Agent 工作区目录（默认项目根下 `workspaces/`） |
| `PORT` | 服务端口（默认 `8100`） |

### 默认 MCP

- **browser-use**：`npx @playwright/mcp@latest`（需本机已安装 Node.js）
- **amap**：仅在设置 `AMAP_API_KEY` 时启用

## 额外接口（演示 / 调试）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 欢迎页 |
| GET | `/health` | 健康检查 |
| POST | `/tool-test` | 简单 Agent 调用（JSON） |
| POST | `/tool-test/sse` | SSE 流式 |
| POST | `/tool-test/stream` | NDJSON 流式 |

### AgentScope 内置 API（节选）

| 前缀 | 说明 |
|------|------|
| `/agent/` | Agent CRUD |
| `/sessions/` | 会话 |
| `/chat/` | 流式对话 |
| `/credential/` | 凭证 |
| `/workspace/` | MCP / Skill |
| `/schedule/` | 定时任务 |

详见 `/docs`。
