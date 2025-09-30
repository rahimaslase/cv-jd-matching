"""Configuration management for CV matching system."""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_base_url: str = Field(default="https://api.core42.ai/v1", description="OpenAI API base URL")
    openai_model: str = Field(default="gpt-5", description="OpenAI model to use")
    openai_temperature: float = Field(default=0.1, ge=0.0, le=2.0, description="OpenAI temperature setting")
    openai_max_tokens: int = Field(default=1000, ge=1, le=8000, description="Maximum tokens for OpenAI response")
    
    # Application Configuration
    app_name: str = Field(default="CV Matching API", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # API Configuration
    host: str = Field(default="0.0.0.0", description="API host")
    port: int = Field(default=8000, ge=1, le=65535, description="API port")
    
    # Analysis Configuration
    max_retries: int = Field(default=3, ge=1, le=10, description="Maximum retries for OpenAI API calls")
    timeout_seconds: int = Field(default=60, ge=10, le=300, description="Timeout for API calls in seconds")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
