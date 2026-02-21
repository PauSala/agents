from core.llm_wrapper import LLM
from core.inference_guard import InferenceGuard
from .agent_response import AgentDecision
from enum import Enum

class AgentRole(Enum):
    ORQUESTRATOR = "orquestrator"
    SUPERVISOR = "supervisor"
    EXECUTOR = "executor"



class BaseAgent:
    def __init__(self, role: AgentRole, llm: LLM, tools: dict[str, object] | None = None):
        self.role = role
        self.llm = llm
        self.tools = tools or {}
        self.guard = InferenceGuard()


    def run(self, task: str):
        prompt = self.build_prompt(task)
        parsed = self.guard.generate_and_validate(self.llm, prompt, AgentDecision)

        if parsed is None:
            return {
                "type": "fail",
                "reason": "Invalid JSON output after retries"
            }

        return parsed.model_dump()
    
    def build_prompt(self, task: str) -> str:
        return f"""
You are an autonomous workflow agent.

ROLE:
{self.role}

TASK:
{task}

---

STRICT OUTPUT RULES:

1. You MUST respond in valid JSON format.
2. Output must follow this schema:

{{
    "type": "final | tool | fail",
    "content": "response text if final",
    "tool": {{
        "name": "tool_name",
        "args": {{}}
    }},
    "reason": "optional explanation"
}}

If you cannot complete the task, return type="fail".

Do not output markdown.
Do not output commentary outside JSON.

Task:
{task}
"""