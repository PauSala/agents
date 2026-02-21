from abc import ABC, abstractmethod
from typing import Any

from agents.decision_response import AgentDecision
from agents.types import ToolCall, ToolSelection
from core.inference_guard import InferenceGuard, InvalidResponse, TextResponse
from core.llm_wrapper import LLM


class BaseAgent(ABC):
    def __init__(self, llm: LLM):
        self.llm = llm
        self.guard = InferenceGuard()


    @abstractmethod
    def run(self, task: str) -> AgentDecision | TextResponse | InvalidResponse | ToolSelection |  ToolCall | dict[str, Any]:
        """Subclasses must implement this to provide their specific run."""
        pass
    
    @abstractmethod
    def build_prompt(self, task: str) -> str:
        """Subclasses must implement this to provide their specific prompt."""
        pass
