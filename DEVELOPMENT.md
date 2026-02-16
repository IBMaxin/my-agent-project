# Development Guide

A comprehensive guide for contributing to and developing the my-agent-project.

## Table of Contents

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Code Style](#code-style)
- [Git Workflow](#git-workflow)
- [Writing Tools](#writing-tools)
- [Testing](#testing)
- [Configuration](#configuration)
- [Security](#security)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- llama.cpp server running locally
- VS Code or Cursor IDE

### Initial Setup

```bash
# Clone the repository
cd ~/projects
git clone https://github.com/IBMaxin/my-agent-project.git
cd my-agent-project

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
# OR
uv pip install -e .

# Copy environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

### Verify Installation

```bash
# Test the CLI
python -m src.cli

# Should see welcome message
# Type /exit to quit
```

---

## Project Structure

```
my-agent-project/
├── src/                    # Main package
│   ├── __init__.py
│   ├── agent.py           # Agent initialization
│   ├── cli.py             # Interactive CLI
│   ├── config.py          # Configuration management
│   └── logger.py          # Logging setup
├── tools_local.py         # Custom tool definitions
├── tests/                 # Test suite (to be added)
├── docs/                  # Documentation
├── .env.example           # Environment template
├── .cursorrules           # AI assistant rules
├── TODO.md                # Project roadmap
├── DEVELOPMENT.md         # This file
└── README.md              # User-facing docs
```

### Where Things Go

**Adding a new tool?** → `tools_local.py`  
**Adding CLI functionality?** → `src/cli.py`  
**Adding configuration?** → `src/config.py` + `.env.example`  
**Adding tests?** → `tests/test_*.py`  
**Adding documentation?** → `docs/` or update README.md

---

## Code Style

### Python Standards

We follow PEP 8 with these specifics:

**Line length**: 100 characters max  
**Indentation**: 4 spaces (no tabs)  
**Quotes**: Double quotes for strings  
**Imports**: Organized in three groups

### Type Hints

Always use type hints:

```python
# Good ✅
def calculate(a: int, b: int) -> int:
    return a * b

# Bad ❌
def calculate(a, b):
    return a * b
```

### Docstrings

Every function needs a docstring:

```python
def write_text(path: str, content: str) -> str:
    """Write UTF-8 text to a file.
    
    Creates or overwrites a file with the given content.
    
    Args:
        path: File path relative to current directory
        content: Text content to write
        
    Returns:
        Confirmation message with file path
        
    Raises:
        IOError: If file cannot be written
        
    Example:
        >>> write_text("test.txt", "Hello World")
        "Wrote to test.txt"
    """
    # Implementation...
```

### Naming Conventions

```python
# Functions and variables
def my_function():
    my_variable = "value"

# Classes
class MyClass:
    pass

# Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Private/internal
def _internal_helper():
    pass
```

### Import Organization

```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party packages
from rich.console import Console
from smolagents import tool

# Local modules
from src.config import config
from src.logger import logger
```

---

## Git Workflow

### Branch Strategy

**main** - Production-ready code only  
**feature/*** - New features  
**fix/*** - Bug fixes  
**docs/*** - Documentation updates  
**test/*** - Test additions

### Creating a Feature

```bash
# Start from main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/add-json-tool

# Make your changes...
# Test thoroughly!

# Commit with conventional format
git add .
git commit -m "feat: Add JSON file reading tool"

# Push to GitHub
git push origin feature/add-json-tool

# Create Pull Request on GitHub
```

### Commit Message Format

Use **conventional commits**:

```bash
feat: Add new feature
fix: Fix a bug
docs: Update documentation
test: Add or update tests
refactor: Refactor code without changing behavior
chore: Update dependencies, configs, etc.
style: Format code (no logic changes)
```

**Examples**:
```bash
feat: Add list_files tool with glob support
fix: Resolve timeout issue in run_shell
docs: Update README with troubleshooting section
test: Add unit tests for calculator tool
refactor: Extract config loading into separate module
chore: Update smolagents to 1.2.0
```

### Before Committing

- [ ] Code works locally
- [ ] No print() statements (use logger instead)
- [ ] Type hints added
- [ ] Docstrings written
- [ ] No .env or secrets committed
- [ ] TODO.md updated if relevant

---

## Writing Tools

### Tool Template

```python
from smolagents import tool
from src.logger import logger

@tool
def my_tool(param: str) -> str:
    """Brief one-line description.
    
    Longer explanation of what the tool does and when to use it.
    The agent reads this docstring to understand the tool!
    
    Args:
        param: Description of what this parameter does
        
    Returns:
        Description of what the tool returns (always a string)
        
    Example:
        my_tool("example")  # Returns "Result: example"
    """
    try:
        logger.info(f"Tool called with: {param}")
        
        # Your implementation here
        result = do_something(param)
        
        logger.info(f"Tool succeeded: {result}")
        return f"Success: {result}"
        
    except Exception as e:
        logger.error(f"Tool failed: {e}", exc_info=True)
        return f"Error: {str(e)}"
```

### Tool Best Practices

1. **Clear docstring** - The model reads this to understand what the tool does
2. **Return strings** - Models handle strings better than objects
3. **Handle errors** - Always use try/except
4. **Log everything** - Helps with debugging
5. **Keep it simple** - One tool = one job

### Adding Tools to Agent

In `src/agent.py`:

```python
from tools_local import calculator, write_text, read_text, run_shell
from tools_local import my_new_tool  # Add import

def create_agent(model, config):
    agent = CodeAgent(
        tools=[calculator, write_text, read_text, run_shell, my_new_tool],  # Add here
        model=model,
        # ...
    )
    return agent
```

---

## Testing

### Test Structure

Tests go in `tests/` directory:

```
tests/
├── __init__.py
├── test_config.py      # Tests for src/config.py
├── test_tools.py       # Tests for tools_local.py
└── test_agent.py       # Tests for src/agent.py
```

### Writing Tests

```python
# tests/test_tools.py
import pytest
from tools_local import calculator, write_text

def test_calculator_multiplies():
    """Test calculator tool multiplies correctly."""
    result = calculator(5, 6)
    assert result == 30

def test_calculator_with_negatives():
    """Test calculator handles negative numbers."""
    result = calculator(-3, 4)
    assert result == -12

def test_write_text_creates_file(tmp_path):
    """Test write_text creates a file."""
    test_file = tmp_path / "test.txt"
    result = write_text(str(test_file), "Hello")
    
    assert test_file.exists()
    assert test_file.read_text() == "Hello"
    assert "test.txt" in result
```

### Running Tests

```bash
# Install pytest
pip install pytest

# Run all tests
pytest

# Run specific test file
pytest tests/test_tools.py

# Run with output
pytest -v

# Run with coverage
pip install pytest-cov
pytest --cov=src --cov-report=html
```

---

## Configuration

### Environment Variables

All configuration goes in `.env`:

```bash
# LLM Configuration
MODEL_ID=Qwen3-4B-Instruct-2507-Q4_K_M.gguf
API_BASE=http://127.0.0.1:8080/v1
API_KEY=local
TEMPERATURE=0.1
MAX_TOKENS=2048

# Agent Configuration
STREAM_OUTPUTS=true
MAX_STEPS=10

# Logging
LOG_LEVEL=INFO
LOG_FILE=agent.log
LOG_TO_FILE=true
LOG_TO_CONSOLE=true

# Safety
SHELL_APPROVAL_REQUIRED=true
ALLOWED_PATHS=.
```

### Adding New Config

1. Add to `.env.example` with comment
2. Add to `src/config.py`:

```python
class Config:
    # Existing config...
    
    # New setting
    NEW_SETTING: str = os.getenv("NEW_SETTING", "default_value")
    NEW_NUMBER: int = int(os.getenv("NEW_NUMBER", "42"))
    NEW_FLAG: bool = os.getenv("NEW_FLAG", "true").lower() == "true"
```

3. Use in code:

```python
from src.config import config

value = config.NEW_SETTING  # Don't use os.getenv() directly!
```

---

## Security

### Critical Rules

1. **Never commit secrets** - Check `.gitignore` includes `.env`
2. **Validate paths** - Prevent `../../etc/passwd` attacks
3. **Require approval** - Shell commands need human approval
4. **Log security events** - Track what commands were run

### Path Validation Example

```python
from pathlib import Path

def validate_path(path: str) -> Path:
    """Validate file path is within allowed directory.
    
    Args:
        path: Path to validate
        
    Returns:
        Validated Path object
        
    Raises:
        ValueError: If path escapes allowed directory
    """
    resolved = Path(path).resolve()
    allowed = Path.cwd().resolve()
    
    if not str(resolved).startswith(str(allowed)):
        raise ValueError(f"Path traversal detected: {path}")
        
    return resolved
```

### Shell Command Safety

The `run_shell` tool has two safety layers:

1. **Denylist** - Blocks dangerous commands
2. **Approval gate** - Human must approve each command

```python
DENIED_COMMANDS = {"rm", "rmdir", "sudo", "su", "chmod", "chown"}

# Check if command is denied
if any(cmd in command for cmd in DENIED_COMMANDS):
    return "Error: Command blocked for safety"

# Require human approval
approval = input(f"Run: {command}? [y/N]: ")
if approval.lower() != "y":
    return "Command cancelled by user"
```

---

## Common Patterns

### Logging

```python
from src.logger import logger

# Different log levels
logger.debug("Detailed debugging info")
logger.info("Normal operation info")
logger.warning("Something unusual happened")
logger.error("An error occurred", exc_info=True)  # Includes stack trace
```

### Error Handling

```python
# Always handle specific exceptions
try:
    with open(path) as f:
        content = f.read()
except FileNotFoundError:
    logger.error(f"File not found: {path}")
    return f"Error: {path} does not exist"
except PermissionError:
    logger.error(f"Permission denied: {path}")
    return f"Error: Cannot access {path}"
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return f"Error: {str(e)}"
```

### File Operations

```python
from pathlib import Path

# Use Path instead of os.path
path = Path("data/file.txt")

# Check existence
if path.exists():
    content = path.read_text()

# Create parent directories
path.parent.mkdir(parents=True, exist_ok=True)

# Write content
path.write_text("content", encoding="utf-8")
```

---

## Troubleshooting

### Common Issues

**Import errors**
```bash
# Make sure you installed in editable mode
pip install -e .

# Make sure you're in the right directory
cd ~/projects/my-agent-project
```

**Connection refused (llama.cpp)**
```bash
# Check if llama.cpp is running
curl http://127.0.0.1:8080/v1/models

# Check .env has correct API_BASE
grep API_BASE .env
```

**Config not loading**
```bash
# Make sure .env exists
ls -la .env

# Test config loading
python -c "from src.config import config; print(config.MODEL_ID)"
```

**Agent gives weird responses**
- Temperature too high? Try 0.1-0.3
- Model too small? Try 7B+ model
- Use task-based prompts, not conversational ones

### Getting Help

1. Check `agent.log` for error messages
2. Read error messages carefully
3. Search GitHub issues
4. Ask in discussions
5. Create a detailed bug report

---

## Quick Reference

### Common Commands

```bash
# Run interactive CLI
python -m src.cli

# Run single prompt
python -m src.cli "your prompt here"

# Run tests
pytest

# Format code
ruff format .

# Check code
ruff check .

# View logs
tail -f agent.log
```

### File Locations

- Config: `src/config.py` + `.env`
- Tools: `tools_local.py`
- Logs: `agent.log`
- Tests: `tests/`
- Docs: `docs/` and `*.md` files

---

## Resources

- [smolagents Documentation](https://github.com/huggingface/smolagents)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [PEP 8 Style Guide](https://pep8.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**Last Updated**: 2026-02-16
