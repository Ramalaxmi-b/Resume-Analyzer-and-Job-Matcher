# Resume Analyzer & Job Matcher

Hi! 👋
This is a project I built to help job seekers get instant feedback on their resumes and see how well they match with job descriptions. It uses machine learning and natural language processing to extract skills, compare resumes with job descriptions, suggest improvements, and even recommend roles.

---

## 🔍 What It Does

* **Resume Parsing:** Upload your resume (PDF or DOCX) and the app will extract your details like skills and experience.
* **Job Description Matching:** Paste a job description, and it’ll compare it with your resume to calculate a match percentage.
* **Skill Suggestions:** Highlights which skills you're missing based on the JD.
* **Interview Questions:** Generates relevant technical and non-technical questions based on matched skills.
* **Preparation Plan:** Gives you a learning path to improve missing skills.
* **AI Resume Feedback:** Suggests improvements to make your resume better.
* **Job Role Recommendations:** Based on your resume, it suggests possible roles you might fit into.
* **Gamified Skill Tracker:** A fun progress bar to visualize which skills you already have and what you’re missing.

---

## 🧠 Tech Stack

**Frontend:**

* React.js
* TailwindCSS

**Backend:**

* Flask (Python)
* REST APIs
* CORS enabled
* File parsing (PDF/DOCX)

**ML/NLP:**

* BERT-based sentence embeddings for similarity
* Custom skill/topic extractors
* Resume cleaning and preprocessing

---

## 📁 Folder Structure

```
resume-analyzer-job-matcher/
│
├── backend/
│   ├── app.py                # Main Flask app
│   ├── routes/               # Endpoints for match score, upload, etc.
│   ├── parsers/              # File extractors for PDF and DOCX
│   └── utils/                # Skill and text processing logic
│
└── frontend/
    └── src/
        ├── components/       # React components
        ├── App.js            # Main app
        └── index.js          # Entry point
```

---

## 🛠 How to Run Locally

### 📦 Clone the project

```bash
git clone https://github.com/Ramalaxmi-b/Resume-Analyzer-and-Job-Matcher.git
cd Resume-Analyzer-and-Job-Matcher
```

### ▶️ Backend (Flask)

```bash
cd backend
python -m venv env
source env/bin/activate      # Windows: env\Scripts\activate
pip install -r requirements.txt
flask run
```

### 💻 Frontend (React)

```bash
cd frontend
npm install
npm start
```

---

## ✨ Why I Built This

I wanted to create something practical and helpful for job seekers, especially freshers like me. It’s a way to apply everything I’ve been learning—from backend APIs and ML to frontend React design.

---

## 📬 Contact

Have feedback or questions?

* 📧 Email: [ramalaxmib671@gmail.com](mailto:ramalaxmib671@gmail.com)
* 🌐 GitHub: [@Ramalaxmi-b](https://github.com/Ramalaxmi-b)

---

