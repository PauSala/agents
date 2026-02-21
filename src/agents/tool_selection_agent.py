
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
You are a tool execution agent. Your task is to select the appropriate tool to execute the task.

AVAILABLE TOOLS:
{tools_info}

TASK:
{task}

----


INSTRUCTIONS:

1. Select exactly ONE tool_name from the list above.

2. Create a compressed version of the TASK.

Compression rules:
- Remove explanations.
- Remove tool documentation.
- Remove formatting artifacts.
- Do NOT generate executable code.
- Do NOT include code snippets.
- Do NOT include program logic.
- Keep only the minimal description of the task.

Output ONLY JSON.

{{
    "tool_name": "the tool to use",
    "prompt": "TASK"
}}


STRICT FORBIDDEN CONTENT:
- Python code
- Shell commands
- Programming logic
- Tool metadata
- Documentation fragments
- Markdown formatting
- Quotes outside JSON
"""
    def _format_tools_info(self) -> str:
        """Return minimal tool registry representation for prompt routing."""
    
        specs: list[ToolSpec] = self.registry.get_tool_specs()
    
        return "\n".join(
            f"- {spec['name']}: {spec.get('description', '')}"
            for spec in specs
        )