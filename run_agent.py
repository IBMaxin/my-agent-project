#!/usr/bin/env python3
import os
from smolagents import CodeAgent, OpenAIServerModel, tool
from tools_local import write_text, read_text, run_shell


@tool
def calculator(a: int, b: int) -> int:
    """Multiply two integers and return the result.

    Args:
        a: The first integer to multiply.
        b: The second integer to multiply.

    Returns:
        The product of a and b.
    """
    return a * b


def main():
    model = OpenAIServerModel(
        model_id="Qwen3-4B-Instruct-2507-Q4_K_M.gguf",
        api_base="http://127.0.0.1:8080/v1",
        api_key=os.environ.get("OPENAI_API_KEY", "local"),
        temperature=0.1,  # Low temperature for 4B model reliability
    )

    agent = CodeAgent(
        tools=[calculator, write_text, read_text, run_shell],
        model=model,
        stream_outputs=True,
    )

    prompt = (
        "Create a README.md that says hello and lists 3 project goals.\n\n"
        "IMPORTANT: You MUST write files using write_text(path, content). "
        "Do NOT use Python open() or file operations.\n\n"
        "After writing, use read_text('README.md') to verify your work."
    )

    print(agent.run(prompt))


if __name__ == "__main__":
    main()


