"""Tool registry — single source of truth for tool specs and execution."""

from typing import Any, Callable, TypedDict

from agents.types import ToolSelection
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

    def execute(self, selection: ToolSelection) -> Any:
        """Execute a tool by routing to its registered handler.

        Args:
            selection: The tool selection containing tool_name and prompt

        Raises:
            ValueError: If no handler is registered for the tool
        """
        handler = self._handlers.get(selection.tool_name)
        if not handler:
            raise ValueError(f"No handler registered for tool '{selection.tool_name}'")
        return handler(selection.prompt)

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
