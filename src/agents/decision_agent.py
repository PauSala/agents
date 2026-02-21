from agents.base_agent import BaseAgent
from agents.decision_response import AgentDecision
from core.inference_guard import InvalidResponse
from inspect import cleandoc


class DecisionAgent(BaseAgent):
    def run(self, task: str) -> InvalidResponse | AgentDecision:
        prompt = self.build_prompt(task)
        parsed = self.guard.run_structured_inference(self.llm, prompt, AgentDecision)

        if parsed is None:
            return InvalidResponse(reason="Invalid JSON output after retries")

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
              Use when the task requires performing an action (APIs, FS, maths).

            - code:
              Use when asked to generate code.

            - fail:
              Use when the task is invalid.

            ----

            {output_constraints}
        """)
        
        return prompt