import json
from typing import Type, TypeVar

from pydantic import BaseModel

from core.llm_wrapper import LLM

T = TypeVar("T", bound=BaseModel)

class TextResponse(BaseModel):
    response: str

class InvalidResponse(BaseModel):
    reason: str


class InferenceGuard:

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def parse_json(self, text: str):
        try:
            return json.loads(text)
        except Exception:
            return None
        
    # TODO: This is bullshit fuck LLMs
    def strip_code_fences(self, text: str) -> str:
        text = text.strip()

        if text.startswith("```"):
            lines = text.splitlines()
            lines = lines[1:]

            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        return text
        
    def run_structured_inference(self, llm: LLM, prompt: str, schema: Type[T]) -> T | None:
        """
        Run inference + validation with retry.
        """

        for _ in range(self.max_retries):

            output = llm.generate(prompt)
            print(output)
            parsed = self.parse_json(self.strip_code_fences(output))

            if parsed is None:
                continue

            try:
                return schema(**parsed)
            except Exception:
                continue

        return None
    
    def run_text_inference(self, llm: LLM, prompt: str) -> TextResponse| None:
        """
        Run inference and wrap model output into {response: text}.
        """

        for _ in range(self.max_retries):

            output = llm.generate(prompt)
            return TextResponse(response=output)

        return None