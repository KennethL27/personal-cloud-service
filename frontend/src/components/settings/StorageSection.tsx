import React from 'react';

type ViewMode = 'view' | 'edit';

interface Drive {
  device: string;
  mountpoint: string;
  free: string;
}

interface StorageSectionProps {
  mode: ViewMode;
  currentPath: string;
  selectedPath: string;
  drives: Drive[];
  onPathChange: (path: string) => void;
}

export function StorageSection({ 
  mode, 
  currentPath, 
  selectedPath, 
  drives, 
  onPathChange 
}: StorageSectionProps) {
  return (
    <div className="bg-gray-500 rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Storage Settings</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            Hard Drive Path Selection
          </label>
          {mode === 'view' ? (
            <p className="text-gray-300">
              {currentPath || 'Not configured'}
            </p>
          ) : (
            <select
              value={selectedPath}
              onChange={(e) => onPathChange(e.target.value)}
              className="w-full px-3 py-2 bg-gray-700 text-white rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select a drive...</option>
              {drives.map((drive) => (
                <option key={drive.device} value={drive.mountpoint}>
                  {drive.device} - {drive.mountpoint} ({drive.free} free)
                </option>
              ))}
            </select>
          )}
        </div>
      </div>
    </div>
  );
}
