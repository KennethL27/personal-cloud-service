import { useState } from 'react';
import { BrowseResponse } from '../types';
import apiClient from '../client';

export const useFileBrowse = () => {
  const [data, setData] = useState<BrowseResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const browseFiles = async (category?: string) => {
    try {
      setLoading(true);
      setError(null);
      setData(null);
      
      const response = await apiClient.browseFiles(category);
      setData(response);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred during file browsing';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setData(null);
    setError(null);
    setLoading(false);
  };

  return {
    data,
    loading,
    error,
    browseFiles,
    reset,
  };
};
