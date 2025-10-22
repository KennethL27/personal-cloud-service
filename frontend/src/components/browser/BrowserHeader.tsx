import React from 'react';

interface BrowserHeaderProps {
  currentPath: string;
  pathDisplay: string;
  itemCount: number;
  onBack: () => void;
}

export function BrowserHeader({ 
  currentPath, 
  pathDisplay, 
  itemCount, 
  onBack 
}: BrowserHeaderProps) {
  return (
    <div className="bg-gray-500 rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          {currentPath && (
            <button
              onClick={onBack}
              className="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors"
            >
              ← Back
            </button>
          )}
          <h2 className="text-xl font-semibold">
            {pathDisplay}
          </h2>
        </div>
        
        <div className="text-sm text-gray-300">
          {itemCount} item{itemCount !== 1 ? 's' : ''}
        </div>
      </div>
    </div>
  );
}