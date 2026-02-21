from typing import Any

from agents.python_agent import PythonAgent
from agents.types import ToolSelection
from tools.registry import ToolRegistry


class ToolExecutorRouter:
    def __init__(self, python_agent: PythonAgent):
        self.registry = ToolRegistry()
        self.python_agent = python_agent

    def run(self, selection: ToolSelection) -> Any:
        tool_name = selection.tool_name

        tool = self.registry.get(tool_name)
        if tool is None:
            raise ValueError(f"Tool '{tool_name}' not found")

        # Currently only PythonAgent exists
        if tool_name == "python":
            return self.python_agent.run(selection.prompt)

        raise ValueError(f"No executor implemented for tool '{tool_name}'")