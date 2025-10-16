// API Response Types
export interface HealthCheckResponse {
  status: string;
}

export interface UploadResponse {
  uploaded_files: string[];
}

export interface ErrorResponse {
  status: string;
  message: string;
}

export interface FileInfo {
  name: string;
  size?: number;
  type?: string;
  lastModified?: Date;
}

// API Client Configuration
export interface ApiConfig {
  baseUrl: string;
  timeout?: number;
}

// Request Types
export interface UploadFileRequest {
  files: File[];
}

export interface StreamFileRequest {
  fileName: string;
}

export interface FileMetadata {
  name: string;
  size: number;
  type: string;
  modified: string;
  category: string;
}

export interface BrowseResponse {
  files: FileMetadata[];
  total_count: number;
}

// Authentication Types
export interface User {
  email: string;
  name?: string;
  picture?: string;
  sub?: string;
}

export interface LoginRequest {
  token: string;
}

export interface LoginResponse {
  message: string;
  user: User;
}

export interface LogoutResponse {
  message: string;
}

export interface VerifyResponse {
  authenticated: boolean;
  user?: User;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}
