import React from "react";

export default function PreparationPlan({ plan }) {
  if (!plan || plan.length === 0) return null;
  return (
    <div className="mt-6">
      <h2 className="text-xl font-bold text-green-800 mb-2">Personalized Preparation Plan</h2>
      <ul className="list-disc list-inside text-left">
        {plan.map((item, i) => (
          <li key={i} className="mb-1">
            <span className="font-semibold">{item.topic}:</span>{" "}
            <a href={item.link} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
              {item.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}