# factorybot

基于 [AgentScope](https://github.com/agentscope-ai/agentscope) 的 Agent 服务（Agent / Session / Chat / MCP / 定时任务等 API）。

## 前置条件

- Python ≥ 3.12，[uv](https://docs.astral.sh/uv/)
- **Redis**（本地或远程，用于持久化 Agent、会话、凭证等）
- `DASHSCOPE_API_KEY`（对话模型）

## 启动 Agent 服务

```bash
uv sync
cp .env.example .env   # 配置 DASHSCOPE_API_KEY、Redis 等
# 确保 Redis 已运行，例如: docker run -d -p 6379:6379 redis:7-alpine
uv run uvicorn main:app --port 8100 --reload
# 或
uv run python main.py
```

- API 文档：http://127.0.0.1:8100/docs  

### 环境变量

| 变量 | 说明 |
|------|------|
| `DASHSCOPE_API_KEY` | 通义 / DashScope API Key |
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
