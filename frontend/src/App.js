import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import UploadResume from "./components/UploadResume";
import MatchResults from "./components/MatchResults";
import "./index.css";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-blue-700 p-4 text-white flex justify-between items-center">
          <h1 className="text-2xl font-bold">Resume Analyzer</h1>
          <div>
            <Link to="/" className="px-3 hover:underline">Home</Link>
            <Link to="/upload" className="px-3 hover:underline">Upload Resume</Link>
            <Link to="/results" className="px-3 hover:underline">Results</Link>
          </div>
        </nav>
        <div className="p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<UploadResume />} />
            <Route path="/results" element={<MatchResults />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
