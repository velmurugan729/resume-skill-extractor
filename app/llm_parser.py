from openai import OpenAI
import json
from typing import Dict
from tenacity import retry, stop_after_attempt, wait_exponential

class LLMParser:
    PROMPT_TEMPLATE = """Extract the following from this resume:
    - full_name
    - email
    - phone
    - skills (as list)
    - experience (list with: title, company, duration)
    - education (list with: degree, institution, year)
    
    Return ONLY valid JSON. Resume:
    {text}"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.max_tokens = 4096  # GPT-3.5 limit

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def extract_data(self, text: str) -> Dict:
        """Extract structured data with retry logic"""
        truncated = self._truncate_text(text)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a resume parser that outputs strict JSON."
            }, {
                "role": "user",
                "content": self.PROMPT_TEMPLATE.format(text=truncated)
            }],
            temperature=0,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    def _truncate_text(self, text: str) -> str:
        """Ensure text fits within token limits"""
        return text[:self.max_tokens//2]  # Conservative estimate
