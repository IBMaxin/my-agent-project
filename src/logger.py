"""Logging configuration for the agent."""
import logging
import sys
from pathlib import Path
from rich.logging import RichHandler
from src.config import config


def setup_logger(name: str = "agent") -> logging.Logger:
    """Setup and configure logger with file and console handlers.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with Rich formatting
    if config.LOG_TO_CONSOLE:
        console_handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_path=False,
        )
        console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
        console_formatter = logging.Formatter(
            "%(message)s",
            datefmt="[%X]",
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if config.LOG_TO_FILE:
        log_path = config.get_log_path()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # Always log everything to file
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


# Create default logger
logger = setup_logger()
