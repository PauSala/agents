"""Tool that executes Python code in a Docker sandbox."""

import os
import subprocess
import tempfile
from typing import Optional

from pydantic import BaseModel

from tools.tool import Tool

SANDBOX_IMAGE = "agents-sandbox"


class PythonCodeInput(BaseModel):
    code: str


class PythonCodeOutput(BaseModel):
    output: str
    error: Optional[str] = None
    success: bool = False


class PythonCodeTool(Tool[PythonCodeInput, PythonCodeOutput]):
    """Execute Python code in an isolated Docker container."""

    name = "python"
    description = "Execute isolated Python code in a sandboxed Docker container."
    input_schema = PythonCodeInput

    MAX_CODE_LENGTH = 5000
    MAX_OUTPUT_BYTES = 64 * 1024  # 64KB
    TIMEOUT_SECONDS = 10
    MEMORY_LIMIT_MB = 128

    def execute(self, input_data: PythonCodeInput) -> PythonCodeOutput:
        code = input_data.code.strip()

        if len(code) > self.MAX_CODE_LENGTH:
            return PythonCodeOutput(output="", error="Code too long", success=False)

        tmp_filename = None
        process: subprocess.Popen[str] | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False
            ) as tmp_file:
                tmp_file.write(code)
                tmp_filename = tmp_file.name

            # Make readable by Docker's sandbox user (uid 1000)
            os.chmod(tmp_filename, 0o644)

            process = subprocess.Popen(
                [
                    "docker",
                    "run",
                    "--rm",
                    "--network",
                    "none",
                    "--read-only",
                    "--cap-drop=ALL",
                    "--security-opt=no-new-privileges",
                    "--tmpfs",
                    "/tmp:size=16m",
                    f"--memory={self.MEMORY_LIMIT_MB}m",
                    "--cpus=1",
                    "--pids-limit=32",
                    "-v",
                    f"{tmp_filename}:/sandbox/script.py:ro",
                    SANDBOX_IMAGE,
                    "python",
                    "/sandbox/script.py",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout, stderr = process.communicate(timeout=self.TIMEOUT_SECONDS)

            # Truncate to prevent host memory exhaustion
            stdout = (stdout or "")[: self.MAX_OUTPUT_BYTES]
            stderr = (stderr or "")[: self.MAX_OUTPUT_BYTES]
            success = process.returncode == 0

            return PythonCodeOutput(
                output=stdout.strip(), error=stderr.strip(), success=success
            )

        except subprocess.TimeoutExpired:
            if process:
                process.kill()
                process.wait()
            return PythonCodeOutput(
                output="", error="Execution timed out", success=False
            )
        except Exception as e:
            return PythonCodeOutput(
                output="", error=f"Execution error: {e}", success=False
            )
        finally:
            if tmp_filename:
                try:
                    os.remove(tmp_filename)
                except Exception:
                    pass
