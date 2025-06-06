import os

class Settings:
    def __init__(self):
        self.llm_api_key = os.getenv("OPENAI_API_KEY", "")
        
settings = Settings()
