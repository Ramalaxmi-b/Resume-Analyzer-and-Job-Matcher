// File: frontend/src/components/MatchResults.js
import React, { useEffect, useState } from "react";
import InterviewQuestions from "./InterviewQuestions";
import PreparationPlan from "./PreparationPlan";
import ResumeFeedback from "./ResumeFeedback";
import JobRecommender from "./JobRecommender";
import SkillProgress from "./SkillProgress";

export default function MatchResults() {
  const [score, setScore] = useState(null);
  const [suggestions, setSuggestions] = useState("");

  const [questions, setQuestions] = useState({
    technical: [],
    nonTechnical: [],
    core: [],
  });
  const [matchedSkills, setMatchedSkills] = useState([]);
  const [missingSkills, setMissingSkills] = useState([]);
  const [coreTopics, setCoreTopics] = useState([]);
  const [resumePreview, setResumePreview] = useState("");
  const [jdPreview, setJdPreview] = useState("");
  const [preparationPlan, setPreparationPlan] = useState([]);
  const [resumeFeedback, setResumeFeedback] = useState("");
  const [recommendedJobs, setRecommendedJobs] = useState([]);

  useEffect(() => {
    const data = JSON.parse(localStorage.getItem("analyzeResults") || "null");
    if (data) {
      setScore(data.match_score || null);
      setSuggestions(data.suggestions || "");
      setQuestions(data.interview_questions || { technical: [], nonTechnical: [], core: [] });
      setMatchedSkills(data.matched_skills || []);
      setMissingSkills(data.missing_skills || []);
      setCoreTopics(data.core_topics || []);
      setResumePreview(data.resume_preview || "");
      setJdPreview(data.jd_preview || "");
      setPreparationPlan(data.preparation_plan || []);
      setResumeFeedback(data.resume_feedback || "");
      setRecommendedJobs(data.recommended_jobs || []);

      const resultSection = document.getElementById("results-section");
      resultSection?.scrollIntoView({ behavior: "smooth" });
    }
  }, []);

  return (
    <div id="results-section" className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg text-center">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Matching Results</h2>
      {score !== null ? (
        <div>
          <p className="text-lg font-semibold">Match Score: {score}%</p>
          {score >= 80 && <p className="mt-1 text-green-600 font-medium">🏆 Great match! You're interview-ready!</p>}
          {score >= 50 && score < 80 && <p className="mt-1 text-yellow-600 font-medium">💪 Decent match! Strengthen missing skills.</p>}
          {score < 50 && <p className="mt-1 text-red-600 font-medium">📘 Keep learning! Review the preparation plan.</p>}
          <p className="mt-2 text-gray-700">{suggestions}</p>

          <div className="mt-4 flex flex-col md:flex-row gap-4 justify-center">
            <div className="w-full md:w-1/2 bg-gray-50 p-3 rounded">
              <h3 className="font-semibold text-gray-700 mb-1">Resume Preview</h3>
              <p className="text-xs text-gray-600">{resumePreview}</p>
            </div>
            <div className="w-full md:w-1/2 bg-gray-50 p-3 rounded">
              <h3 className="font-semibold text-gray-700 mb-1">JD Preview</h3>
              <p className="text-xs text-gray-600">{jdPreview}</p>
            </div>
          </div>

          <hr className="my-6 border-t border-gray-300" />
          <div className="flex flex-wrap justify-center gap-4">
            <div>
              <h4 className="font-semibold text-blue-700">Matched Skills</h4>
              <p className="text-sm">{matchedSkills.join(", ") || "None"}</p>
            </div>
            <div>
              <h4 className="font-semibold text-red-700">Missing Skills</h4>
              <p className="text-sm">{missingSkills.join(", ") || "None"}</p>
            </div>
            <div>
              <h4 className="font-semibold text-purple-700">Core Topics</h4>
              <p className="text-sm">{coreTopics.join(", ") || "None"}</p>
            </div>
          </div>

          <hr className="my-6 border-t border-gray-300" />
          <InterviewQuestions questions={questions} />

          <hr className="my-6 border-t border-gray-300" />
          <PreparationPlan plan={preparationPlan} />

          <hr className="my-6 border-t border-gray-300" />
          <ResumeFeedback feedback={resumeFeedback} />

          <hr className="my-6 border-t border-gray-300" />
          <JobRecommender roles={recommendedJobs} />

          <hr className="my-6 border-t border-gray-300" />
          <SkillProgress matched={matchedSkills} missing={missingSkills} />

          <button
            onClick={() => navigator.clipboard.writeText(JSON.stringify(localStorage.getItem("analyzeResults"), null, 2))}
            className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            📋 Copy Report JSON
          </button>
        </div>
      ) : (
        <p>No results available. Please upload a resume and job description first.</p>
      )}
    </div>
  );
}
