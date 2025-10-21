import React from 'react';

export function LoadingSpinner() {
  return (
    <div className="min-h-screen bg-gray-800 flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-white mx-auto mb-4"></div>
        <p className="text-white text-lg">Loading settings...</p>
      </div>
    </div>
  );
}