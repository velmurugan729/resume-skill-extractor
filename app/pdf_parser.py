import fitz  # PyMuPDF
import re
from typing import Dict, List
import pdfplumber  # type: ignore # Alternative parser

class PDFParser:
    SKILLS = {
        'Programming': ['python', 'java', 'c++', 'javascript', 'go', 'rust'],
        'Cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
        'Databases': ['sql', 'postgresql', 'mongodb', 'redis'],
        'Tools': ['git', 'jenkins', 'terraform', 'ansible']
    }

    def __init__(self):
        self.email_re = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        self.phone_re = re.compile(r'(\+\d{1,3}\s?)?(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}')

    def extract_text(self, pdf_path: str) -> str:
        """Extract text with fallback mechanism"""
        try:
            # First try PyMuPDF for speed
            with fitz.open(pdf_path) as doc:
                text = "".join(page.get_text() for page in doc)
                if len(text) > 50:  # Minimum viable text check
                    return text
            
            # Fallback to pdfplumber for problematic PDFs
            with pdfplumber.open(pdf_path) as pdf:
                return "".join(page.extract_text() or "" for page in pdf.pages)
            
        except Exception:
            return ""

    def extract_basic_info(self, text: str) -> Dict:
        """Extract contact info and skills"""
        return {
            'name': self._extract_name(text),
            'email': self._extract_first_match(self.email_re, text),
            'phone': self._extract_first_match(self.phone_re, text),
            'skills': self._extract_skills(text)
        }

    def _extract_name(self, text: str) -> str:
        """Improved name extraction"""
        if not text:
            return ""
        
        # Try first non-empty line
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return lines[0] if lines else ""

    def _extract_first_match(self, pattern: re.Pattern, text: str) -> str:
        match = pattern.search(text)
        return match.group(0) if match else ""

    def _extract_skills(self, text: str) -> List[str]:
        """Categorized skill extraction"""
        text_lower = text.lower()
        return [
            skill.title() 
            for category in self.SKILLS.values() 
            for skill in category 
            if skill in text_lower
        ]
