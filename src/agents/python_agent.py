from typing import Any

from agents.base_agent import BaseAgent
from agents.types import ToolCall
from core.inference_guard import InvalidResponse
from core.llm_wrapper import LLM
from tools.python_tool import PythonCodeTool


class PythonAgent(BaseAgent):
    """Agent that directly executes Python tool."""

    def __init__(self, llm: LLM):
        super().__init__(llm)
        self.python_tool = PythonCodeTool()

    def run(self, task: str) -> InvalidResponse | dict[str, Any]:
        """Execute Python task."""

        prompt = self.build_prompt(task)

        parsed = self.guard.run_structured_inference(
            self.llm,
            prompt,
            ToolCall
        )

        print(parsed)

        if parsed is None:
            return InvalidResponse(
                reason="Failed to parse tool execution request"
            )

        # Directly execute python tool (no registry lookup)
        try:
            result = self.python_tool.execute(
                self.python_tool.input_schema(
                    **parsed.arguments
                )
            )
            return result.model_dump()
        except Exception as e:
            return InvalidResponse(
                reason=f"Python tool execution failed: {e}"
            )

    def build_prompt(self, task: str) -> str:
        return f"""
You are a Python code writer agent.

You must generate a Python working file to solve the given task, importing built-in modules if necessary.

TASK:
{task}

STRICT OUTPUT RULES:
- Do not generate markdown.
- Do not wrap JSON inside code fences.
- Output ONLY valid JSON.
- The response must start with '{' and end with '}'.
- The Python code must print the final result using print().
- Do not generate any text outside JSON.
- Do not generate greetings or explanations.
- Do not output chain-of-thought reasoning.

OUTPUT FORMAT:

{{
    "arguments": {{
        "code": "python file contents"
    }}
}}

NEGATIVE RULES:
- Never output conversational text.
- Never output ```json or ``` blocks.
- Never add commentary after JSON.
"""