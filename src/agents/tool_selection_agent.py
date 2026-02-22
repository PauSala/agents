from inspect import cleandoc

from agents.base_agent import BaseAgent
from agents.types import ToolSelection
from core.llm_wrapper import LLM
from core.log_collector import LogCollector
from core.types import Err, Ok, Result
from tools.registry import ToolRegistry, ToolSpec


class ToolSelectionAgent(BaseAgent[ToolSelection]):
    """Agent that selects tools based on task description."""

    def __init__(self, llm: LLM, registry: ToolRegistry, log: LogCollector | None = None):
        super().__init__(llm, log)
        self.registry = registry

    def run(self, task: str) -> Result[ToolSelection]:
        """Execute task by selecting and running appropriate tool."""
        self.log.log("ToolSelectionAgent", "start", task=task)
        prompt = self.build_prompt(task)
        parsed = self.guard.run_structured_inference(prompt, ToolSelection)

        if parsed is None:
            self.log.log("ToolSelectionAgent", "failed", reason="Failed to parse tool selection")
            return Err("Failed to parse tool selection", stage="inference")

        self.log.log("ToolSelectionAgent", "selected", tool=parsed.tool_name, prompt=parsed.prompt)
        return Ok(parsed)

    def build_prompt(self, task: str) -> str:
        """Build prompt with available tools and task description."""
        tools_info = self._format_tools_info()
        schema = cleandoc("""
            {
                "tool_name": "exact_tool_id",
                "prompt": "Plain language summary of the objective"
            }
        """)
        output_constraints = self.json_output_instructions(schema)
        
        return cleandoc(f"""
            Act as a precise Router Agent. Your sole purpose is to map a User Request to the correct Tool Name and provide a clean, high-level intent string.
    
            ### AVAILABLE TOOLS
            {tools_info}
    
            ### USER REQUEST
            {task}
    
            ### INSTRUCTIONS
            1. **IDENTIFY**: Select the single most appropriate `tool_name` from the list above.
            2. **STRIP**: Remove all implementation details, coding logic, variable names, and technical constraints from the request.
            3. **RESTATE**: Provide a "prompt" that is a plain-language summary of the goal.
    
            {output_constraints}
        """)
    
    def _format_tools_info(self) -> str:
        """Return minimal tool registry representation for prompt routing."""
    
        specs: list[ToolSpec] = self.registry.get_tool_specs()
    
        return "\n".join(
            f"- {spec['name']}: {spec.get('description', '')}"
            for spec in specs
        )
