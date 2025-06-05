import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_resume_info(text: str) -> dict:
    prompt = f"""
    Extract the following details in JSON format from this resume:
    - Name
    - Email
    - Phone
    - Skills
    - Education
    - Work Experience

    Resume:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response["choices"][0]["message"]["content"]

    # Ensure it’s valid JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse model output as JSON", "raw": content}
