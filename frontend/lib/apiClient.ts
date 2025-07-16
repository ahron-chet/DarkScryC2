import axios from 'axios';
import { getAccessToken, getRefreshToken, setTokens, clearTokens } from './authClient';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_MANAGEMENT_API_URL,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token && config.headers) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refresh = getRefreshToken();
      if (refresh) {
        try {
          const res = await axios.post(
            `${process.env.NEXT_PUBLIC_MANAGEMENT_API_URL}/auth/refresh`,
            { refresh_token: refresh }
          );
          setTokens(res.data.access_token, res.data.refresh_token);
          originalRequest.headers['Authorization'] = `Bearer ${res.data.access_token}`;
          return api(originalRequest);
        } catch (_) {
          clearTokens();
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;
