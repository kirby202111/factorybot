from agentscope.agent import Agent
from agentscope.tool import Toolkit, Bash, Grep, Glob, Read, Write, Edit
from agentscope.credential import DashScopeCredential
from agentscope.model import DashScopeChatModel
from agentscope.message import UserMsg
from agentscope.event import (
    ConfirmResult,
    EventType,
    RequireUserConfirmEvent,
    UserConfirmResultEvent,
)
import asyncio
import os

from dotenv import load_dotenv

from tools import get_current_time_tool

load_dotenv()


async def stream_reply(agent: Agent, inputs) -> str:
    pending_confirm: RequireUserConfirmEvent | None = None
    parts: list[str] = []

    async for evt in agent.reply_stream(inputs):
        match evt.type:
            case EventType.TEXT_BLOCK_DELTA:
                parts.append(evt.delta)
            case EventType.REQUIRE_USER_CONFIRM:
                pending_confirm = evt
            case EventType.REPLY_END:
                pass

    if pending_confirm is not None:
        confirm = UserConfirmResultEvent(
            reply_id=pending_confirm.reply_id,
            confirm_results=[
                ConfirmResult(
                    confirmed=True,
                    tool_call=tool_call,
                    rules=tool_call.suggested_rules,
                )
                for tool_call in pending_confirm.tool_calls
            ],
        )
        return await stream_reply(agent, confirm)

    return "".join(parts)


async def tool_test(user_message: str = "告诉我现在的美国时间。") -> str:
    agent = Agent(
        name="Friday",
        system_prompt="You're a helpful assistant named Friday.",
        model=DashScopeChatModel(
            credential=DashScopeCredential(
                api_key=os.environ["DASHSCOPE_API_KEY"],
            ),
            model="gui-plus-2026-02-26",
        ),
        toolkit=Toolkit(
            tools=[
                get_current_time_tool,
                # Bash(),
                # Grep(),
                # Glob(),
                # Read(),
                # Write(),
                # Edit()
            ]
        ),
    )

    return await stream_reply(agent, UserMsg("Tony", user_message))


if __name__ == "__main__":
    reply = asyncio.run(tool_test())
    print(reply)
