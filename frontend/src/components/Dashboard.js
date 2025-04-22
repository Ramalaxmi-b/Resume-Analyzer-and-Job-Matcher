import React from "react";
import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-50 to-purple-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-500 text-white py-6 shadow-md rounded-b-2xl">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold">Resume Analyzer & Optimizer</h1>
          <p className="mt-2 text-lg">
            Enhance your resume and discover how well it matches your dream job!
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-10">
        {/* Hero Section */}
        <section className="mb-12 text-center">
          <h2 className="text-3xl font-extrabold text-gray-800">
            Welcome to Resume Analyzer
          </h2>
          <p className="mt-4 text-xl text-gray-600 max-w-xl mx-auto">
            Our application leverages advanced NLP techniques to analyze and optimize your resume. 
            Get actionable insights to stand out and secure your ideal job.
          </p>
          <img
            src={`${process.env.PUBLIC_URL}/search.png`}  // Reference the image in the public folder
            alt="Job Search Illustration"
            className="mx-auto mt-6 w-64 h-auto rounded-lg shadow-xl hover:scale-105 transition-transform duration-300"
          />
        </section>

        {/* Optimize Resume Section */}
        <section className="bg-white rounded-lg shadow-lg p-6 mb-12">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Optimize Your Resume</h2>
          <p className="text-gray-600 mb-6">
            Upload your resume and enter the job description to receive personalized feedback on how to optimize your resume. Our advanced analysis will show you the match percentage and recommendations to improve your chances.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link
              to="/upload"
              className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white font-semibold rounded-lg shadow-md hover:from-purple-600 hover:to-pink-500 transition-all duration-300"
            >
              Upload Resume
            </Link>
            <Link
              to="/results"
              className="px-6 py-3 bg-gradient-to-r from-green-400 to-teal-500 text-white font-semibold rounded-lg shadow-md hover:from-green-500 hover:to-emerald-600 transition-all duration-300"
            >
              View Results
            </Link>
          </div>
        </section>

        {/* Why Optimize Section */}
        <section className="text-center">
          <h2 className="text-2xl font-bold text-gray-800">Why Optimize Your Resume?</h2>
          <p className="mt-4 text-gray-600 max-w-2xl mx-auto">
            A well-optimized resume increases your chances of getting noticed by recruiters and leads to better job matches. 
            Our system provides insights and actionable recommendations, ensuring that your resume highlights the most relevant skills and experiences.
          </p>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-4">
        <div className="container mx-auto text-center">
          <p>&copy; {new Date().getFullYear()} Resume Analyzer. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
