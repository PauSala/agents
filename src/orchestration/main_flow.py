from agents.decision_agent import DecisionAgent
from agents.decision_response import DecisionType
from agents.python_agent import PythonAgent
from agents.tool_selection_agent import ToolSelectionAgent
from core.llm_wrapper import LLM
from core.log_collector import LogCollector
from tools.python_tool import PythonCodeTool
from tools.registry import ToolRegistry

fast_llm = LLM(model="deepseek-coder:6.7b")
strong_llm = LLM(model="qwen2.5-coder:14b")
log = LogCollector()


registry = ToolRegistry()
python_tool = PythonCodeTool()
python_agent = PythonAgent(strong_llm, tool=python_tool, log=log)
registry.register(python_tool, handler=python_agent.run)

agent = DecisionAgent(fast_llm, log=log)
tool_agent = ToolSelectionAgent(strong_llm, registry=registry, log=log)


def run(prompt: str):
    decision = agent.run(prompt)

    if not decision.ok or decision.value is None:
        print(f"Decision failed: {decision.error}")
    elif decision.value.type == DecisionType.TOOL:
        selection = tool_agent.run(prompt)

        if not selection.ok or selection.value is None:
            print(f"Tool selection failed: {selection.error}")
        else:
            response = registry.execute(
                selection.value.tool_name, selection.value.prompt
            )

            if not response.ok:
                print(f"Tool execution failed: {response.error}")
            else:
                print(response.value)
    else:
        print("Non-tool task — not yet implemented")

    print("\n--- Agent Log ---")
    print(log.summary())
