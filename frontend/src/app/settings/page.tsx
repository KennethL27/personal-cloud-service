'use client';

import React, { useState, useEffect } from 'react';
import { useAuthContext } from '@/contexts/AuthContext';
import { useUserSettings } from '@/lib/api/hooks/useUserSettings';

type ViewMode = 'view' | 'edit';

export default function Settings() {
  const { user } = useAuthContext();
  const { 
    settings, settingsLoading, settingsError, fetchSettings, updateSettings,
    drives, drivesLoading, drivesError, fetchMountedDrives 
  } = useUserSettings();
  
  const [mode, setMode] = useState<ViewMode>('view');
  const [formData, setFormData] = useState({
    hard_drive_path_selection: '',
    // Add other settings as needed
  });
  const [saveLoading, setSaveLoading] = useState(false);

  // Load data on component mount
  useEffect(() => {
    fetchSettings();
    fetchMountedDrives();
  }, []);

  // Update form data when settings are loaded
  useEffect(() => {
    if (settings) {
      setFormData({
        hard_drive_path_selection: settings.hard_drive_path_selection,
      });
    }
  }, [settings]);

  const handleEdit = () => {
    setMode('edit');
  };

  const handleCancel = () => {
    setMode('view');
    // Reset form data to current settings
    if (settings) {
      setFormData({
        hard_drive_path_selection: settings.hard_drive_path_selection,
      });
    }
  };

  const handleSave = async () => {
    try {
      setSaveLoading(true);
      await updateSettings(formData);
      setMode('view');
    } catch (error) {
      console.error('Failed to update settings:', error);
    } finally {
      setSaveLoading(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  if (settingsLoading || drivesLoading) {
    return (
      <div className="min-h-screen bg-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading settings...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-800">
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto space-y-6">
          {/* Header */}
          <div className="bg-gray-500 rounded-lg shadow p-6">
            <div className="flex justify-between items-center">
              <h1 className="text-3xl font-bold">Settings</h1>
              {mode === 'view' ? (
                <button
                  onClick={handleEdit}
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                >
                  Edit Settings
                </button>
              ) : (
                <div className="flex gap-2">
                  <button
                    onClick={handleCancel}
                    className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSave}
                    disabled={saveLoading}
                    className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50 transition-colors"
                  >
                    {saveLoading ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Error Display */}
          {(settingsError || drivesError) && (
            <div className="bg-red-900 border border-red-700 text-red-100 px-4 py-3 rounded">
              <div className="flex justify-between items-center">
                <span>{settingsError || drivesError}</span>
                <button
                  onClick={() => {
                    // Clear errors and retry
                    fetchSettings();
                    fetchMountedDrives();
                  }}
                  className="ml-4 px-3 py-1 bg-red-700 text-white rounded hover:bg-red-600 transition-colors"
                >
                  Retry
                </button>
              </div>
            </div>
          )}

          {/* Account Information Section */}
          <div className="bg-gray-500 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Account Information</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Name</label>
                {mode === 'view' ? (
                  <p className="text-gray-300">{user?.name || 'Not provided'}</p>
                ) : (
                  <input
                    type="text"
                    value={user?.name || ''}
                    disabled
                    className="w-full px-3 py-2 bg-gray-600 text-gray-300 rounded border border-gray-400"
                    placeholder="Name (read-only)"
                  />
                )}
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Email</label>
                <p className="text-gray-300">{user?.email}</p>
                <p className="text-xs text-gray-400 mt-1">Email cannot be changed</p>
              </div>
            </div>
          </div>

          {/* Path Selection Section */}
          <div className="bg-gray-500 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Storage Settings</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  Hard Drive Path Selection
                </label>
                {mode === 'view' ? (
                  <p className="text-gray-300">
                    {settings?.hard_drive_path_selection || 'Not configured'}
                  </p>
                ) : (
                  <select
                    value={formData.hard_drive_path_selection}
                    onChange={(e) => handleInputChange('hard_drive_path_selection', e.target.value)}
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

          {/* Sharing Options Section */}
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

          {/* Settings Info */}
          {settings && (
            <div className="bg-gray-500 rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-2">Settings Information</h3>
              <div className="text-sm text-gray-300 space-y-1">
                <p>Created: {new Date(settings.created_at).toLocaleString()}</p>
                <p>Last Updated: {new Date(settings.updated_at).toLocaleString()}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
  