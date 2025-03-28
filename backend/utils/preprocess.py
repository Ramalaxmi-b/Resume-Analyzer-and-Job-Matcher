# File: backend/utils/preprocess.py

import re

def clean_text(text):
    """Clean the text by removing extra spaces, special characters, and converting to lowercase."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)         # Replace multiple spaces with a single space
    text = re.sub(r"[^\w\s]", "", text)        # Remove special characters
    return text.lower().strip()
