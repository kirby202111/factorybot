# factorybot

基于 AgentScope 的 FastAPI 服务。

## 启动

```bash
uv sync
cp .env.example .env   # 配置 DASHSCOPE_API_KEY
uv run uvicorn main:app --port 8100 --reload
```

浏览器打开 http://127.0.0.1:8100 ；API 文档见 http://127.0.0.1:8100/docs。

## 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 欢迎页 |
| GET | `/health` | 健康检查 |
| POST | `/tool-test` | 调用 agent（一次性 JSON） |
| POST | `/tool-test/sse` | **SSE** 流式（`text/event-stream`） |
| POST | `/tool-test/stream` | **Streamable HTTP** 流式（`application/x-ndjson`） |

### 两种流式对比

| | SSE `/tool-test/sse` | Streamable HTTP `/tool-test/stream` |
|---|---|---|
| Content-Type | `text/event-stream` | `application/x-ndjson` |
| 数据格式 | `event:` + `data:` 行 | 每行一个 JSON |
| 典型客户端 | `EventSource` | `fetch` + `ReadableStream` |

**SSE：**
```bash
curl -N -X POST http://127.0.0.1:8100/tool-test/sse \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Tell me the current US time.\"}"
```

**Streamable HTTP（NDJSON）：**
```bash
curl -N -X POST http://127.0.0.1:8100/tool-test/stream \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Tell me the current US time.\"}"
```
