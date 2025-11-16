# src/awesome_copilot/config.py
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    server_name: str = "awesome-copilot/mcp"
    version: str = "0.1.0"
    transport: str = "http"  # ex: stdio, http
    host: str = "127.0.0.1"
    port: int = 8000
    api_key: Optional[str] = None

    model_config = ConfigDict(env_file=".env", extra="ignore")
