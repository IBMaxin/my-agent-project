"""Configuration management for the agent."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Config:
    """Configuration settings loaded from environment variables."""

    # LLM Settings
    MODEL_ID: str = os.getenv("MODEL_ID", "Qwen3-4B-Instruct-2507-Q4_K_M.gguf")
    API_BASE: str = os.getenv("API_BASE", "http://127.0.0.1:8080/v1")
    API_KEY: str = os.getenv("API_KEY", "local")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2048"))

    # Agent Settings
    STREAM_OUTPUTS: bool = os.getenv("STREAM_OUTPUTS", "true").lower() == "true"
    MAX_STEPS: int = int(os.getenv("MAX_STEPS", "10"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE: str = os.getenv("LOG_FILE", "agent.log")
    LOG_TO_FILE: bool = os.getenv("LOG_TO_FILE", "true").lower() == "true"
    LOG_TO_CONSOLE: bool = os.getenv("LOG_TO_CONSOLE", "true").lower() == "true"

    # Safety
    SHELL_APPROVAL_REQUIRED: bool = (
        os.getenv("SHELL_APPROVAL_REQUIRED", "true").lower() == "true"
    )
    ALLOWED_PATHS: str = os.getenv("ALLOWED_PATHS", ".")

    @classmethod
    def get_project_root(cls) -> Path:
        """Get the project root directory."""
        return Path(__file__).parent.parent

    @classmethod
    def get_log_path(cls) -> Path:
        """Get the full path to the log file."""
        return cls.get_project_root() / cls.LOG_FILE


config = Config()
