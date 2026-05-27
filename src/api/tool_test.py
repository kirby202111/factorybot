from fastapi import APIRouter

from demo.tool_test import tool_test
from schemas.tool_test import ToolTestRequest, ToolTestResponse

router = APIRouter(tags=["tool-test"])


@router.post("", response_model=ToolTestResponse)
async def tool_test_endpoint(request: ToolTestRequest) -> ToolTestResponse:
    reply = await tool_test(request.message)
    return ToolTestResponse(reply=reply)
