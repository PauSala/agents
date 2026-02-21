from agents.base_agent import BaseAgent
from core.llm_wrapper import LLM

llm = LLM()
agent = BaseAgent("tutor", llm)

print(agent.run("Say hello"))