# File: backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

# Import custom modules using relative imports
from routes.job_matcher import match_resumes_to_jobs, calculate_match_score
from parsers.text_extractor import extract_text_from_pdf, extract_text_from_docx
from utils.preprocess import clean_text

# Configuration
UPLOAD_FOLDER = "backend/uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def home():
    """Home route to verify API is running."""
    return jsonify({"message": "Resume Analyzer API is running!"})

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    """Handle resume file upload and return the saved file path."""
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
    """
    Parse the uploaded resume.
    Expects a JSON payload: { "filepath": "backend/uploads/your_resume.pdf" }
    Returns cleaned text and placeholder entity information.
    """
    data = request.json
    filepath = data.get("filepath")

    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "Invalid or missing file path"}), 400

    if filepath.lower().endswith(".pdf"):
        text = extract_text_from_pdf(filepath)
    elif filepath.lower().endswith(".docx"):
        text = extract_text_from_docx(filepath)
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

    # Placeholder for entity extraction (can be enhanced later)
    entities = {
        "name": None,
        "email": None,
        "phone": None,
        "skills": []
    }

    return jsonify({"text": text_cleaned, "entities": entities}), 200

@app.route("/match_resume", methods=["POST"])
def match_resume():
    """
    Match a resume with a job description using semantic similarity (BERT-based embeddings).
    Expects a JSON payload:
      { "resume_text": "extracted resume text", "job_description": "job description text" }
    Returns a match score percentage.
    """
    data = request.json
    resume_text = data.get("resume_text", "")
    job_description = data.get("job_description", "")

    if not resume_text or not job_description:
        return jsonify({"error": "Both resume_text and job_description are required"}), 400

    score = calculate_match_score(resume_text, job_description)
    return jsonify({"match_score": score}), 200

if __name__ == "__main__":
    app.run(debug=True)
