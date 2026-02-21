from typing import Optional, Any
from pydantic import BaseModel
from enum import Enum

class DecisionType(Enum):
    EXPLAIN = "explain"
    TOOL = "tool"
    CODE = "code"
    FAIL = "fail"


class AgentDecision(BaseModel):
    type: DecisionType
    content: Optional[str] = None
    tool: Optional[dict[str, Any]] = None
    reason: Optional[str] = None