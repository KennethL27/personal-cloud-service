import { ApiConfig, ErrorResponse, BrowseResponse, LoginRequest, LoginResponse, LogoutResponse, VerifyResponse, UserSettingsResponse, UserSettings, MountedDrivesResponse, FolderItem } from './types';
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
      credentials: 'include', // Include cookies for authentication
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
  async uploadFiles(files: File[], currentFilePath : string) {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    formData.append('file_path_location', currentFilePath);

    const url = getApiUrl(API_CONFIG.endpoints.upload);
    
    try {
          const response = await fetch(url, {
      method: 'POST',
      body: formData,
      credentials: 'include',
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
        credentials: 'include',
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

  // File Browse
  async browseFiles(category?: string): Promise<BrowseResponse> {
    const url = new URL(getApiUrl(API_CONFIG.endpoints.browse));
    
    if (category) {
      url.searchParams.append('category', category);
    }
    
    try {
      const response = await fetch(url.toString(), {
        method: 'GET',
        credentials: 'include',
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
      throw new Error('An unexpected error occurred during file browsing');
    }
  }

  // Authentication Methods
  async login(request: LoginRequest): Promise<LoginResponse> {
    return this.request<LoginResponse>(API_CONFIG.endpoints.login, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async logout(): Promise<LogoutResponse> {
    return this.request<LogoutResponse>(API_CONFIG.endpoints.logout, {
      method: 'POST',
    });
  }

  async verifyAuth(): Promise<VerifyResponse> {
    return this.request<VerifyResponse>(API_CONFIG.endpoints.verify, {
      method: 'GET',
    });
  }

  // User Settings Methods
  async getUserSettings(): Promise<UserSettingsResponse> {
    return this.request<UserSettingsResponse>('/file/user_settings/', {
      method: 'GET',
    });
  }

  async updateUserSettings(settings: UserSettings): Promise<{ status: string }> {
    return this.request<{ status: string }>('/file/user_settings/', {
      method: 'PUT',
      body: JSON.stringify(settings),
    });
  }

  async getMountedDrives(): Promise<MountedDrivesResponse> {
    return this.request<MountedDrivesResponse>('/file/list_mounted_drives/', {
      method: 'GET',
    });
  }

  // List Folder Items
  async listFolderItems(path: string = ""): Promise<FolderItem[]> {
    const params = new URLSearchParams();
    if (path) {
      params.append('path', path);
    }
    
    const url = `${getApiUrl(API_CONFIG.endpoints.listFolderItems)}?${params.toString()}`;
    
    try {
      const response = await fetch(url, {
        method: 'GET',
        credentials: 'include',
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
      throw new Error('An unexpected error occurred while listing folder items');
    }
  }
}

// Create and export default instance
export const apiClient = new ApiClient({
  baseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
});

export default apiClient;
