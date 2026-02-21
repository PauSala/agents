from agents.decision_agent import DecisionAgent
from agents.decision_response import AgentDecision, DecisionType
from agents.tool_selection_agent import ToolSelectionAgent
from core.llm_wrapper import LLM

llm = LLM()
agent = DecisionAgent(llm)
tool_agent = ToolSelectionAgent(llm)

prompt = "Calculate the first 50 primes from 3000-5000"
response= agent.run(prompt)
print(response, isinstance(response, AgentDecision))
if isinstance(response, AgentDecision) and response.type == DecisionType.TOOL:
    print(tool_agent.run(prompt))
