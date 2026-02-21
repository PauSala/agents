from agents.decision_agent import DecisionAgent
from agents.decision_response import AgentDecision, DecisionType
from agents.python_agent import PythonAgent
from agents.tool_selection_agent import ToolSelectionAgent
from agents.types import ToolSelection
from core.llm_wrapper import LLM
from tools.python_tool import PythonCodeTool
from tools.registry import ToolRegistry

llm = LLM()

# Build the registry — single source of truth for tools
registry = ToolRegistry()
python_agent = PythonAgent(llm)
registry.register(PythonCodeTool(), handler=python_agent.run)

agent = DecisionAgent(llm)
tool_agent = ToolSelectionAgent(llm, registry=registry)

prompt = "Give me a list of 30 numbers alternating negative and positives, starting from 0"

# Step 1 — Intent classification
decision = agent.run(prompt)

if isinstance(decision, AgentDecision) and decision.type == DecisionType.TOOL:
    tool_selection = tool_agent.run(prompt)

    if isinstance(tool_selection, ToolSelection):
        response = registry.execute(tool_selection)
        print(response)
    else:
        print("Tool routing failed")

else:
    print("Non-tool task or invalid decision")
