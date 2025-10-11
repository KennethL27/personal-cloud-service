import { useState } from 'react';
import apiClient from '../client';

export const useFileStream = () => {
  const [data, setData] = useState<{ blob: Blob; url: string; type: string; name: string } | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const streamFile = async (fileName: string) => {
    try {
      setLoading(true);
      setError(null);
      setData(null);
      
      const blob = await apiClient.streamFile(fileName);
      
      // Create object URL for the blob
      const url = URL.createObjectURL(blob);
      
      // Store blob data with metadata
      const fileData = {
        blob,
        url,
        type: blob.type || 'application/octet-stream',
        name: fileName
      };
      
      setData(fileData);
      
      return fileData;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred during file streaming';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    if (data?.url) {
      URL.revokeObjectURL(data.url); // Clean up object URL
    }
    setData(null);
    setError(null);
    setLoading(false);
  };

  return {
    data,
    loading,
    error,
    streamFile,
    reset,
  };
};
