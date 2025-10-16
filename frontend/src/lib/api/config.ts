export const API_CONFIG = {
  baseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  timeout: parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '10000'),
  endpoints: {
    health: '/health_check/',
    upload: '/file/upload/',
    stream: '/file/stream/',
    browse: '/file/browse/',
    login: '/auth/login/',
    logout: '/auth/logout/',
    verify: '/auth/verify/',
  },
} as const;

export const getApiUrl = (endpoint: string) => `${API_CONFIG.baseUrl}${endpoint}`;
