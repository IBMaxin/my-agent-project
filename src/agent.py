"""Agent initialization and configuration."""
from smolagents import CodeAgent, OpenAIServerModel, tool
from src.config import config
from src.logger import logger
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


def create_agent() -> CodeAgent:
    """Create and configure the CodeAgent.
    
    Returns:
        Configured CodeAgent instance
    """
    logger.info("Initializing OpenAI model with llama.cpp backend")
    logger.debug(
        f"Model config: model_id={config.MODEL_ID}, "
        f"api_base={config.API_BASE}, temperature={config.TEMPERATURE}"
    )
    
    model = OpenAIServerModel(
        model_id=config.MODEL_ID,
        api_base=config.API_BASE,
        api_key=config.API_KEY,
        temperature=config.TEMPERATURE,
    )
    
    logger.info("Creating CodeAgent with tools")
    agent = CodeAgent(
        tools=[calculator, write_text, read_text, run_shell],
        model=model,
        stream_outputs=config.STREAM_OUTPUTS,
        max_steps=config.MAX_STEPS,
    )
    
    return agent
