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
