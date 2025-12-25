import os
from dotenv import load_dotenv

load_dotenv()


def get_deepseek_api_key() -> str:
    """Get DeepSeek API key from environment variables."""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY not found in environment variables. "
            "Please set it in your .env file."
        )
    return api_key


def get_deepseek_base_url() -> str:
    """Get DeepSeek API base URL, defaults to official endpoint."""
    return os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")


def get_deepseek_model() -> str:
    """Get DeepSeek model name to use."""
    return os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
