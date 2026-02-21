from agents.base_agent import BaseAgent
from agents.decision_response import AgentDecision
from core.inference_guard import InvalidResponse


class DecisionAgent(BaseAgent):
    def run(self, task: str) -> InvalidResponse | AgentDecision:
        prompt = self.build_prompt(task)
        parsed = self.guard.run_structured_inference(self.llm, prompt, AgentDecision)

        if parsed is None:
            return InvalidResponse(reason="Invalid JSON output after retries")

        return parsed
    
    def build_prompt(self, task: str) -> str:
        return f"""
You are a workflow decision classifier.

You must classify the given TASK into one of:
EXPLAIN | TOOL | CODE | FAIL.

TASK:
{task}

----

CLASSIFICATION RULES:

- EXPLAIN:
  Use when the task requires explanation, description, reasoning, or informational response only.
  No execution or code artifact is required.

- TOOL:
  Use when the task requires performing an action in the system
  (e.g., filesystem operations, external APIs, database access, calculations using a runtime tool).

- CODE:
  Use when the task requires generating source code as the final artifact
  (e.g., implementing an algorithm in a specific programming language).

- FAIL:
  Use when the task cannot be completed or is invalid.

----

STRICT OUTPUT RULES:
- Output ONLY parseable JSON.
- Output must always match this exact JSON schema:

{{
    "type": "explain | tool | code | fail",
    "reason": "mandatory explanation of why the task has been classified into the type"
}}

- Do not wrap JSON inside code fences.
- Do not output markdown.
- Do not output free text outside the JSON.
"""