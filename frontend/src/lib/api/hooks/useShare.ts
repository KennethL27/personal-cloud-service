import { useApiState } from './useApiState';
import { apiClient } from '../client';
import { ShareFormRequest, ShareFormResponse } from '../types';

export const useShare = () => {
  const shareState = useApiState<ShareFormResponse>();

  const sharePath = async (shareData: ShareFormRequest) => {
    return shareState.executeAsync(async () => {
      return await apiClient.share(shareData);
    });
  };

  return {
    share: sharePath,
    loading: shareState.loading,
    error: shareState.error,
    data: shareState.data,
    reset: shareState.reset,
  };
};
