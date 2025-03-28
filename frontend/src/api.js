import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000"; // Flask backend

// Upload Resume API Call
export const uploadResume = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await axios.post(`${API_BASE_URL}/upload_resume`, formData, {
            headers: { "Content-Type": "multipart/form-data" }
        });
        return response.data; // { message: "File uploaded successfully", filepath: "uploads/sample.pdf" }
    } catch (error) {
        console.error("Error uploading file:", error);
        throw error;
    }
};

// Parse Resume API Call
export const parseResume = async (filepath) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/parse_resume`, { filepath }, {
            headers: { "Content-Type": "application/json" }
        });
        return response.data; // { text: "Extracted Resume Content" }
    } catch (error) {
        console.error("Error parsing resume:", error);
        throw error;
    }
};

// Match Resume with Job Description API Call
export const matchResume = async (resumeText, jobDescription) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/match_resume`, {
            resume_text: resumeText,
            job_description: jobDescription
        }, {
            headers: { "Content-Type": "application/json" }
        });
        return response.data; // { match_score: 0.75 }
    } catch (error) {
        console.error("Error matching resume:", error);
        throw error;
    }
};
