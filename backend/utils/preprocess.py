# File: backend/utils/preprocess.py

import re

def clean_text(text, preserve_case=False, remove_numbers=False):
    """
    Clean the text by removing extra spaces, special characters, and converting to lowercase.
    Also removes common headers/footers and normalizes unicode.
    Options:
        preserve_case: If True, does not lowercase the text.
        remove_numbers: If True, removes all digits.
    """
    if not text:
        return ""
    # Remove common headers/footers (example: page numbers, "resume", etc.)
    text = re.sub(r"\b(page|resume|curriculum vitae|cv)\b", "", text, flags=re.IGNORECASE)
    # Normalize unicode
    text = text.encode("ascii", "ignore").decode()
    # Remove numbers if specified
    if remove_numbers:
        text = re.sub(r"\d+", "", text)
    # Replace multiple spaces/newlines with a single space
    text = re.sub(r"\s+", " ", text)
    # Remove special characters except for basic punctuation
    text = re.sub(r"[^\w\s.,;:!?-]", "", text)
    # Remove spaces before punctuation
    text = re.sub(r"\s+([.,;:!?-])", r"\1", text)
    # Lowercase unless preserve_case is True
    if not preserve_case:
        text = text.lower()
    return text.strip()

def extract_skills(text):
    # Example: simple keyword-based extraction
    skills_db = {"python", "java", "c++", "javascript", "html", "css", "react", "node.js", "tensorflow", "sql", "flask"}
    words = set(text.lower().split())
    return list(skills_db.intersection(words))

def extract_core_topics(text):
    # Example: extract topics based on keywords
    topics_db = {"machine learning", "data science", "web development", "cloud", "database", "nlp", "ai"}
    found = []
    for topic in topics_db:
        if topic in text.lower():
            found.append(topic)
    return found
