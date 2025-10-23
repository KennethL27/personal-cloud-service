import React from 'react';

interface BannerProps {
  message: string;
  type: 'success' | 'error';
  onClose: () => void;
}

export function Banner({ message, type, onClose }: BannerProps) {
  const bgColor = type === 'success' ? 'bg-green-600' : 'bg-red-600';
  const textColor = 'text-white';
  
  return (
    <div className={`${bgColor} ${textColor} px-4 py-3 rounded-lg shadow flex justify-between items-center`}>
      <span>{message}</span>
      <button
        onClick={onClose}
        className="ml-4 text-white hover:text-gray-200 focus:outline-none"
      >
        ✕
      </button>
    </div>
  );
}
