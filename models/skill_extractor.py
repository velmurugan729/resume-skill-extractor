from transformers import pipeline

def extract_skills_with_llm(text: str):
    """Uses a zero-shot classifier to extract relevant skills."""
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    skills = ["Python", "Java", "SQL", "Machine Learning", "Deep Learning", "NLP", "Django", "React", "C++", "Cloud"]
    result = classifier(text, skills, multi_label=True)
    return [label for label, score in zip(result['labels'], result['scores']) if score > 0.5]
