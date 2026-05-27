from pydantic import BaseModel, Field


class ToolTestRequest(BaseModel):
    message: str = Field(
        default="告诉我现在的美国时间。",
        description="User message sent to the agent.",
    )


class ToolTestResponse(BaseModel):
    reply: str
