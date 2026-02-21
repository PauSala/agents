from abc import ABC, abstractmethod
from typing import Any

from agents.decision_response import AgentDecision
from core.inference_guard import InferenceGuard
from core.llm_wrapper import LLM



class BaseAgent(ABC):
    def __init__(self, llm: LLM, tools: dict[str, object] | None = None):
        self.llm = llm
        self.tools = tools or {}
        self.guard = InferenceGuard()


    @abstractmethod
    def run(self, task: str) -> AgentDecision | dict[str, Any] | str:
        """Subclasses must implement this to provide their specific run."""
        pass
    
    @abstractmethod
    def build_prompt(self, task: str) -> str:
        """Subclasses must implement this to provide their specific prompt."""
        pass
