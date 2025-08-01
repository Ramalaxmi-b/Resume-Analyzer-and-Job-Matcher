# File: backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

# Import custom modules using relative imports
from routes.job_matcher import match_resumes_to_jobs, calculate_match_score
from parsers.text_extractor import extract_text_from_pdf, extract_text_from_docx
from utils.preprocess import clean_text
from utils.text_processing import extract_skills, extract_core_topics

# Configuration
UPLOAD_FOLDER = "backend/uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Resume Analyzer API is running!"})

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    print("Received file upload request")
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        print(f"✅ File saved at: {filepath}")
        return jsonify({"message": "File uploaded successfully", "filepath": filepath}), 200

    return jsonify({"error": "Invalid file format"}), 400

@app.route("/parse_resume", methods=["POST"])
def parse_resume():
    data = request.json
    filepath = data.get("filepath")

    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "Invalid or missing file path"}), 400

    if filepath.lower().endswith(".pdf"):
        text, _ = extract_text_from_pdf(filepath)
    elif filepath.lower().endswith(".docx"):
        text, _ = extract_text_from_docx(filepath)
    elif filepath.lower().endswith(".txt"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Unsupported file format"}), 400

    if not text or "Error" in text:
        return jsonify({"error": "Failed to extract text from resume"}), 500

    text_cleaned = clean_text(text)

    entities = {
        "name": None,
        "email": None,
        "phone": None,
        "skills": []
    }

    return jsonify({"text": text_cleaned, "entities": entities}), 200

@app.route("/match_resume", methods=["POST"])
def match_resume():
    data = request.json
    resume_text = data.get("resume_text", "")
    job_description = data.get("job_description", "")

    if not resume_text or not job_description:
        return jsonify({"error": "Both resume_text and job_description are required"}), 400

    score = calculate_match_score(resume_text, job_description)
    return jsonify({"match_score": score}), 200

def generate_interview_questions(matched_skills, core_topics):
    technical_qs = []
    behavioral_qs = [
        "Tell me about a time you failed and what you learned from it.",
        "Describe a time you had to learn a new technology quickly.",
        "How do you prioritize tasks when working under a tight deadline?"
    ]
    core_qs = []

    for skill in matched_skills:
        if skill in ["python", "java", "c++"]:
            technical_qs.append(f"What are the differences between {skill} and other programming languages?")
            technical_qs.append(f"How have you used {skill} in real-world projects?")
        elif skill in ["react", "html", "css", "javascript"]:
            technical_qs.append(f"How do you manage state in a {skill}-based application?")
            technical_qs.append(f"What are the key performance optimizations in {skill}?")
        elif skill in ["flask", "django", "node.js", "spring boot"]:
            technical_qs.append(f"How would you design a scalable backend using {skill}?")
            technical_qs.append(f"What are the common security concerns with {skill}?")
        elif skill in ["sql", "mongodb", "mysql", "postgresql"]:
            technical_qs.append(f"How do you optimize queries in {skill}?")
            technical_qs.append(f"Explain indexing in {skill}.")
        elif skill in ["tensorflow", "pytorch", "machine learning"]:
            technical_qs.append(f"Explain a machine learning project you've built using {skill}.")
            technical_qs.append(f"What are the challenges in training models using {skill}?")
        else:
            technical_qs.append(f"Tell me how you've applied {skill} in a past project.")

    for topic in core_topics:
        if "system design" in topic:
            core_qs.append("How would you design a scalable job-matching platform?")
        elif "web development" in topic:
            core_qs.append("What’s your approach to full-stack development?")
        elif "cloud" in topic:
            core_qs.append("Compare AWS, Azure, and GCP. Which would you choose and why?")
        elif "nlp" in topic:
            core_qs.append("What NLP pipeline would you use to analyze resume text?")
        else:
            core_qs.append(f"What do you know about {topic}?")

    return {
        "technical": technical_qs[:5],
        "nonTechnical": behavioral_qs[:3],
        "core": core_qs[:5]
    }

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    resume_text = data.get("resume_text", "")
    job_description = data.get("job_description", "")

    if not resume_text or not job_description:
        return jsonify({"success": False, "error": "Both resume_text and job_description are required"}), 400

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)
    core_topics = extract_core_topics(job_description)

    matched = set(resume_skills) & set(jd_skills)
    missing = set(jd_skills) - set(resume_skills)
    score = int(len(matched) / max(1, len(jd_skills)) * 100)
    suggestions = f"Consider adding these skills: {', '.join(missing)}" if missing else "Great match!"

    questions = generate_interview_questions(list(matched), core_topics)

    preparation_plan = [
        {"topic": skill, "title": f"Improve your {skill} skills", "link": f"https://www.google.com/search?q={skill}+tutorial"}
        for skill in missing
    ]

    resume_feedback = []
    if not matched:
        resume_feedback.append("Your resume lacks relevant keywords. Add technical skills aligned with the job.")
    if len(resume_text) < 200:
        resume_feedback.append("Your resume content seems too short. Consider adding more detailed experience.")
    if not any(word in resume_text.lower() for word in ["project", "experience", "internship"]):
        resume_feedback.append("Mention specific projects or experiences to highlight your capabilities.")
    if not "github" in resume_text.lower():
        resume_feedback.append("Add a GitHub or portfolio link to demonstrate your work.")

    job_roles = {
        "web development": "Frontend Developer",
        "backend": "Backend Developer",
        "database": "Database Engineer",
        "cloud": "Cloud Engineer",
        "nlp": "NLP Engineer",
        "ai": "AI Engineer",
        "testing": "QA/Test Engineer",
        "sql": "SQL Analyst",
        "python": "Python Developer",
        "spring boot": "Java Backend Developer"
    }

    recommended_jobs = list({job_roles.get(skill_or_topic) for skill_or_topic in matched.union(core_topics) if job_roles.get(skill_or_topic)})

    return jsonify({
        "match_score": score,
        "suggestions": suggestions,
        "interview_questions": questions,
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "core_topics": core_topics,
        "resume_preview": resume_text[:200] + "..." if len(resume_text) > 200 else resume_text,
        "jd_preview": job_description[:200] + "..." if len(job_description) > 200 else job_description,
        "preparation_plan": preparation_plan,
        "resume_feedback": resume_feedback,
        "recommended_jobs": recommended_jobs
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
