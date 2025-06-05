import re

def extract_email(text):
    return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)

def extract_phone(text):
    return re.findall(r"\b\d{10}\b", text)

def extract_name(text):
    lines = text.strip().split("\n")
    return lines[0]  # Usually first line is name
