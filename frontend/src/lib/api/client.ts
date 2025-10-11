import { ApiConfig, ErrorResponse } from './types';
import { API_CONFIG, getApiUrl } from './config';

class ApiClient {
  private config: ApiConfig;

  constructor(config: ApiConfig) {
    this.config = config;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.config.baseUrl}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      method: 'GET', // Explicitly set default method
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      mode: 'cors', // Explicitly set CORS mode
      credentials: 'same-origin', // Handle credentials properly
      ...options,
    };

    try {
      const response = await fetch(url, defaultOptions);
      
      if (!response.ok) {
        const errorData: ErrorResponse = await response.json().catch(() => ({
          status: 'error',
          message: `HTTP ${response.status}: ${response.statusText}`,
        }));
        
        throw new Error(errorData.message || `HTTP ${response.status}`);
      }

      // Handle empty responses
      if (response.status === 204 || response.headers.get('content-length') === '0') {
        return {} as T;
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred');
    }
  }

  // Health Check
  async healthCheck() {
    return this.request<{ status: string }>(API_CONFIG.endpoints.health, {
      method: 'GET',
    });
  }

  // File Upload
  async uploadFiles(files: File[]) {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    const url = getApiUrl(API_CONFIG.endpoints.upload);
    
    try {
          const response = await fetch(url, {
      method: 'POST',
      body: formData,
    });

      if (!response.ok) {
        const errorData: ErrorResponse = await response.json().catch(() => ({
          status: 'error',
          message: `HTTP ${response.status}: ${response.statusText}`,
        }));
        
        throw new Error(errorData.message || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred during file upload');
    }
  }

  // File Stream (for downloading)
  async streamFile(fileName: string): Promise<Blob> {
    const url = `${getApiUrl(API_CONFIG.endpoints.stream)}?file_name=${encodeURIComponent(fileName)}`;
    
    try {
      const response = await fetch(url, {
        method: 'GET',
      });
      
      if (!response.ok) {
        const errorData: ErrorResponse = await response.json().catch(() => ({
          status: 'error',
          message: `HTTP ${response.status}: ${response.statusText}`,
        }));
        
        throw new Error(errorData.message || `HTTP ${response.status}`);
      }

      return await response.blob();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred during file download');
    }
  }
}

// Create and export default instance
export const apiClient = new ApiClient({
  baseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
});

export default apiClient;
