import json
from collections.abc import AsyncIterable

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from fastapi.sse import EventSourceResponse, ServerSentEvent

from factorybot.agents.tool_test import tool_test, tool_test_stream
from factorybot.schemas.tool_test import ToolTestRequest, ToolTestResponse

router = APIRouter(tags=["tool-test"])


@router.post("", response_model=ToolTestResponse)
async def tool_test_endpoint(request: ToolTestRequest) -> ToolTestResponse:
    reply = await tool_test(request.message)
    return ToolTestResponse(reply=reply)


@router.post("/sse", response_class=EventSourceResponse)
async def tool_test_sse_endpoint(
    body: ToolTestRequest,
    request: Request,
) -> AsyncIterable[ServerSentEvent]:
    """SSE：text/event-stream，浏览器可用 EventSource 消费。"""
    async for chunk in tool_test_stream(body.message):
        if await request.is_disconnected():
            break
        yield ServerSentEvent(data={"delta": chunk}, event="token")
    yield ServerSentEvent(data="[DONE]", event="done")


@router.post("/stream")
async def tool_test_streamable_http_endpoint(
    body: ToolTestRequest,
    request: Request,
) -> StreamingResponse:
    """Streamable HTTP：chunked 响应体 + NDJSON（每行一个 JSON）。"""

    async def ndjson_lines():
        async for chunk in tool_test_stream(body.message):
            if await request.is_disconnected():
                break
            yield json.dumps({"delta": chunk}, ensure_ascii=False) + "\n"
        yield json.dumps({"done": True}, ensure_ascii=False) + "\n"

    return StreamingResponse(
        ndjson_lines(),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
