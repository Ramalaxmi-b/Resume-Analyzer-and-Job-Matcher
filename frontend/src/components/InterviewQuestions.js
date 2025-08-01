import React from "react";

export default function InterviewQuestions({ questions }) {
  const renderQuestions = (title, list) => (
    <div className="mb-4">
      <h3 className="text-lg font-semibold text-blue-700 mb-2">{title}</h3>
      {list && list.length > 0 ? (
        <ul className="list-disc list-inside text-left">
          {list.map((q, i) => (
            <li key={i} className="mb-1">{q}</li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500">No questions generated.</p>
      )}
    </div>
  );

  return (
    <div className="mt-6">
      <h2 className="text-xl font-bold text-gray-800 mb-2">Interview Questions</h2>
      {renderQuestions("Technical", questions.technical)}
      {renderQuestions("Non-Technical", questions.nonTechnical)}
      {renderQuestions("Core Domain", questions.core)}
    </div>
  );
}