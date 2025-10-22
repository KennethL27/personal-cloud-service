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

export interface DriveInfo {
  device: string;
  mountpoint: string;
  fstype: string;
  opts: string;
  total: string;
  used: string;
  free: string;
  percent_used: string;
}

export interface UserSettings {
  hard_drive_path_selection: string;
}

export interface UserSettingsResponse {
  id: number;
  user_id: number;
  hard_drive_path_selection: string;
  created_at: string;
  updated_at: string;
}

export type MountedDrivesResponse = DriveInfo[];

export interface FolderItem {
  name: string;
  full_path: string;
  relative_path: string;
  type: "folder" | "file";
  size: string | null;
  modified: string;
}

export interface ListFolderResponse {
  items: FolderItem[];
}
