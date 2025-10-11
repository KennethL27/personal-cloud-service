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
