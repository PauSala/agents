from typing import Any, Optional

from pydantic import BaseModel

from agents.base_agent import BaseAgent
from core.inference_guard import InvalidResponse
from core.llm_wrapper import LLM
from tools.registry import ToolRegistry, ToolSpec


class ToolCall(BaseModel):
    """Schema for tool execution."""
    tool_name: str
    arguments: dict[str, Any]


class ToolAgent(BaseAgent):
    """Agent that selects and executes tools based on task description."""

    def __init__(self, llm: LLM, tools: Optional[dict[str, object]] = None):
        super().__init__(llm, tools)
        self.registry = ToolRegistry()

    def run(self, task: str) -> InvalidResponse | dict[str, Any]:
        """Execute task by selecting and running appropriate tool."""
        prompt = self.build_prompt(task)
        parsed = self.guard.run_structured_inference(self.llm, prompt, ToolCall)

        if parsed is None:
            return InvalidResponse(reason="Failed to parse tool selection").model_dump()

        try:
            result = self.registry.execute(parsed.tool_name, **parsed.arguments)
            return result.model_dump() if hasattr(result, "model_dump") else result
        except Exception as e:
            return InvalidResponse(reason=f"Tool execution failed: {e}").model_dump()

    def build_prompt(self, task: str) -> str:
        """Build prompt with available tools and task description."""
        tools_info = self._format_tools_info()
        
        return f"""
You are a tool execution agent. Your task is to select the appropriate tool and call it with the correct arguments.

AVAILABLE TOOLS:
{tools_info}

TASK:
{task}

----

INSTRUCTIONS:
1. Analyze the task and identify which tool to use
2. Determine the arguments required by that tool
3. Output ONLY valid JSON in this exact format:

{{
    "tool_name": "name_of_the_tool",
    "arguments": {{"argument_name": "argument_value"}}
}}

RULES:
- Never output markdown or free text outside JSON
- tool_name must be one of the available tools above
- arguments must be a valid dict matching the tool's input requirements
- Always wrap string values in quotes
"""

    def _format_tools_info(self) -> str:
        """Format available tools with their input schemas for the prompt."""
        specs: list[ToolSpec] = self.registry.get_tool_specs()
        tools_text: list[str] = []
        for spec in specs:
            schema = spec["input_schema"]
            properties = schema.get("properties", {})
            required = schema.get("required", [])
            
            args_desc: list[str] = []
            for arg_name, arg_info in properties.items():
                arg_type = arg_info.get("type", "string")
                arg_desc = arg_info.get("description", "")
                required_marker = "(required)" if arg_name in required else "(optional)"
                args_desc.append(f"    - {arg_name} ({arg_type}) {required_marker}: {arg_desc}")
            
            args_block = "\n".join(args_desc) if args_desc else "    (no arguments)"
            tools_text.append(f"- {spec['name']}: {spec['description']}\n  Arguments:\n{args_block}")
        return "\n\n".join(tools_text)