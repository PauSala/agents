# Multi-Agent Framework — Roadmap Index

## 0. Setup
- Install local/free LLM
- Create LLM wrapper
- Test prompt → response

## 1. Core Agent
- Agent class (role, tools)
- Structured JSON output
- Output validation

## 2. Tool System (Skills)
- Define tool functions
- Tool registry
- Safe execution layer

## 3. Orchestrator
- Execution loop
- Task handling
- Termination conditions
- Logging

## 4. Multi-Agent Architecture
- Planner agent
- Worker agent
- Task board (TODO / DOING / DONE / FAILED)

## 5. Reflection / Reviewer
- Review agent
- Feedback loop
- Iteration limit

## 6. Shared Memory
- Memory class
- Store tasks
- Store tool outputs
- Context management

## 7. Robustness
- JSON schema validation
- Retry logic
- Loop detection
- Step limits
- Error handling

## 8. Project Structure
- agents/
- tools/
- core/
- config/
- logs/
- main.py
