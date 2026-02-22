from enum import Enum
from typing import Optional

from pydantic import BaseModel


class DecisionType(Enum):
    EXPLAIN = "explain"
    TOOL = "tool"
    CODE = "code"
    FAIL = "fail"


class AgentDecision(BaseModel):
    type: DecisionType
    content: Optional[str] = None
    reason: Optional[str] = None
