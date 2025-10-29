import { useApiState } from './useApiState';
import { apiClient } from '../client';
import { AdminCheckResponse } from '../types';

export const useAdminCheck = () => {
    const adminCheckState = useApiState<AdminCheckResponse>();

    const adminCheckPath = async () => {
        return adminCheckState.executeAsync(async () => {
        return await apiClient.adminCheck();
        });
    };

    return {
        adminCheck: adminCheckPath,
        loading: adminCheckState.loading,
        error: adminCheckState.error,
        data: adminCheckState.data,
        reset: adminCheckState.reset,
    };
};