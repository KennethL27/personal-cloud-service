import React from 'react';

interface SuccessMessageProps {
  pathDisplay: string;
  recipientName: string;
  onClose: () => void;
}

export function SuccessMessage({ pathDisplay, recipientName, onClose }: SuccessMessageProps) {
  return (
    <div className="text-center py-8">
      <div className="text-green-400 text-4xl mb-4">✓</div>
      <p className="text-white mb-6">
        Successfully shared <span className="font-semibold">&quot;{pathDisplay}&quot;</span> with {recipientName}
      </p>
      <button
        onClick={onClose}
        className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
      >
        Close
      </button>
    </div>
  );
}
