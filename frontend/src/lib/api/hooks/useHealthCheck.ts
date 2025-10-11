import { useState, useEffect } from 'react';
import { HealthCheckResponse } from '../types';
import apiClient from '../client';

export const useHealthCheck = () => {
  const [data, setData] = useState<HealthCheckResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const checkHealth = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.healthCheck();
      setData(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return {
    data,
    loading,
    error,
    refetch: checkHealth,
  };
};
