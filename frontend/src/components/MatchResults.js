// File: frontend/src/components/MatchResults.js
import React, { useEffect, useState } from "react";

export default function MatchResults() {
  const [score, setScore] = useState(null);
  const [suggestions, setSuggestions] = useState("");

  useEffect(() => {
    // Retrieve from localStorage
    const storedScore = localStorage.getItem("matchScore");
    const storedSuggestions = localStorage.getItem("matchSuggestions");
    if (storedScore) {
      setScore(storedScore);
    }
    if (storedSuggestions) {
      setSuggestions(storedSuggestions);
    }
  }, []);

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg text-center">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Matching Results</h2>
      {score ? (
        <div>
          <p className="text-lg font-semibold">Match Score: {score}%</p>
          <p className="mt-2 text-gray-700">{suggestions}</p>
        </div>
      ) : (
        <p>No results available. Please upload a resume and job description first.</p>
      )}
    </div>
  );
}
