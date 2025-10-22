import React from 'react';

interface ErrorMessageProps {
  message: string;
}

export function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <div className="bg-red-500 rounded-lg shadow p-6">
      <p className="text-red-100">Error: {message}</p>
    </div>
  );
}