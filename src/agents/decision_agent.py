from agents.base_agent import BaseAgent
from agents.decision_response import AgentDecision
from core.inference_guard import InvalidResponse
from inspect import cleandoc


class DecisionAgent(BaseAgent[AgentDecision]):
    def run(self, task: str) -> AgentDecision | InvalidResponse:
        self.log.log("DecisionAgent", "start", task=task)
        prompt = self.build_prompt(task)
        parsed = self.guard.run_structured_inference(prompt, AgentDecision)

        if parsed is None:
            self.log.log("DecisionAgent", "failed", reason="Invalid JSON output after retries")
            return InvalidResponse(reason="Invalid JSON output after retries")

        self.log.log("DecisionAgent", "decision", type=parsed.type.value, reason=parsed.reason)
        return parsed
    

    def build_prompt(self, task: str) -> str:
        schema = cleandoc("""
            {
                "type": "explain | tool | code | fail",
                "reason": "mandatory explanation of why the task has been classified into the type"
            }
        """)

        output_constraints = self.json_output_instructions(schema)
        prompt = cleandoc(f"""
            You are a workflow decision classifier.

            You must classify the given TASK into one of:
            explain | tool | code | fail.

            TASK:
            {task}

            ----

            ### CLASSIFICATION RULES:

            - explain:
              Use when the task requires explanation or reasoning.
            
            - tool:
              Use when the task requires performing an action that could require a tool (APIs, FS, Math).

            - code:
              Use when asked to generate code.

            - fail:
              Use only when the task is impossible to be resolved by a tool.

            ----

            {output_constraints}
        """)
        
        return prompt