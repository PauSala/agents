from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


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