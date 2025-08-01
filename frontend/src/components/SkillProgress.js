import React from "react";

export default function SkillProgress({ matched = [], missing = [] }) {
  const total = matched.length + missing.length;

  const getProgress = (skill) => {
    return matched.includes(skill) ? 100 : 0;
  };

  const renderBar = (skill, progress) => (
    <div key={skill} className="mb-3">
      <p className="text-sm text-gray-800 font-medium mb-1 capitalize">🛠️ {skill}</p>
      <div className="w-full bg-gray-200 h-3 rounded overflow-hidden">
        <div
          className={`h-3 rounded transition-all duration-700 ease-in-out ${
            progress === 100 ? "bg-green-500" : "bg-yellow-400"
          }`}
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
  );

  return (
    <div className="mt-6 text-left">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">🎯 Skill Progress</h3>
      <div className="bg-white p-4 rounded-lg shadow">
        {matched.concat(missing).map((skill) =>
          renderBar(skill, getProgress(skill))
        )}
      </div>

      <div className="mt-4 text-green-700 font-semibold">
        ✅ Skills Mastered: {matched.length} / {total}
      </div>

      {matched.length === total && total > 0 && (
        <div className="mt-2 text-blue-600 font-bold text-sm">
          🏅 You’ve mastered all required skills for this role. Excellent job!
        </div>
      )}
    </div>
  );
}
