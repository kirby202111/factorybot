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
| POST | `/tool-test` | 调用 agent |
