import { useState } from 'react';
import apiClient from '../client';

export const useFileDownload = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const downloadFile = async (fileName: string) => {
    try {
      setLoading(true);
      setError(null);
      
      const blob = await apiClient.streamFile(fileName);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      return blob;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred during download';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setError(null);
    setLoading(false);
  };

  return {
    loading,
    error,
    downloadFile,
    reset,
  };
};
