
from agents.base_agent import BaseAgent
from agents.types import ToolSelection
from core.inference_guard import InvalidResponse
from core.llm_wrapper import LLM
from tools.registry import ToolRegistry, ToolSpec


class ToolSelectionAgent(BaseAgent):
    """Agent that selects tools based on task description."""

    def __init__(self, llm: LLM):
        super().__init__(llm)
        self.registry = ToolRegistry()

    def run(self, task: str) -> InvalidResponse | ToolSelection:
        """Execute task by selecting and running appropriate tool."""
        prompt = self.build_prompt(task)
        parsed = self.guard.run_structured_inference(self.llm, prompt, ToolSelection)

        if parsed is None:
            return InvalidResponse(reason="Failed to parse tool selection")

        return parsed

    def build_prompt(self, task: str) -> str:
        """Build prompt with available tools and task description."""
        tools_info = self._format_tools_info()
        
        return f"""
Act as a precise Router Agent. Your sole purpose is to map a User Request to the correct Tool Name and provide a clean, high-level intent string.

### AVAILABLE TOOLS
{tools_info}

### USER REQUEST
{task}

### INSTRUCTIONS
1. **IDENTIFY**: Select the single most appropriate `tool_name` from the list above.
2. **STRIP**: Remove all implementation details, coding logic, variable names, and technical constraints from the request.
3. **RESTATE**: Provide a "prompt" that is a plain-language summary of the goal.

### OUTPUT FORMAT
Output ONLY a raw JSON object. No markdown blocks, no conversational text, and no quotes outside the JSON.

{{
    "tool_name": "exact_tool_id",
    "prompt": "Plain language summary of the objective"
}}

### STRICT NEGATIVE CONSTRAINTS
- NO code snippets or logic (e.g., no 'for loops', 'imports', or 'functions').
- NO formatting symbols or backticks.
- NO mentions of tool metadata or documentation.
- NO conversational filler.
"""
    def _format_tools_info(self) -> str:
        """Return minimal tool registry representation for prompt routing."""
    
        specs: list[ToolSpec] = self.registry.get_tool_specs()
    
        return "\n".join(
            f"- {spec['name']}: {spec.get('description', '')}"
            for spec in specs
        )