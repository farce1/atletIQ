"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";

function IntegrationSuccessContent() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get("session_id");
  const [countdown, setCountdown] = useState(5);

  useEffect(() => {
    // Countdown timer
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          // Redirect back to chat or home page
          window.location.href = "/";
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-700 to-indigo-800 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 text-center">
        {/* Success Icon */}
        <div className="mx-auto w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-6">
          <svg
            className="w-12 h-12 text-green-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>

        {/* Success Message */}
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Authorization Successful!
        </h1>

        <p className="text-gray-600 mb-6">
          Your Apple Health data has been successfully connected to AtletIQ.
        </p>

        {/* Data Access Info */}
        <div className="bg-gray-50 rounded-lg p-4 mb-6 text-left">
          <h2 className="font-semibold text-gray-900 mb-3">
            We now have access to:
          </h2>
          <ul className="space-y-2">
            <li className="flex items-center text-gray-700">
              <span className="text-green-500 mr-2">✓</span>
              Workout data
            </li>
            <li className="flex items-center text-gray-700">
              <span className="text-green-500 mr-2">✓</span>
              Heart rate metrics
            </li>
            <li className="flex items-center text-gray-700">
              <span className="text-green-500 mr-2">✓</span>
              Active energy burned
            </li>
            <li className="flex items-center text-gray-700">
              <span className="text-green-500 mr-2">✓</span>
              Distance traveled
            </li>
          </ul>
        </div>

        {/* Session Info */}
        {sessionId && (
          <div className="text-sm text-gray-500 mb-4">
            Session ID: {sessionId}
          </div>
        )}

        {/* Redirect Message */}
        <div className="text-gray-600">
          Redirecting you back in <span className="font-bold text-purple-600">{countdown}</span> seconds...
        </div>

        {/* Manual Redirect Button */}
        <button
          onClick={() => window.location.href = "/"}
          className="mt-6 w-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-purple-700 hover:to-indigo-700 transition-all transform hover:scale-105"
        >
          Return Now
        </button>
      </div>
    </div>
  );
}

export default function IntegrationSuccess() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-700 to-indigo-800 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    }>
      <IntegrationSuccessContent />
    </Suspense>
  );
}
