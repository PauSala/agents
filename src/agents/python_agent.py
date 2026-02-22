from inspect import cleandoc

from agents.base_agent import BaseAgent
from agents.types import ToolCall
from core.llm_wrapper import LLM
from core.log_collector import LogCollector
from core.types import Err, Ok, Result
from tools.python_tool import PythonCodeOutput, PythonCodeTool


class PythonAgent(BaseAgent[PythonCodeOutput]):
    def __init__(
        self,
        llm: LLM,
        tool: PythonCodeTool,
        max_retries: int = 6,
        log: LogCollector | None = None,
    ):
        super().__init__(llm, log)
        self.python_tool = tool
        self.max_retries = max_retries

        self.code_schema = cleandoc("""
            {
                "arguments": {
                    "code": "A string containing valid Python code. Use \\n for newlines."
                }
            }
        """)

    def run(self, task: str) -> Result[PythonCodeOutput]:
        self.log.log("PythonAgent", "start", task=task)
        previous_error: str | None = None
        failed_code = ""
        last_result: PythonCodeOutput | None = None

        for attempt in range(self.max_retries + 1):
            if previous_error and failed_code:
                self.log.log(
                    "PythonAgent", "retry", attempt=attempt, error=previous_error
                )
                prompt = self.build_fix_prompt(task, failed_code, previous_error)
            else:
                prompt = self.build_prompt(task)

            parsed = self.guard.run_structured_inference(prompt, ToolCall)

            if not parsed:
                self.log.log(
                    "PythonAgent",
                    "failed",
                    reason="Failed to parse code execution request",
                )
                return Err("Failed to parse code execution request", stage="inference")

            code_attr = parsed.arguments.get("code")
            if not isinstance(code_attr, str):
                self.log.log(
                    "PythonAgent",
                    "failed",
                    reason="LLM returned non-string code attribute",
                )
                return Err("LLM returned non-string code attribute", stage="validation")

            try:
                input_data = self.python_tool.input_schema(code=code_attr)
                last_result = self.python_tool.execute(input_data)
            except Exception as e:
                previous_error = str(e)
                failed_code = code_attr
                continue

            if last_result.success:
                self.log.log("PythonAgent", "success", output=last_result.output)
                return Ok(last_result)

            previous_error = last_result.error
            failed_code = code_attr

        self.log.log("PythonAgent", "exhausted", attempts=self.max_retries + 1)
        if last_result is not None:
            return Err(
                f"Code execution failed after {self.max_retries + 1} attempts: {last_result.error}",
                stage="tool_execution",
            )
        return Err("Python tool failed after retries", stage="tool_execution")

    def _sandbox_constraints(self) -> str:
        return cleandoc("""
            ### SANDBOX CONSTRAINTS
            - Available libraries: Python standard library, numpy, pandas, scipy, sympy, matplotlib.
            - Do NOT use any other third-party packages.
            - Do NOT access the filesystem (no reading/writing files).
            - The code MUST include a print() statement for the final result.
        """)

    def build_fix_prompt(self, task: str, failed_code: str, error: str) -> str:
        output_constraints = self.json_output_instructions(
            self.code_schema, allow_code_in_value=True
        )
        sandbox = self._sandbox_constraints()
        return cleandoc(f"""
            Act as a Python Code Generator. The previous code failed. Analyze the error and fix it.

            ### ORIGINAL TASK
            {task}

            ### FAILED CODE
            {failed_code}

            ### ERROR MESSAGE
            {error}

            {sandbox}

            {output_constraints}
        """)

    def build_prompt(self, task: str) -> str:
        output_constraints = self.json_output_instructions(
            self.code_schema, allow_code_in_value=True
        )
        sandbox = self._sandbox_constraints()
        return cleandoc(f"""
            Act as a Python Code Generator.

            ### TASK
            Generate a Python script that executes the following task and prints the final result:
            {task}

            {sandbox}

            {output_constraints}
        """)
