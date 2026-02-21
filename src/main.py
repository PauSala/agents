from agents.decision_agent import DecisionAgent
from agents.tool_agent import ToolAgent
from core.llm_wrapper import LLM

llm = LLM()
agent = DecisionAgent(llm)
tool_agent = ToolAgent(llm)

# print(agent.run("Can you sum sqrt(7) + log(2)?"))
print(tool_agent.run("Can give me a list of 4 primes?"))