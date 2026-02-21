from typing import Any
from inspect import cleandoc
from agents.base_agent import BaseAgent
from agents.types import ToolCall
from core.inference_guard import InvalidResponse
from core.llm_wrapper import LLM
from tools.python_tool import PythonCodeTool

class PythonAgent(BaseAgent):
    def __init__(self, llm: LLM, max_retries: int = 2):
        super().__init__(llm)
        self.python_tool = PythonCodeTool()
        self._max_retries_limit = max_retries
        self.current_retries = 0
        
        self.code_schema = cleandoc("""
            {
                "arguments": {
                    "code": "A string containing valid, PEP8 compliant Python code. Use standard newline characters (\\n)."
                }
            }
        """)

    def run(self, task: str, previous_error: str | None = None, failed_code: str = "") -> Any:
        if previous_error and failed_code:
            prompt = self.build_fix_prompt(task, failed_code, previous_error)
        else:
            self.current_retries = 0 
            prompt = self.build_prompt(task)

        parsed = self.guard.run_structured_inference(self.llm, prompt, ToolCall)

        if not parsed:
            return InvalidResponse(reason="Failed to parse code execution request")

        code_attr = parsed.arguments.get("code")
        if not isinstance(code_attr, str):
            return InvalidResponse(reason="LLM returned non-string code attribute")

        try:
            input_data = self.python_tool.input_schema(code=code_attr)
            result = self.python_tool.execute(input_data)
            
            if not result.success and self.current_retries < self._max_retries_limit:
                self.current_retries += 1
                return self.run(task, previous_error=result.error, failed_code=code_attr)
            
            return result.model_dump()

        except Exception as e:
            if self.current_retries < self._max_retries_limit:
                self.current_retries += 1
                return self.run(task, previous_error=str(e), failed_code=code_attr)
            return InvalidResponse(reason=f"Python tool failed after retries: {e}")

    def build_fix_prompt(self, task: str, failed_code: str, error: str) -> str:
        output_constraints = self.json_output_instructions(self.code_schema)
        return cleandoc(f"""
            The previous Python code you generated failed. Fix it.

            ### ORIGINAL TASK
            {task}

            ### FAILED CODE
            {failed_code}

            ### ERROR MESSAGE
            {error}

            {output_constraints}
        """)

    def build_prompt(self, task: str) -> str:
        output_constraints = self.json_output_instructions(self.code_schema)
        return cleandoc(f"""
            Act as a deterministic Python Code Generator.

            ### TASK
            Generate a Python script that executes the following task and prints the final result:
            {task}

            {output_constraints}
            - The Python code MUST include a print() statement for the final result.
        """)