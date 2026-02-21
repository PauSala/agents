from agents.base_agent import BaseAgent, AgentRole
from core.llm_wrapper import LLM

llm = LLM()
agent = BaseAgent(AgentRole.ORQUESTRATOR, llm)

print(agent.run("Say hello"))