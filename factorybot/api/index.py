from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(tags=["index"])


@router.get("/", response_class=PlainTextResponse)
async def index() -> str:
    return "欢迎使用 factorybot。"
