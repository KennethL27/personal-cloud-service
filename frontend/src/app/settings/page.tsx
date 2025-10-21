'use client';

import React, { useState, useEffect } from 'react';
import { useAuthContext } from '@/contexts/AuthContext';
import { useUserSettings } from '@/lib/api/hooks/useUserSettings';
import { SettingsHeader } from '@/components/settings/SettingsHeader';
import { ErrorDisplay } from '@/components/settings/ErrorDisplay';
import { AccountSection } from '@/components/settings/AccountSection';
import { StorageSection } from '@/components/settings/StorageSection';
import { SharingSection } from '@/components/settings/SharingSection';
import { SettingsInfo } from '@/components/settings/SettingsInfo';
import { LoadingSpinner } from '@/components/settings/LoadingSpinner';

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
  });
  const [saveLoading, setSaveLoading] = useState(false);

  useEffect(() => {
    fetchSettings();
    fetchMountedDrives();
  }, []);

  useEffect(() => {
    if (settings) {
      setFormData({
        hard_drive_path_selection: settings.hard_drive_path_selection,
      });
    }
  }, [settings]);

  const handleEdit = () => setMode('edit');

  const handleCancel = () => {
    setMode('view');
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

  const handlePathChange = (value: string) => {
    setFormData(prev => ({
      ...prev,
      hard_drive_path_selection: value,
    }));
  };

  const handleRetry = () => {
    fetchSettings();
    fetchMountedDrives();
  };

  if (settingsLoading || drivesLoading) {
    return <LoadingSpinner />;
  }

  const error = settingsError || drivesError;

  return (
    <div className="min-h-screen bg-gray-800">
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto space-y-6">
          <SettingsHeader
            mode={mode}
            onEdit={handleEdit}
            onCancel={handleCancel}
            onSave={handleSave}
            saveLoading={saveLoading}
          />

          <ErrorDisplay error={error} onRetry={handleRetry} />

          <AccountSection user={user} mode={mode} />

          <StorageSection
            mode={mode}
            currentPath={settings?.hard_drive_path_selection || ''}
            selectedPath={formData.hard_drive_path_selection}
            drives={drives}
            onPathChange={handlePathChange}
          />

          <SharingSection mode={mode} />

          {settings && (
            <SettingsInfo
              createdAt={settings.created_at}
              updatedAt={settings.updated_at}
            />
          )}
        </div>
      </div>
    </div>
  );
}