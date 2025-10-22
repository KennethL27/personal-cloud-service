import { useState } from 'react';
import { FolderItem } from '../types';
import apiClient from '../client';

export const useListFolderItems = () => {
  const [data, setData] = useState<FolderItem[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const listFolderItems = async (path: string = "") => {
    try {
      setLoading(true);
      setError(null);
      setData(null);
      
      const response = await apiClient.listFolderItems(path);
      setData(response);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred while listing folder items';
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
    listFolderItems,
    reset,
  };
};
