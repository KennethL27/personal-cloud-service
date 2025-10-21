import { useApiState } from './useApiState';
import { apiClient } from '../client';
import { UserSettings, UserSettingsResponse, MountedDrivesResponse, DriveInfo } from '../types';

export const useUserSettings = () => {
  const settingsState = useApiState<UserSettingsResponse>();
  const drivesState = useApiState<MountedDrivesResponse>();

  const fetchSettings = async () => {
    return settingsState.executeAsync(async () => {
      return await apiClient.getUserSettings();
    });
  };

  const updateSettings = async (settings: UserSettings) => {
    return settingsState.executeAsync(async () => {
      return await apiClient.updateUserSettings(settings);
    });
  };

  const fetchMountedDrives = async () => {
    return drivesState.executeAsync(async () => {
      return await apiClient.getMountedDrives();
    });
  };

  return {
    // Settings state
    settings: settingsState.data,
    settingsLoading: settingsState.loading,
    settingsError: settingsState.error,
    fetchSettings,
    updateSettings,
    
    // Drives state
    drives: drivesState.data || [],
    drivesLoading: drivesState.loading,
    drivesError: drivesState.error,
    fetchMountedDrives,
  };
};