"""Tool registry for managing and executing tools."""

from typing import Optional, Any, TypedDict

from tools.tool import Tool
from tools.python_tool import PythonCodeTool


class ToolSpec(TypedDict):
    """Specification of a tool."""
    name: str
    description: str
    input_schema: dict[str, Any]


class ToolRegistry:
    """Registry to manage tools and execute them by name."""

    def __init__(self):
        self._tools: dict[str, Tool[Any, Any]] = {
            "python": PythonCodeTool(),
        }

    def get(self, name: str) -> Optional[Tool[Any, Any]]:
        """Get a tool by name.

        Args:
            name: The tool name

        Returns:
            The Tool instance or None if not found
        """
        return self._tools.get(name)

    def execute(self, name: str, **kwargs: Any) -> Any:
        """Execute a tool by name.

        Args:
            name: The tool name
            **kwargs: Arguments to pass to the tool (must match tool's input type)

        Returns:
            The tool's output

        Raises:
            ValueError: If the tool is not found
        """
        tool = self.get(name)
        if tool is None:
            raise ValueError(f"Tool '{name}' not found")
        # Instantiate the input schema from kwargs
        input_instance = tool.input_schema(**kwargs)
        return tool.execute(input_instance)

    def list_tools(self) -> list[str]:
        """Get list of all registered tool names."""
        return list(self._tools.keys())

    def get_tool_specs(self) -> list[ToolSpec]:
        """Get specifications of all tools for LLM prompt.

        Returns:
            List of tool specs with name, description, and input schema
        """
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
