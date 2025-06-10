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
        """Extract contact info, skills, and experience (basic heuristic)"""
        return {
            'name': self._extract_name(text),
            'email': self._extract_first_match(self.email_re, text),
            'phone': self._extract_first_match(self.phone_re, text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text) 
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
    def _extract_experience(self, text: str):
        """
        Heuristic extraction for experience sections.
        Looks for lines under 'Experience' or similar headings.
        """
        lines = text.split('\n')
        experience = []
        capture = False
        for line in lines:
            if re.search(r'experience|work history|employment', line, re.I):
                capture = True
                continue
            if capture:
                # Stop at next section
                if re.match(r'^[A-Z][A-Za-z ]{2,}:$', line.strip()):
                    break
                # Simple pattern: Job Title at Company (Duration)
                m = re.match(r'(.+?) at (.+?) \((.+?)\)', line.strip())
                if m:
                    experience.append({
                        'title': m.group(1).strip(),
                        'company': m.group(2).strip(),
                        'duration': m.group(3).strip()
                    })
                elif line.strip():
                    # Fallback: just add line as title
                    experience.append({'title': line.strip(), 'company': '', 'duration': ''})
        return experience
