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

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager (or pip)
- llama.cpp server running at `http://127.0.0.1:8080`

### Install

```bash
# Clone and enter the project
cd my-agent-project

# Install dependencies
uv pip install -e .
# OR
pip install -r requirements.txt

# Create your .env file
cp .env.example .env
# Edit .env if needed (optional)
```

### Run

**Interactive Mode (Recommended)**
```bash
python -m src.cli
```

This launches an interactive REPL with commands:
- `/help` - Show available commands
- `/config` - Display current configuration
- `/clear` - Clear conversation history
- `/exit` or `/quit` - Exit the program

**Single-Prompt Mode**
```bash
python -m src.cli "Create a test.txt file with hello world"
```

**Legacy Mode**
```bash
python run_agent.py  # Still works for backward compatibility
```

## Project Structure

```
my-agent-project/
├── src/
│   ├── cli.py         # Interactive CLI (NEW)
│   ├── agent.py       # Agent initialization
│   ├── config.py      # Configuration management
│   └── logger.py      # Structured logging
├── tools_local.py     # Custom tools
├── run_agent.py       # Legacy script
├── .env.example       # Configuration template
├── docs/
│   ├── setup.md       # Detailed setup guide
│   └── tools.md       # Tools reference
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

All settings are configured via `.env` file (see `.env.example`):

```bash
# LLM Configuration
MODEL_ID=Qwen3-4B-Instruct-2507-Q4_K_M.gguf
API_BASE=http://127.0.0.1:8080/v1
TEMPERATURE=0.1

# Agent Configuration
STREAM_OUTPUTS=true
MAX_STEPS=10

# Logging
LOG_LEVEL=INFO
LOG_FILE=agent.log
```

View current config with `/config` command in the CLI.

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

## Troubleshooting

### Model Interpretation Quirks

**Print Output Confusion**: Smaller models (like Qwen3-4B) sometimes misinterpret Python's `print()` return value:

```python
content = read_text("file.txt")  # Returns "Hello World"
print(content)                    # Prints "Hello World", returns None
# Model sees: Out: None
```

The model may conclude the file is empty when it sees `Out: None`, even though the **execution logs** show the correct content was printed. This is a model interpretation issue, not a tool failure.

**Solution**: Check the **Execution logs** section in the output, not just the `Out:` line. The tools work correctly; the model is just confused by Python semantics.

### Best Prompts for Small Models

Small models (4B) work best with task-based prompts rather than conversational ones:

✅ **Good prompts**:
- "Create a file called test.txt with 'Hello World'"
- "Calculate 25 multiplied by 4"
- "Read the contents of README.md"
- "List files using run_shell: ls -la"

❌ **Problematic prompts**:
- "Hello" (too vague)
- "What can you do?" (conversational)
- "What tools do you have?" (meta-question)

### Model Recommendations

For best results with CodeAgent:
- **4B models**: Works but occasional confusion (Qwen3-4B)
- **7B+ models**: Recommended for better reliability (Qwen2.5-Coder-7B, Mistral-7B)
- **Coder models**: Specifically trained for code tasks (CodeQwen, Qwen2.5-Coder)

### Connection Issues

If you see connection errors:
```bash
# Verify llama.cpp is running
curl http://127.0.0.1:8080/v1/models

# Check your .env file
cat .env | grep API_BASE
```

## Documentation

- [Setup Guide](docs/setup.md) - Detailed installation and troubleshooting
- [Tools Reference](docs/tools.md) - Complete tool documentation

## License

MIT
