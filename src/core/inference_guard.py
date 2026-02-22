import json
import re
from typing import Type, TypeVar

from pydantic import BaseModel

from core.llm_wrapper import LLM

T = TypeVar("T", bound=BaseModel)

class TextResponse(BaseModel):
    response: str

class InvalidResponse(BaseModel):
    reason: str


class InferenceGuard:

    def __init__(self, llm: LLM, max_retries: int = 3):
        self.llm = llm
        self.max_retries = max_retries

    def parse_json(self, text: str):
        try:
            return json.loads(text)
        except Exception:
            return None

    def strip_code_fences(self, text: str) -> str:
        text = text.strip()
        match = re.search(r"```\w*\n(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text
        
    def run_structured_inference(self, prompt: str, schema: Type[T]) -> T | None:
        """Run inference + validation with retry."""

        for _ in range(self.max_retries):
            output = self.llm.generate(prompt)
            parsed = self.parse_json(self.strip_code_fences(output))

            if parsed is None:
                continue

            try:
                return schema(**parsed)
            except Exception:
                continue

        return None
    
    def run_text_inference(self, prompt: str) -> TextResponse | None:
        """Run inference and wrap model output into {response: text}."""

        for _ in range(self.max_retries):
            try:
                output = self.llm.generate(prompt)
                return TextResponse(response=output)
            except Exception:
                continue

        return None
