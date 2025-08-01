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
from utils.preprocess import clean_text

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
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
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

def extract_education(text):
    """Extracts education information from text."""
    education_keywords = ["bachelor", "master", "phd", "b.tech", "m.tech", "bsc", "msc", "mba", "degree", "university", "college"]
    found = []
    for line in text.split("\n"):
        for keyword in education_keywords:
            if keyword in line.lower():
                found.append(line.strip())
    return found

def preprocess_text(text):
    """Cleans and preprocesses the text."""
    return clean_text(text)

def parse_resume(file_path):
    """Parses resume and extracts key details."""
    file_ext = file_path.split(".")[-1].lower()
    try:
        if file_ext == "pdf":
            text = extract_text_from_pdf(file_path)
        elif file_ext == "docx":
            text = extract_text_from_docx(file_path)
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
    except Exception as e:
        return {"success": False, "error": str(e)}

    # Extract Information
    text_cleaned = preprocess_text(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text_cleaned)
    name = extract_name(text)
    education = extract_education(text)

    return {
        "success": True,
        "name": name,
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "skills": skills,
        "education": education,
        "raw_text": text_cleaned,
        "preview": text_cleaned[:200] + "..." if len(text_cleaned) > 200 else text_cleaned
    }

# Example Usage
if __name__ == "__main__":
    resume_data = parse_resume("test_resume.pdf")
    print(resume_data)
