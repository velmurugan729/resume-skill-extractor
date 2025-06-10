import fitz  # PyMuPDF
import re
from typing import Dict, List
import spacy
import pdfplumber

nlp = spacy.load("en_core_web_sm")

class PDFParser:
    SKILLS = {
        'Programming': ['python', 'java', 'c++', 'javascript', 'go', 'rust'],
        'Cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
        'Databases': ['sql', 'postgresql', 'mongodb', 'redis'],
        'Tools': ['git', 'jenkins', 'terraform', 'ansible']
    }

    def __init__(self):
        self.email_re = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        self.phone_re = re.compile(r'(\+\d{1,3}\s?)?(\(?\d{3}\)?)[\s.-]?\d{3}[\s.-]?\d{4}')
        self.edu_keywords = ['bachelor', 'master', 'b.sc', 'm.sc', 'b.e', 'm.e', 'phd', 'university', 'college']
        self.exp_keywords = ['experience', 'intern', 'developer', 'engineer', 'manager']

    def extract_text(self, pdf_path: str) -> str:
        try:
            with fitz.open(pdf_path) as doc:
                text = "".join(page.get_text() for page in doc)
                if len(text) > 50:
                    return text

            with pdfplumber.open(pdf_path) as pdf:
                return "".join(page.extract_text() or "" for page in pdf.pages)
        except Exception:
            return ""

    def extract_basic_info(self, text: str) -> Dict:
        return {
            'name': self._extract_name(text),
            'email': self._extract_email(text),
            'phone': self._extract_first_match(self.phone_re, text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text)
        }

    def _extract_name(self, text: str) -> str:
        doc = nlp(text[:500])  # Only look at top part of resume
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()
        return text.strip().split('\n')[0]  # fallback

    def _extract_email(self, text: str) -> str:
        doc = nlp(text)
        for token in doc:
            if token.like_email:
                return token.text
        return self._extract_first_match(self.email_re, text)

    def _extract_first_match(self, pattern: re.Pattern, text: str) -> str:
        match = pattern.search(text)
        return match.group(0) if match else ""

    def _extract_skills(self, text: str) -> List[str]:
        text_lower = text.lower()
        return sorted({
            skill.title()
            for category in self.SKILLS.values()
            for skill in category
            if skill in text_lower
        })

    def _extract_experience(self, text: str) -> List[Dict]:
        lines = text.lower().split('\n')
        exp_lines = [line.strip() for line in lines if any(k in line for k in self.exp_keywords)]
        return [{"title": line} for line in exp_lines[:3]]  # limit to first 3

    def _extract_education(self, text: str) -> List[Dict]:
        lines = text.lower().split('\n')
        edu_lines = [line.strip() for line in lines if any(k in line for k in self.edu_keywords)]
        return [{"degree": line} for line in edu_lines[:3]]
