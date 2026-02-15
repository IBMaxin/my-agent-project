# Project: my-agent-project

## Project purpose
Build a local-first coding agent on Debian 13 that can plan work (todos), edit files, run tests, and delegate subtasks to subagents, while staying responsive and safe.

## Tech stack
- OS: Debian 13
- LLM runtime: llama.cpp (local server)
- Default model: Qwen3-4B-Instruct-2507-Q4_K_M.gguf
- Acceleration: Vulkan offload when available (ngl set high for speed)

## Rules (how to work)
- Ask before making destructive changes (deleting files, rewriting large sections, resetting git history).
- Keep changes small and incremental; prefer multiple small commits over one huge commit.
- After code changes: run the smallest relevant test or command, then report results.
- If unsure: read files first (`ls`, `glob`, `grep`, `read_file`) before editing.
- Prefer targeted edits (`edit_file`) over rewriting whole files.
- Keep responses short by default; only go long when I ask.

## Repo layout (initial)
- `README.md`: project notes and usage
- `.deepagents/AGENTS.md`: these project conventions for the agent
- `src/`: application code (create when we start coding)
- `tests/`: tests (create when we add tests)

## How to run common commands (local)
- List files: `ls -la`
- Search text: `grep -R "pattern" -n .`
- Run tests: (to be added once we pick a language/framework)

