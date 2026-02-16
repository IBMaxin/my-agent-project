# my-agent-project

A local AI agent using Hugging Face smolagents with llama.cpp for code generation and file operations.

## Project Goals

1. Develop a robust and scalable system.
2. Improve user experience through intuitive design.
3. Ensure high performance and reliability under load.

## What This Does

This project runs a CodeAgent that can:
- Create and edit files using `write_text`
- Read and verify files using `read_text`
- Execute shell commands with human approval using `run_shell`
- Perform calculations using `calculator`

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- llama.cpp server running at `http://127.0.0.1:8080`

### Install

```bash
uv venv
uv pip install "smolagents[toolkit]"
```

### Run

```bash
uv run python run_agent.py
```

## Project Structure

```
my-agent-project/
├── run_agent.py      # Main agent script
├── tools_local.py    # Custom tools (write_text, read_text, run_shell)
├── docs/
│   ├── setup.md      # Detailed setup guide
│   └── tools.md      # Tools reference
└── README.md
```

## Tools (4 Total)

| Tool | Purpose |
|------|---------|
| `write_text` | Create/edit files |
| `read_text` | Inspect files |
| `run_shell` | Run commands with human approval |
| `calculator` | Simple math |

### run_shell Safety

Two-layer safety system:
1. **Denylist**: Blocks `rm`, `rmdir`, `sudo`, `su`, `chmod`, `chown`
2. **Human approval gate**: Every command requires user approval

## Configuration

### Model Settings (Optimized for 4B)

```python
model = OpenAIServerModel(
    model_id="Qwen3-4B-Instruct-2507-Q4_K_M.gguf",
    api_base="http://127.0.0.1:8080/v1",
    api_key="local",
    temperature=0.1,  # Low temperature for reliability
)
```

### Why temperature=0.1?

- 4B models are prone to hallucination at higher temperatures
- Low temperature (0.0-0.3) produces deterministic outputs
- Essential for code generation tasks

## About smolagents

[smolagents](https://github.com/huggingface/smolagents) is a lightweight agent library from Hugging Face. Key concepts:

### CodeAgent

The agent executes Python code to solve tasks. It:
1. Receives a prompt
2. Plans which tools to use
3. Writes and executes Python code
4. Returns the result

### Tools

Tools are Python functions decorated with `@tool`. The model uses docstrings to understand what each tool does:

```python
@tool
def write_text(path: str, content: str) -> str:
    """Write UTF-8 text to a file.
    
    Args:
        path: The file path to write to.
        content: The text content to write.
    
    Returns:
        A confirmation message.
    """
    # Implementation
```

### Tool Best Practices

1. **Keep tools minimal** - 3-6 tools for small models
2. **Clear docstrings** - Model relies on these
3. **Return strings** - Easier for model to process
4. **Handle errors gracefully** - Return error messages

## Documentation

- [Setup Guide](docs/setup.md) - Detailed installation and troubleshooting
- [Tools Reference](docs/tools.md) - Complete tool documentation

## License

MIT
