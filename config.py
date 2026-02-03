"""Configuration management for the Agentic Honey-Pot system."""
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Authentication
    api_key: str = "default_secret_key_change_me"
    
    # LLM Configuration
    llm_provider: Literal["gemini", "anthropic", "openai"] = "gemini"
    google_api_key: str = ""
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    
    # GUVI Integration
    guvi_callback_url: str = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    
    # Conversation Settings
    max_conversation_turns: int = 20
    scam_threshold: float = 0.7
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
