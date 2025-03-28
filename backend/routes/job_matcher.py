# File: backend/routes/job_matcher.py

from sentence_transformers import SentenceTransformer, util
from utils.preprocess import clean_text

# Load the SentenceTransformer model once at startup
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_match_score(resume_text, job_description):
    """
    Calculate semantic match score between resume and job description using Sentence Transformers.
    Returns the score as a percentage.
    """
    # Clean texts (optional if already cleaned)
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)
    
    # Encode the texts to obtain embeddings
    embeddings = model.encode([resume_text, job_description], convert_to_tensor=True)
    cosine_sim = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    # cosine_sim is a tensor; convert it to a float percentage
    return round(float(cosine_sim.item() * 100), 2)

def match_resumes_to_jobs(resume_text):
    """
    Matches the resume text against job descriptions stored in the data folder using semantic similarity.
    Returns the top 5 job matches with similarity scores.
    """
    JOB_DESCRIPTIONS_FOLDER = "backend/data/job_description"
    job_descriptions = {}

    # Load job descriptions from text files
    try:
        for filename in os.listdir(JOB_DESCRIPTIONS_FOLDER):
            if filename.endswith(".txt"):
                filepath = f"{JOB_DESCRIPTIONS_FOLDER}/{filename}"
                with open(filepath, "r", encoding="utf-8") as f:
                    job_descriptions[filename] = clean_text(f.read())
    except Exception as e:
        print(f"Error loading job descriptions: {e}")
        return ["Error: Job descriptions folder not found."]

    if not job_descriptions:
        return ["No job descriptions found in data/job_description."]

    results = []
    # Calculate semantic similarity for each job description
    for job_file, job_text in job_descriptions.items():
        score = calculate_match_score(resume_text, job_text)
        results.append({"job": job_file, "score": score})
    
    # Sort by highest score and return top 5 matches
    results = sorted(results, key=lambda x: x["score"], reverse=True)[:5]
    return results
