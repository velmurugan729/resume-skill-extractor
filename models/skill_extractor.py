from transformers import pipeline

def extract_skills(text):
    # Dummy version – replace with real NLP logic later
    skills_list = ["Python", "Java", "Machine Learning", "SQL"]
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    return found_skills
