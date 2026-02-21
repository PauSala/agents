from typing import Optional
from pydantic import BaseModel


class AgentResponse(BaseModel):
    type: str
    content: Optional[str] = None
    tool: Optional[dict] = None
    reason: Optional[str] = None
