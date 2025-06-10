import os
import spacy 

class Settings:
    def __init__(self):
        self.APP_NAME = "Resume Parser extractor"
        self.OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
        self.USE_AI = True
        self.DEBUG = False
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except:
            os.system("python -m spacy download en_core_web_lg")
            self.nlp = spacy.load("en_core_web_lg")

settings = Settings()
