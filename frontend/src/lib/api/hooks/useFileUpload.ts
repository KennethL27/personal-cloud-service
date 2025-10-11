import { useState } from 'react';
import { UploadResponse } from '../types';
import apiClient from '../client';

export const useFileUpload = () => {
  const [data, setData] = useState<UploadResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const uploadFiles = async (files: File[]) => {
    try {
      setLoading(true);
      setError(null);
      setData(null);
      
      const response = await apiClient.uploadFiles(files);
      setData(response);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred during upload';
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
    uploadFiles,
    reset,
  };
};
