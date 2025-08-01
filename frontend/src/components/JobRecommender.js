// frontend/src/components/JobRecommender.js
import React from "react";

export default function JobRecommender({ roles }) {
  if (!roles.length) return null;
  return (
    <div className="mt-6 text-left">
      <h2 className="text-xl font-bold text-indigo-600 mb-2">Recommended Job Roles</h2>
      <ul className="list-disc list-inside text-gray-700">
        {roles.map((role, index) => (
          <li key={index}>{role}</li>
        ))}
      </ul>
    </div>
  );
}
