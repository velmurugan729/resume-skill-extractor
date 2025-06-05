import re
import spacy
import subprocess
import importlib.util

# Auto-download spaCy model if missing
model_name = "en_core_web_sm"
if importlib.util.find_spec(model_name) is None:
    subprocess.run(["python", "-m", "spacy", "download", model_name])

nlp = spacy.load(model_name)

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "Not found"

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not found"

def extract_skills(text):
    known_skills = ["python", "java", "sql", "machine learning", "django", "c++"]
    found = []
    for skill in known_skills:
        if skill.lower() in text.lower():
            found.append(skill)
    return list(set(found))

def extract_experience(text):
    pattern = r'(\d+)\+?\s+(years|yrs)\s+experience'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else "Not found"

def extract_all(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text)
    }
