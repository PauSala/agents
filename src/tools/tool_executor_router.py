from typing import Any

from agents.python_agent import PythonAgent
from agents.types import ToolSelection


class ToolExecutorRouter:
    def __init__(self, python_agent: PythonAgent):
        self.handlers = {
            "python": python_agent.run,
        }

    def run(self, selection: ToolSelection) -> Any:
        handler = self.handlers.get(selection.tool_name)
        
        if not handler:
            raise ValueError(f"No executor implemented for tool '{selection.tool_name}'")

        return handler(selection.prompt)