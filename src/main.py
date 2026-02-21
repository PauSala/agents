from agents.decision_agent import DecisionAgent
from agents.decision_response import AgentDecision, DecisionType
from agents.python_agent import PythonAgent
from agents.tool_selection_agent import ToolSelectionAgent
from agents.types import ToolSelection
from core.llm_wrapper import LLM
from tools.tool_executor_router import ToolExecutorRouter

llm = LLM()
agent = DecisionAgent(llm)
tool_agent = ToolSelectionAgent(llm)
python_agent = PythonAgent(llm)
execution_router = ToolExecutorRouter(python_agent=python_agent)

prompt = "Can you sum log(x) from 0 to 100?"

# Step 1 — Intent classification
decision = agent.run(prompt)

if isinstance(decision, AgentDecision) and decision.type == DecisionType.TOOL:
    tool_selection = tool_agent.run(prompt)

    if isinstance(tool_selection, ToolSelection):
        response = execution_router.run(tool_selection)

        print(response)

    else:
        print("Tool routing failed")

else:
    print("Non-tool task or invalid decision")