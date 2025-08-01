// File: frontend/src/components/UploadResume.js

import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function UploadResume() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [uploadMessage, setUploadMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleJobDescChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadMessage("Please select a resume file!");
      return;
    }
    if (!jobDescription.trim()) {
      setUploadMessage("Please enter a job description!");
      return;
    }

    setUploadMessage("");
    setLoading(true);

    try {
      // Step 1: Upload resume
      const formData = new FormData();
      formData.append("file", file);

      const uploadResponse = await axios.post("http://127.0.0.1:5000/upload_resume", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const filepath = uploadResponse.data.filepath;

      // Step 2: Parse resume
      const parseResponse = await axios.post(
        "http://127.0.0.1:5000/parse_resume",
        { filepath },
        { headers: { "Content-Type": "application/json" } }
      );
      const resumeText = parseResponse.data.text;

      setUploadMessage("Analyzing resume...");
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Step 3: Analyze
      const analyzeResponse = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription,
        }),
      });

      if (!analyzeResponse.ok) {
        throw new Error("Network response was not ok");
      }

      const analyzeData = await analyzeResponse.json();
      console.log("Analyze data:", analyzeData); // Optional debug log

      localStorage.setItem("analyzeResults", JSON.stringify(analyzeData));
      navigate("/results");

      setUploadMessage("Analysis complete! Visit the Results page.");
    } catch (error) {
      setUploadMessage("Error uploading or processing resume!");
      console.error("Upload Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        Upload Your Resume & Enter Job Description
      </h2>
      <div className="mb-4">
        <input type="file" onChange={handleFileChange} className="w-full p-2 border rounded" />
      </div>
      <div className="mb-4">
        <textarea
          value={jobDescription}
          onChange={handleJobDescChange}
          placeholder="Enter the job description here..."
          rows="4"
          className="w-full p-2 border rounded"
        ></textarea>
      </div>
      <button
        onClick={handleUpload}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition-colors"
        disabled={loading}
      >
        {loading ? (
          <div className="flex items-center justify-center">
            <svg className="animate-spin h-5 w-5 mr-3 text-white" viewBox="0 0 24 24">
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8H4z"
              ></path>
            </svg>
            Analyzing...
          </div>
        ) : (
          "Submit"
        )}
      </button>
      {uploadMessage && (
        <p className="mt-4 text-center text-sm text-gray-600">{uploadMessage}</p>
      )}
    </div>
  );
}