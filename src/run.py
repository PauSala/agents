from core.events import NoOpEmitter
from orchestration import Director

prompt = "Can you resolve x^2 + 3x + 1 = 0?"
director = Director(emitter=NoOpEmitter())
director.run(prompt=prompt)
