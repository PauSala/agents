from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from core.inference_guard import InferenceGuard, InvalidResponse
from core.llm_wrapper import LLM
from inspect import cleandoc

T = TypeVar("T")


class BaseAgent(ABC, Generic[T]):
    def __init__(self, llm: LLM):
        self.llm = llm
        self.guard = InferenceGuard()

    @abstractmethod
    def run(self, task: str) -> T | InvalidResponse:
        """Subclasses must implement this to provide their specific run."""
        pass
    
    @abstractmethod
    def build_prompt(self, task: str) -> str:
        """Subclasses must implement this to provide their specific prompt."""
        pass

    def json_output_instructions(self, schema: str) -> str:
        """
        Generates the standardized Output Format and Constraints block
        with a custom JSON schema interpolated inside.
        """
        return cleandoc(f"""
            ### OUTPUT FORMAT
            Output ONLY a raw JSON object. No markdown blocks, no conversational text, and no quotes outside the JSON.
            {schema}
    
            ### STRICT NEGATIVE CONSTRAINTS
            - NO code snippets or logic (e.g., no 'for loops', 'imports', or 'functions').
            - NO formatting symbols or backticks.
            - NO mentions of tool metadata or documentation.
            - NO conversational filler.
        """)
