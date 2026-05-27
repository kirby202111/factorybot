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


async def stream_reply(agent: Agent, inputs) -> None:
    pending_confirm: RequireUserConfirmEvent | None = None

    async for evt in agent.reply_stream(inputs):
        match evt.type:
            case EventType.TEXT_BLOCK_DELTA:
                print(evt.delta, end="", flush=True)
            case EventType.REQUIRE_USER_CONFIRM:
                pending_confirm = evt
            case EventType.REPLY_END:
                print()

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
        await stream_reply(agent, confirm)


async def tool_test() -> None:
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

    user_message = "告诉我现在的美国时间。"
    print(f"用户: {user_message}\n")
    print("Friday: ", end="", flush=True)
    await stream_reply(agent, UserMsg("Tony", user_message))


if __name__ == "__main__":
    asyncio.run(main())
