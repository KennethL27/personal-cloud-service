import React from 'react';

type ViewMode = 'view' | 'edit';

interface SharingSectionProps {
  mode: ViewMode;
}

export function SharingSection({ mode }: SharingSectionProps) {
  return (
    <div className="bg-gray-500 rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Sharing Options</h2>
      <div className="space-y-4">
        <div className="flex items-center">
          <input
            type="checkbox"
            id="allowSharing"
            className="mr-3 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            disabled={mode === 'view'}
          />
          <label htmlFor="allowSharing" className="text-sm font-medium">
            Allow file sharing with other users
          </label>
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="publicAccess"
            className="mr-3 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            disabled={mode === 'view'}
          />
          <label htmlFor="publicAccess" className="text-sm font-medium">
            Enable public access links
          </label>
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="requireAuth"
            className="mr-3 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            disabled={mode === 'view'}
          />
          <label htmlFor="requireAuth" className="text-sm font-medium">
            Require authentication for all access
          </label>
        </div>
      </div>
      {mode === 'view' && (
        <p className="text-xs text-gray-400 mt-4">
          Sharing options can only be modified by administrators
        </p>
      )}
    </div>
  );
}
