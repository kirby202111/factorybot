from agentscope.agent import Agent
from agentscope.tool import Toolkit, Bash, Grep, Glob, Read, Write, Edit
from agentscope.credential import DashScopeCredential
from agentscope.model import DashScopeChatModel
from agentscope.message import UserMsg
from agentscope.event import EventType

import asyncio
import os

from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    agent = Agent(
        name="Friday",
        system_prompt="You're a helpful assistant named Friday.",
        model=DashScopeChatModel(
            credential=DashScopeCredential(
                api_key=os.environ["DASHSCOPE_API_KEY"],
            ),
            model="qwen3.6-plus",
        ),
        toolkit=Toolkit(
            tools=[
                Bash(),
                Grep(),
                Glob(),
                Read(),
                Write(),
                Edit(),
            ]
        ),
    )

    user_message = "请用一句话介绍特朗普。"
    print(f"用户: {user_message}\n")
    print("Friday: ", end="", flush=True)

    async for evt in agent.reply_stream(UserMsg("Tony", user_message)):
        match evt.type:
            case EventType.TEXT_BLOCK_DELTA:
                print(evt.delta, end="", flush=True)
            case EventType.REPLY_END:
                print()

asyncio.run(main())