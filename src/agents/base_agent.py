from abc import ABC, abstractmethod
from inspect import cleandoc
from typing import Generic, TypeVar

from core.events import NoOpEmitter
from core.inference_guard import InferenceGuard
from core.llm_wrapper import LLM
from core.log_collector import LogCollector
from core.types import Result

T = TypeVar("T")


class BaseAgent(ABC, Generic[T]):
    def __init__(self, id: str, llm: LLM, log: LogCollector | None = None):
        self.id = id
        self.llm = llm
        self.guard = InferenceGuard(llm)
        self.log = log or LogCollector(NoOpEmitter())

    @abstractmethod
    def run(self, task: str, caller_id: str = "") -> Result[T]:
        """Subclasses must implement this to provide their specific run."""
        pass

    @abstractmethod
    def build_prompt(self, task: str) -> str:
        """Subclasses must implement this to provide their specific prompt."""
        pass

    def json_output_instructions(
        self, schema: str, allow_code_in_value: bool = False
    ) -> str:
        """
        Generates the standardized Output Format and Constraints block
        with a custom JSON schema interpolated inside.

        When allow_code_in_value is True, the "no code snippets" constraint
        is omitted so the model can embed code inside JSON string values.
        """
        constraints = [
            "- NO formatting symbols or backticks.",
            "- NO mentions of tool metadata or documentation.",
            "- NO conversational filler.",
        ]
        if not allow_code_in_value:
            constraints.insert(
                0,
                "- NO code snippets or logic (e.g., no 'for loops', 'imports', or 'functions').",
            )

        constraints_block = "\n".join(constraints)

        return cleandoc(f"""
            ### OUTPUT FORMAT
            Output ONLY a raw JSON object. No markdown blocks, no conversational text, and no quotes outside the JSON.
            {schema}
    
            ### STRICT NEGATIVE CONSTRAINTS
            {constraints_block}
        """)
