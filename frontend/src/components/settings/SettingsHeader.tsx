import React from 'react';

type ViewMode = 'view' | 'edit';

interface SettingsHeaderProps {
  mode: ViewMode;
  onEdit: () => void;
  onCancel: () => void;
  onSave: () => void;
  saveLoading: boolean;
}

export function SettingsHeader({ mode, onEdit, onCancel, onSave, saveLoading }: SettingsHeaderProps) {
  return (
    <div className="bg-gray-500 rounded-lg shadow p-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Settings</h1>
        {mode === 'view' ? (
          <button
            onClick={onEdit}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            Edit Settings
          </button>
        ) : (
          <div className="flex gap-2">
            <button
              onClick={onCancel}
              className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={onSave}
              disabled={saveLoading}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50 transition-colors"
            >
              {saveLoading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}