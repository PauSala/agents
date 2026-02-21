"""Math tool for executing Python math expressions."""

import math
from typing import Any

from pydantic import BaseModel

from tools.tool import Tool


class MathInput(BaseModel):
    expression: str


class MathOutput(BaseModel):
    result: str


class MathTool(Tool[MathInput, MathOutput]):
    """Math tool that executes Python math expressions in a restricted namespace."""

    name = "math"
    description = "Execute Python math expressions and return the result"
    input_schema = MathInput

    def execute(self, input_data: MathInput) -> MathOutput:
        """Execute math expression."""
        try:
            # Create a safe namespace with math functions and a few safe builtins
            namespace: dict[str, Any] = {
                "math": math,
                "str": str,
                "int": int,
                "float": float,
                "abs": abs,
                "round": round,
                "max": max,
                "min": min,
                "__builtins__": {},
                **{name: getattr(math, name) for name in dir(math) if not name.startswith("_")},
            }
            result = eval(input_data.expression, namespace)
            return MathOutput(result=str(result))
        except Exception as e:
            return MathOutput(result=f"Error: {e}")
