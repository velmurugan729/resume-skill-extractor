from openai import OpenAI
import json
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential


class LLMParser:
    PROMPT_TEMPLATE = """You are a resume parser.
Extract the following from the resume text provided:
- full_name
- email
- phone
- skills: list of skills/technologies mentioned
- experience: list of dictionaries with keys: title, company, duration
- education: list of dictionaries with keys: degree, institution, year

Return the result strictly as a valid JSON object without any comments or explanation.
Resume:
{text}"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.max_tokens = 4096  # GPT-3.5 limit

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def extract_data(self, text: str) -> Dict[str, Any]:
        """Extract structured data using LLM with retry"""
        truncated = self._truncate_text(text)

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that returns only JSON data."
                },
                {
                    "role": "user",
                    "content": self.PROMPT_TEMPLATE.format(text=truncated)
                }
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

        try:
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            raise ValueError("Failed to parse LLM response as JSON") from e

    def _truncate_text(self, text: str) -> str:
        """Ensure input text is within token limits (approx. 2k tokens = ~8k chars)"""
        return text[:8000]
