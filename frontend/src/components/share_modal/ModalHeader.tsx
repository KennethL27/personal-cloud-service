import React from 'react';

interface ModalHeaderProps {
  showSuccess: boolean;
  onClose: () => void;
}

export function ModalHeader({ showSuccess, onClose }: ModalHeaderProps) {
  return (
    <div className="flex justify-between items-center mb-6">
      <h2 className="text-xl font-semibold">
        {showSuccess ? 'Share Successful' : 'Share Folder'}
      </h2>
      <button
        onClick={onClose}
        className="text-gray-300 hover:text-white text-2xl leading-none"
      >
        ×
      </button>
    </div>
  );
}
