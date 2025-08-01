import re

def extract_skills(text):
    # Expanded and realistic skillset
    skills_db = {
        "python", "java", "c++", "javascript", "html", "css", "react", "node.js", "node", "express",
        "spring boot", "flask", "django", "mysql", "mongodb", "sql", "postgresql",
        "tensorflow", "pytorch", "machine learning", "deep learning", "nlp",
        "docker", "kubernetes", "git", "github", "linux", "aws", "azure", "firebase",
        "problem solving", "data structures", "algorithms", "communication", "leadership"
    }
    text = text.lower()
    found_skills = []
    for skill in skills_db:
        # Match whole word or phrase using regex
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)
    return found_skills


def extract_core_topics(text):
    topics_db = {
        "machine learning", "data science", "web development", "cloud", "database",
        "nlp", "ai", "frontend", "backend", "devops", "microservices", "rest api",
        "system design", "software architecture", "testing", "deployment"
    }
    text = text.lower()
    found = []
    for topic in topics_db:
        if topic in text:
            found.append(topic)
    return found
