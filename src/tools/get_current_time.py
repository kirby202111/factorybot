from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from agentscope.message import TextBlock, ToolResultState
from agentscope.tool import FunctionTool, ToolChunk


async def get_current_time(timezone: str = "Asia/Shanghai") -> ToolChunk:
    """Get the current date and time in the given timezone.

    Args:
        timezone (str):
            IANA timezone name, e.g. "Asia/Shanghai" or "UTC".
    """
    try:
        now = datetime.now(ZoneInfo(timezone))
    except ZoneInfoNotFoundError:
        return ToolChunk(
            content=[
                TextBlock(
                    type="text",
                    text=f"Unknown timezone: {timezone}",
                ),
            ],
            state=ToolResultState.ERROR,
            is_last=True,
        )

    return ToolChunk(
        content=[
            TextBlock(
                type="text",
                text=now.strftime("%Y-%m-%d %H:%M:%S %Z"),
            ),
        ],
        is_last=True,
    )


get_current_time_tool = FunctionTool(
    get_current_time,
    name="GetCurrentTime",
    is_read_only=True,
)
