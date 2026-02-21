"""Tool that executes Python code in a sandboxed subprocess with resource limits."""

import subprocess
import tempfile
import os
import sys
import resource
from typing import Optional

from pydantic import BaseModel

from tools.tool import Tool


class PythonCodeInput(BaseModel):
    code: str


class PythonCodeOutput(BaseModel):
    output: str
    error: Optional[str] = None
    success: bool = False


class PythonCodeTool(Tool[PythonCodeInput, PythonCodeOutput]):
    """Execute isolated Python code in a sandboxed subprocess. Required code not to be quoted"""

    name = "python"
    description = "Execute isolated Python code in a sandboxed subprocess"
    input_schema = PythonCodeInput

    MAX_CODE_LENGTH = 5000
    TIMEOUT_SECONDS = 3
    MEMORY_LIMIT_MB = 128
    CPU_TIME_LIMIT_SECONDS = 2

    def _limit_resources(self):
        """Apply resource limits (Unix only)."""
        # Limit CPU time
        try:
            if hasattr(resource, "RLIMIT_CPU"):
                resource.setrlimit(
                    resource.RLIMIT_CPU,
                    (self.CPU_TIME_LIMIT_SECONDS, self.CPU_TIME_LIMIT_SECONDS),
                )
        except Exception:
            # If setting RLIMIT_CPU fails, ignore to avoid crashing the child process
            pass

        # Limit memory usage (may not be supported on all platforms)
        try:
            if hasattr(resource, "RLIMIT_AS"):
                memory_bytes = self.MEMORY_LIMIT_MB * 1024 * 1024
                resource.setrlimit(
                    resource.RLIMIT_AS,
                    (memory_bytes, memory_bytes),
                )
        except Exception:
            # Ignore failures (some OSes disallow or don't support RLIMIT_AS)
            pass

    def execute(self, input_data: PythonCodeInput) -> PythonCodeOutput:
        code = input_data.code.strip()
        print(code)

        if len(code) > self.MAX_CODE_LENGTH:
            return PythonCodeOutput(output="", error="Code too long", success=False)

        tmp_filename = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp_file:
                tmp_file.write(code)
                tmp_filename = tmp_file.name

            process = subprocess.run(
                [sys.executable, tmp_filename],
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT_SECONDS,
                preexec_fn=self._limit_resources if os.name != "nt" else None,
            )

            stdout = process.stdout or ""
            stderr = process.stderr or ""
            success = process.returncode == 0

            return PythonCodeOutput(output=stdout.strip(), error=stderr.strip(), success=success)

        except subprocess.TimeoutExpired:
            return PythonCodeOutput(output="", error="Execution timed out", success=False)
        except Exception as e:
            return PythonCodeOutput(output="", error=f"Execution error: {e}", success=False)
        finally:
            if tmp_filename:
                try:
                    os.remove(tmp_filename)
                except Exception:
                    pass
