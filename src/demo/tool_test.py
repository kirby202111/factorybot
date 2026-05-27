from collections.abc import AsyncIterator

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


def _build_agent() -> Agent:
    return Agent(
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


async def stream_reply_chunks(agent: Agent, inputs) -> AsyncIterator[str]:
    pending_confirm: RequireUserConfirmEvent | None = None

    async for evt in agent.reply_stream(inputs):
        match evt.type:
            case EventType.TEXT_BLOCK_DELTA:
                yield evt.delta
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
        async for chunk in stream_reply_chunks(agent, confirm):
            yield chunk


async def stream_reply(agent: Agent, inputs) -> str:
    parts: list[str] = []
    async for chunk in stream_reply_chunks(agent, inputs):
        parts.append(chunk)
    return "".join(parts)


async def tool_test(user_message: str = "告诉我现在的美国时间。") -> str:
    agent = _build_agent()
    return await stream_reply(agent, UserMsg("Tony", user_message))


async def tool_test_stream(
    user_message: str = "告诉我现在的美国时间。",
) -> AsyncIterator[str]:
    agent = _build_agent()
    async for chunk in stream_reply_chunks(agent, UserMsg("Tony", user_message)):
        yield chunk


if __name__ == "__main__":
    async def _main() -> None:
        async for chunk in tool_test_stream():
            print(chunk, end="", flush=True)
        print()

    asyncio.run(_main())
