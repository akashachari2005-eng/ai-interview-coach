"""
Resume Parser
Extracts text and information from PDF resumes
Author: Adarsh
"""

import PyPDF2
import pdfplumber
import spacy
import re
from .skills_database import SKILLS_DB, EDUCATION_KEYWORDS

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


class ResumeParser:
    """Class to handle all resume parsing operations"""

    def __init__(self):
        self.nlp = nlp
        self.skills_db = SKILLS_DB
        self.education_keywords = EDUCATION_KEYWORDS

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from PDF file
        Uses pdfplumber first, falls back to PyPDF2
        """
        text = ""

        # Method 1: pdfplumber (more accurate)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
        except Exception:
            pass

        # Method 2: PyPDF2 (fallback)
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            return None

    def extract_name(self, text):
        """Extract candidate name - improved version"""
        lines = text.strip().split('\n')
        
        # Try first non-empty line (name is usually at top of resume)
        for line in lines[:5]:
            line = line.strip()
            # Skip if empty, contains @ (email), digits (phone), or too long
            if (line and 
                '@' not in line and 
                not any(char.isdigit() for char in line) and
                2 <= len(line.split()) <= 4 and
                len(line) < 50):
                return line
        
        # Fallback to spaCy NER
        doc = self.nlp(text[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        
        return "Unknown"

    def extract_email(self, text):
        """Extract email address from text"""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(pattern, text)
        return emails[0] if emails else None

    def extract_phone(self, text):
        """Extract phone number from text"""
        patterns = [
            r'\+?\d{1,3}[-.\s]?\d{10}',
            r'\+?\d{1,3}[-.\s]?\d{5}[-.\s]?\d{5}',
            r'\d{10}',
            r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',
        ]
        for pattern in patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        return None

    def extract_skills(self, text):
        """Find all technical skills mentioned in the resume"""
        found_skills = []
        text_lower = text.lower()

        for skill in self.skills_db:
            # Word boundary matching to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)

        # Remove duplicates and return
        return list(set(found_skills))

    def extract_education(self, text):
        """Find educational qualifications"""
        education = []
        for keyword in self.education_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                education.append(keyword)
        return list(set(education))

    def extract_experience(self, text):
        """Find companies and years of experience"""
        doc = self.nlp(text)

        # Extract organizations
        companies = []
        for ent in doc.ents:
            if ent.label_ == "ORG":
                companies.append(ent.text)

        # Find years of experience
        years_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience)?',
            r'(?:experience)\s*(?:of)?\s*(\d+)\+?\s*(?:years?|yrs?)',
        ]

        years = []
        for pattern in years_patterns:
            found = re.findall(pattern, text.lower())
            years.extend(found)

        max_years = max([int(y) for y in years], default=0)

        return {
            'companies': list(set(companies))[:10],
            'total_years': max_years
        }

    def extract_linkedin(self, text):
        """Extract LinkedIn URL"""
        pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+'
        urls = re.findall(pattern, text)
        return urls[0] if urls else None

    def extract_github(self, text):
        """Extract GitHub URL"""
        pattern = r'(?:https?://)?(?:www\.)?github\.com/[\w-]+'
        urls = re.findall(pattern, text)
        return urls[0] if urls else None

    def parse(self, pdf_path):
        """
        MAIN METHOD: Parse complete resume

        Args:
            pdf_path (str): Path to PDF file

        Returns:
            dict: All extracted information
        """
        # Step 1: Extract text
        text = self.extract_text_from_pdf(pdf_path)

        if not text:
            return {
                'error': 'Could not extract text from PDF',
                'status': 'failed'
            }

        # Step 2: Extract all information
        result = {
            'name': self.extract_name(text),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'linkedin': self.extract_linkedin(text),
            'github': self.extract_github(text),
            'skills': self.extract_skills(text),
            'education': self.extract_education(text),
            'experience': self.extract_experience(text),
            'raw_text_preview': text[:500],
            'total_text_length': len(text),
            'status': 'success'
        }

        return result