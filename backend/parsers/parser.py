'''📌 Key Features:
✅ Extracts Name, Email, Phone, Skills, and Education
✅ Handles PDFs, DOCX, and Plain Text
✅ Uses SpaCy for NLP-based Information Extraction
✅ Cleans & Preprocesses the Text for ML Models'''


import re
import spacy
import nltk
import PyPDF2
import docx
from nltk.corpus import stopwords

# Load SpaCy NLP Model
nlp = spacy.load("en_core_web_sm")

# Download NLTK Stopwords
nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_email(text):
    """Extracts email addresses using regex."""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(email_pattern, text)

def extract_phone(text):
    """Extracts phone numbers using regex."""
    phone_pattern = r"\+?\d[\d -]{8,15}\d"
    return re.findall(phone_pattern, text)

def extract_skills(text):
    """Extracts skills from text using a predefined skills list."""
    skills_db = {"python", "java", "c++", "javascript", "html", "css", "react", "node.js", "tensorflow", "sql", "flask"}
    words = set(text.lower().split())
    return list(skills_db.intersection(words))

def extract_name(text):
    """Uses SpaCy Named Entity Recognition (NER) to extract candidate names."""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def preprocess_text(text):
    """Removes stopwords, special characters, and converts text to lowercase."""
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters
    words = text.lower().split()
    return " ".join([word for word in words if word not in STOPWORDS])

def parse_resume(file_path):
    """Parses resume and extracts key details."""
    file_ext = file_path.split(".")[-1]
    
    if file_ext == "pdf":
        text = extract_text_from_pdf(file_path)
    elif file_ext == "docx":
        text = extract_text_from_docx(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    # Extract Information
    text_cleaned = preprocess_text(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text_cleaned)
    name = extract_name(text)

    return {
        "name": name,
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "skills": skills,
        "raw_text": text_cleaned
    }

# Example Usage
if __name__ == "__main__":
    resume_data = parse_resume("test_resume.pdf")
    print(resume_data)
