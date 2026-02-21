from typing import Any

from agents.base_agent import BaseAgent
from agents.types import ToolCall
from core.inference_guard import InvalidResponse
from core.llm_wrapper import LLM
from tools.python_tool import PythonCodeTool
from inspect import cleandoc


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
        schema = cleandoc("""
            {
                "arguments": {
                    "code": "A string containing valid, PEP8 compliant Python code. Use line breaks and escape double quotes."
                }
            }
        """)
        output_constraints = self.json_output_instructions(schema)
        return cleandoc(f"""
            Act as a deterministic Python Code Generator. Your output is consumed by a JSON parser.

            ### TASK
            Generate a Python script that executes the following task and prints the final result:
            {task}

            {output_constraints}
            - The Python code MUST include a print() statement for the final result.
            
        """)