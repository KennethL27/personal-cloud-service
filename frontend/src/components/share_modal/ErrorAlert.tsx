import React from 'react';

interface ErrorAlertProps {
  error: string | null;
}

export function ErrorAlert({ error }: ErrorAlertProps) {
  if (!error) return null;

  return (
    <div className="mb-4 bg-red-900 border border-red-700 text-red-100 px-4 py-3 rounded">
      {error}
    </div>
  );
}
