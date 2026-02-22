from uuid import uuid4

from agents.decision_agent import DecisionAgent
from agents.decision_response import DecisionType
from agents.python_agent import PythonAgent
from agents.tool_selection_agent import ToolSelectionAgent
from core.types import AgentStatus, EventEmitter
from core.llm_wrapper import LLM
from core.log_collector import LogCollector
from tools.python_tool import PythonCodeTool
from tools.registry import ToolRegistry


class Director:
    def __init__(self, emitter: EventEmitter):
        self.name = type(self).__name__
        self.agent_id = uuid4().hex

        # Core infrastructure
        self.log = LogCollector(emitter)

        # LLMs
        self.fast_llm = LLM(model="deepseek-coder:6.7b")
        self.strong_llm = LLM(model="qwen2.5-coder:14b")

        # Tool registry
        self.registry = ToolRegistry()

        # Tools + agents
        self.python_tool = PythonCodeTool()
        self.python_agent = PythonAgent(
            llm=self.strong_llm,
            tool=self.python_tool,
            log=self.log,
        )

        self.registry.register(
            self.python_tool,
            handler=self.python_agent.run,
        )

        self.decision_agent = DecisionAgent(
            llm=self.fast_llm,
            log=self.log,
        )

        self.tool_selection_agent = ToolSelectionAgent(
            llm=self.strong_llm,
            registry=self.registry,
            log=self.log,
        )

    def run(self, prompt: str) -> None:
        self.log.log(self.name, AgentStatus.RUNNING.value, agent_id=self.agent_id, task=prompt)
        decision = self.decision_agent.run(prompt, caller_id=self.agent_id)

        if not decision.ok or decision.value is None:
            print(f"Decision failed: {decision.error}")
            self.log.log(self.name, AgentStatus.END.value, agent_id=self.agent_id)
            return

        if decision.value.type == DecisionType.TOOL:
            selection = self.tool_selection_agent.run(prompt, caller_id=self.agent_id)

            if not selection.ok or selection.value is None:
                print(f"Tool selection failed: {selection.error}")
                self.log.log(self.name, AgentStatus.END.value, agent_id=self.agent_id)
                return

            response = self.registry.execute(
                selection.value.tool_name,
                selection.value.prompt,
                caller_id=self.agent_id,
            )

            if not response.ok:
                print(f"Tool execution failed: {response.error}")
            else:
                print(response.value)

        else:
            print("Non-tool task — not yet implemented")

        self.log.log(self.name, AgentStatus.END.value, agent_id=self.agent_id)
        print("\n--- Agent Log ---")
        print(self.log.summary())
