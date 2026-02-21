from agents.decision_agent import DecisionAgent
from core.llm_wrapper import LLM

llm = LLM()
agent = DecisionAgent(llm)

print(agent.run("Can you implement quick sort in java?"))