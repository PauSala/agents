from agents.base_agent import BaseAgent
from agents.decision_response import AgentDecision


class DecisionAgent(BaseAgent):
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
You are a workflow decision classifier, you must classify the given TASK into EXPLAIN | TOOL | CODE | FAIL.

TASK:
{task}

----

STRICT OUTPUT RULES:
- You must output ONLY valid JSON:
- Your output allways matches this schema:
{{
    "type": "explain | tool | code | fail",
    "tool": {{
        "name": "tool_name",
        "args": {{}}
    }},
    "reason": "mandatory explanation of why the task has been classified into the type"
}}
- Never quote the json
- You must not output markdown nor free text

"""