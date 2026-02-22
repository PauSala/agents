"""Tool registry — single source of truth for tool specs and execution."""

from typing import Any, Callable, TypedDict

from core.types import Err, Result
from tools.tool import Tool


class ToolSpec(TypedDict):
    """Specification of a tool."""
    name: str
    description: str
    input_schema: dict[str, Any]


class ToolRegistry:
    """Registry to manage tools and route execution by name."""

    def __init__(self):
        self._tools: dict[str, Tool[Any, Any]] = {}
        self._handlers: dict[str, Callable[[str], Any]] = {}

    def register(self, tool: Tool[Any, Any], handler: Callable[[str], Any]) -> None:
        """Register a tool and its execution handler.

        Args:
            tool: The Tool instance (provides name, description, schema for prompts)
            handler: Callable that receives a prompt string and returns a result
        """
        self._tools[tool.name] = tool
        self._handlers[tool.name] = handler

    def get_tool(self, name: str) -> Tool[Any, Any] | None:
        """Get a tool instance by name."""
        return self._tools.get(name)

    def execute(self, tool_name: str, prompt: str) -> Result[Any]:
        """Execute a tool by routing to its registered handler."""
        handler = self._handlers.get(tool_name)
        if not handler:
            return Err(f"No handler registered for tool '{tool_name}'", stage="routing")
        return handler(prompt)

    def list_tools(self) -> list[str]:
        """Get list of all registered tool names."""
        return list(self._tools.keys())

    def get_tool_specs(self) -> list[ToolSpec]:
        """Get specifications of all tools for LLM prompt."""
        specs: list[ToolSpec] = []
        for tool in self._tools.values():
            specs.append(
                ToolSpec(
                    name=tool.name,
                    description=tool.description,
                    input_schema=tool.input_schema.model_json_schema(),
                )
            )
        return specs
