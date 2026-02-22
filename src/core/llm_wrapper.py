from typing import Any, List

from mcp import Tool
import requests


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
    
    ## TODO: add this to base model
    def generate_with_tools(self, prompt: str,  tools: List[Tool] = []) -> dict[str, Any]:
            # Convert MCP tools to Ollama-friendly tool definitions
            ollama_tools: List[dict[str, Any]] = []
            for tool in tools:
                ollama_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    }
                })

            payload: dict[str, Any]  = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "tools": ollama_tools, 
                "stream": False,
            }

            response = requests.post(f"{self.base_url}/api/chat", json=payload)
            response.raise_for_status()
                
            # Return the whole message object (contains 'content' AND 'tool_calls')
            return response.json()
