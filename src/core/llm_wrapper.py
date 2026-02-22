import requests
from typing import Any


class LLM:
    def __init__(
        self,
        model: str = "qwen2.5-coder:14b",
        base_url: str = "http://localhost:11434",
        timeout: int = 60,
    ):
        self.model = model
        self.base_url = base_url
        self.timeout = timeout

    def generate(self, prompt: str, format: dict[str, Any] | None = None) -> str:
        url = f"{self.base_url}/api/generate"

        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        if format is not None:
            payload["format"] = format

        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()

        return response.json()["response"]