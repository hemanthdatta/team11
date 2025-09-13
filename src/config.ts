// src/config.ts
// This file contains environment-specific configuration

// Determine the API base URL based on the environment
export const getApiBaseUrl = (): string => {
  // When running on Vercel (production)
  if (window.location.hostname !== 'localhost' && 
      window.location.hostname !== '127.0.0.1' && 
      window.location.hostname !== '0.0.0.0') {
    // For the simplified API that doesn't use the /api prefix for endpoints
    return '';
  }
  
  // Local development
  return 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();
