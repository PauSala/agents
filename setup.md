# Steps

## Ollama

Ollama is an LLM manager. You can download/train/serve models with it. 

- Get ollama: curl -fsSL https://ollama.com/install.sh | sh
- Get a model: ollama pull deepseek-coder:6.7b
- Run a model: ollama run deepseek-coder:6.7b
- Send a promt: 
    ``` bash
    curl http://localhost:11434/api/generate -d '{
      "model": "deepseek-coder:6.7b",
      "prompt": "Say hello",
      "stream": false
    }'
    ```
- List models: ollama list
- Models are stored in: ~/.ollama/models

## Docker Sandbox

The Python tool runs LLM-generated code inside a Docker container for isolation.

- Build the sandbox image (one-time): `docker build -f Dockerfile.sandbox -t agents-sandbox .`
- The container runs with: no network, read-only filesystem, 128MB memory limit, PID limit


## Server
export PYTHONPATH=$PYTHONPATH:$(pwd)/src && python3 -m server.server 