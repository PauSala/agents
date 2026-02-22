from inspect import cleandoc

from agents.base_agent import BaseAgent
from agents.decision_response import AgentDecision
from core.types import Err, Ok, Result


class DecisionAgent(BaseAgent[AgentDecision]):
    def run(self, task: str) -> Result[AgentDecision]:
        self.log.log("DecisionAgent", "start", task=task)
        prompt = self.build_prompt(task)
        parsed = self.guard.run_structured_inference(prompt, AgentDecision)

        if parsed is None:
            self.log.log(
                "DecisionAgent", "failed", reason="Invalid JSON output after retries"
            )
            return Err("Invalid JSON output after retries", stage="inference")

        self.log.log(
            "DecisionAgent", "decision", type=parsed.type.value, reason=parsed.reason
        )
        return Ok(parsed)

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
            Classify the TASK into exactly one of: explain | tool | code | fail.

            ### CLASSIFICATION RULES (read these BEFORE looking at the task):

            - tool:
              The task requires executing an action to produce a result: computation, math,
              file operations, API calls, data processing, or anything that needs running code.
              When in doubt between "tool" and "code", choose "tool".

            - code:
              The user explicitly asks you to write or generate source code as the deliverable
              (e.g. "write a function that…", "give me a class for…").

            - explain:
              The task only requires explanation, reasoning, or knowledge — no execution needed.

            - fail:
              The task is nonsensical, empty, or fundamentally impossible to act on.

            ### EXAMPLES
            Task: "Solve x^2 + 3x + 1 = 0" → {{"type": "tool", "reason": "Requires computation to find the roots"}}
            Task: "Write a Python function to sort a list" → {{"type": "code", "reason": "User asks to generate source code"}}
            Task: "What is the capital of France?" → {{"type": "explain", "reason": "Factual question requiring only explanation"}}
            Task: "asdfghjkl" → {{"type": "fail", "reason": "Nonsensical input, cannot determine intent"}}

            ----

            ### TASK (classify this):
            {task}

            ----

            {output_constraints}
        """)

        return prompt
