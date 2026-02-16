import subprocess
import shlex
from pathlib import Path
from smolagents import tool

# Commands that are always blocked for safety
DENYLIST = ["rm", "rmdir", "sudo", "su", "chmod", "chown"]


def _is_blocked(cmd: str) -> bool:
    """Check if command starts with a blocked word."""
    first_word = shlex.split(cmd)[0] if cmd else ""
    return first_word in DENYLIST


@tool
def write_text(path: str, content: str) -> str:
    """Write UTF-8 text to a file (relative to current directory).

    Args:
        path: The file path to write to (relative to current directory).
        content: The text content to write to the file.

    Returns:
        A confirmation message with bytes written and file path.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} bytes to {p}"


@tool
def read_text(path: str) -> str:
    """Read UTF-8 text from a file (relative to current directory).

    Args:
        path: The file path to read (relative to current directory).

    Returns:
        The file contents as a string, or an error message if the file cannot be read.
    """
    try:
        p = Path(path)
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading {path}: {e}"


@tool
def run_shell(cmd: str) -> str:
    """Run a shell command with human approval. Blocked commands: rm, rmdir, sudo, su, chmod, chown.

    Args:
        cmd: The shell command to execute (e.g., 'git status', 'pytest', 'ls -la').

    Returns:
        The command output (stdout + stderr) or a rejection/error message.
    """
    # Layer 1: Hard denylist
    if _is_blocked(cmd):
        return f"Error: Command '{cmd}' is blocked for safety."

    # Layer 2: Human-in-the-loop approval gate
    print(f"\n{'='*60}")
    print(f"Agent wants to run: {cmd}")
    print(f"{'='*60}")
    approval = input("Approve? [y/N]: ").strip().lower()

    if approval != "y":
        return "Command rejected by user."

    # Execute only after approval
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr
    return output.strip() or "(no output)"
