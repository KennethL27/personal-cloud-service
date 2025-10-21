import React from 'react';

interface ErrorDisplayProps {
  error: string | null;
  onRetry: () => void;
}

export function ErrorDisplay({ error, onRetry }: ErrorDisplayProps) {
  if (!error) return null;

  return (
    <div className="bg-red-900 border border-red-700 text-red-100 px-4 py-3 rounded">
      <div className="flex justify-between items-center">
        <span>{error}</span>
        <button
          onClick={onRetry}
          className="ml-4 px-3 py-1 bg-red-700 text-white rounded hover:bg-red-600 transition-colors"
        >
          Retry
        </button>
      </div>
    </div>
  );
}