"""Interactive CLI for the agent."""
import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from smolagents import CodeAgent, OpenAIServerModel
from src.config import config
from src.logger import logger
from src.agent import create_agent


console = Console()


def print_welcome() -> None:
    """Print welcome message."""
    welcome = """
# My Agent Project

A local AI agent using **smolagents** with **llama.cpp**.

**Commands:**
- `/help` - Show this help
- `/clear` - Clear conversation history
- `/config` - Show current configuration
- `/exit` or `/quit` - Exit the program
- Any other input will be sent to the agent
    """
    console.print(Panel(Markdown(welcome), title="🤖 Welcome", border_style="blue"))


def print_config() -> None:
    """Print current configuration."""
    config_text = f"""
**Model Configuration:**
- Model ID: `{config.MODEL_ID}`
- API Base: `{config.API_BASE}`
- Temperature: `{config.TEMPERATURE}`
- Max Tokens: `{config.MAX_TOKENS}`

**Agent Settings:**
- Stream Outputs: `{config.STREAM_OUTPUTS}`
- Max Steps: `{config.MAX_STEPS}`

**Logging:**
- Log Level: `{config.LOG_LEVEL}`
- Log File: `{config.LOG_FILE}`
    """
    console.print(Panel(Markdown(config_text), title="⚙️  Configuration", border_style="cyan"))


def run_interactive_mode() -> None:
    """Run the agent in interactive REPL mode."""
    print_welcome()
    
    # Create agent
    try:
        agent = create_agent()
        logger.info("Agent initialized successfully")
    except Exception as e:
        console.print(f"[red]Error initializing agent: {e}[/red]")
        logger.error(f"Failed to initialize agent: {e}")
        sys.exit(1)
    
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold green]You[/bold green]").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                command = user_input.lower()
                
                if command in ["/exit", "/quit"]:
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break
                
                elif command == "/help":
                    print_welcome()
                    continue
                
                elif command == "/clear":
                    conversation_history.clear()
                    console.print("[yellow]Conversation history cleared.[/yellow]")
                    logger.info("Conversation history cleared")
                    continue
                
                elif command == "/config":
                    print_config()
                    continue
                
                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    console.print("[yellow]Type /help for available commands[/yellow]")
                    continue
            
            # Process user input with agent
            logger.info(f"User prompt: {user_input}")
            console.print("\n[bold blue]Agent[/bold blue]")
            
            try:
                result = agent.run(user_input)
                console.print(f"\n{result}\n")
                logger.info(f"Agent response: {result}")
                
                # Store in history
                conversation_history.append({"user": user_input, "agent": result})
                
            except Exception as e:
                console.print(f"[red]Error running agent: {e}[/red]")
                logger.error(f"Agent execution error: {e}", exc_info=True)
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type /exit to quit.[/yellow]")
            continue
        
        except EOFError:
            console.print("\n[yellow]Goodbye! 👋[/yellow]")
            break


def run_single_prompt(prompt: str) -> None:
    """Run a single prompt and exit.
    
    Args:
        prompt: The prompt to send to the agent
    """
    try:
        agent = create_agent()
        logger.info(f"Running single prompt: {prompt}")
        result = agent.run(prompt)
        console.print(result)
        logger.info(f"Agent response: {result}")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        logger.error(f"Error running single prompt: {e}", exc_info=True)
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    # Check for single prompt mode
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        run_single_prompt(prompt)
    else:
        run_interactive_mode()


if __name__ == "__main__":
    main()
