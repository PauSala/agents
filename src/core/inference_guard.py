import json
from typing import Type, TypeVar
from pydantic import BaseModel

from core.llm_wrapper import LLM

T = TypeVar("T", bound=BaseModel)


class InferenceGuard:

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def parse_json(self, text: str):
        try:
            return json.loads(text)
        except Exception:
            return None

    def generate_and_validate(self, llm: LLM, prompt: str, schema: Type[T]) -> T | None:
        """
        Run inference + validation with retry.
        """

        for _ in range(self.max_retries):

            output = llm.generate(prompt)
            parsed = self.parse_json(output)

            if parsed is None:
                continue

            try:
                return schema(**parsed)
            except Exception:
                continue

        return None