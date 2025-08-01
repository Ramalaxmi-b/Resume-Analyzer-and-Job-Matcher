// frontend/src/components/ResumeFeedback.js
import React from "react";

export default function ResumeFeedback({ feedback }) {
  if (!feedback) return null;
  return (
    <div className="mt-6 text-left">
      <h2 className="text-xl font-bold text-red-600 mb-2">AI-Powered Resume Feedback</h2>
      <p className="text-gray-700">{feedback}</p>
    </div>
  );
}
