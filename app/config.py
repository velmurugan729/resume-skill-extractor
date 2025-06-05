import os
from pydantic_settings import BaseSettings # type: ignore

class Settings(BaseSettings):
    llm_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    class Config:
        env_file = ".env"

settings = Settings()
