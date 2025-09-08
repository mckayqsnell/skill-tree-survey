import axios, { AxiosInstance, AxiosError } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const ADMIN_PASSWORD = import.meta.env.VITE_ADMIN_PASSWORD || 'admin123';

// Logger utility
export const logger = {
  info: (message: string, data?: any) => {
    if (import.meta.env.DEV) {
      console.log(`[INFO] ${message}`, data || '');
    }
  },
  error: (message: string, error?: any) => {
    console.error(`[ERROR] ${message}`, error || '');
  },
  warn: (message: string, data?: any) => {
    console.warn(`[WARN] ${message}`, data || '');
  },
  debug: (message: string, data?: any) => {
    if (import.meta.env.DEV) {
      console.debug(`[DEBUG] ${message}`, data || '');
    }
  },
};

// Error class for API errors
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Create axios instance with default config
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
});

// Admin client with auth header (password set dynamically)
export const adminClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    // Password will be set dynamically when admin authenticates
  },
  timeout: 10000,
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    logger.debug(`API Request: ${config.method?.toUpperCase()} ${config.url}`, {
      params: config.params,
      data: config.data,
    });
    return config;
  },
  (error) => {
    logger.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

adminClient.interceptors.request.use(
  (config) => {
    logger.debug(`Admin API Request: ${config.method?.toUpperCase()} ${config.url}`, {
      params: config.params,
      data: config.data,
    });
    return config;
  },
  (error) => {
    logger.error('Admin request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
const handleResponseError = (error: AxiosError) => {
  if (error.response) {
    const { status, data } = error.response;
    const message = (data as any)?.detail || (data as any)?.message || 'An error occurred';
    
    logger.error(`API Error ${status}: ${message}`, {
      url: error.config?.url,
      method: error.config?.method,
      data: error.response.data,
    });
    
    switch (status) {
      case 400:
        throw new ApiError(status, 'Bad Request: ' + message, data);
      case 401:
        throw new ApiError(status, 'Authentication Failed', data);
      case 403:
        throw new ApiError(status, 'Access Forbidden', data);
      case 404:
        throw new ApiError(status, 'Resource Not Found', data);
      case 422:
        throw new ApiError(status, 'Validation Error: ' + message, data);
      case 500:
        throw new ApiError(status, 'Server Error: ' + message, data);
      default:
        throw new ApiError(status, message, data);
    }
  } else if (error.request) {
    logger.error('No response received from server', error.request);
    throw new ApiError(0, 'No response from server. Please check your connection.');
  } else {
    logger.error('Request setup error', error.message);
    throw new ApiError(0, 'Request failed: ' + error.message);
  }
};

apiClient.interceptors.response.use(
  (response) => {
    logger.debug(`API Response: ${response.status}`, {
      url: response.config.url,
      data: response.data,
    });
    return response;
  },
  handleResponseError
);

adminClient.interceptors.response.use(
  (response) => {
    logger.debug(`Admin API Response: ${response.status}`, {
      url: response.config.url,
      data: response.data,
    });
    return response;
  },
  handleResponseError
);