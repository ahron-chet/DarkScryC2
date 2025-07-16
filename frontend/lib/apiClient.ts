import axios from 'axios';
import { getAccessToken, getRefreshToken, setTokens, clearTokens } from './authClient';

const baseURL = (process.env.NEXT_PUBLIC_MANAGEMENT_API_URL || '').replace(/\/$/, '');

const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
});

const redirectToLogin = () => {
  if (typeof window !== 'undefined') {
    const cb = encodeURIComponent(window.location.pathname);
    window.location.href = `/login?callbackUrl=${cb}`;
  }
};

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
    const status = error.response?.status;
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refresh = getRefreshToken();
      if (refresh) {
        try {
          const res = await axios.post<{ access_token: string; refresh_token: string }>(
            `${baseURL}/auth/refresh`,
            { refresh_token: refresh }
          );
          setTokens(res.data.access_token, res.data.refresh_token);
          originalRequest.headers['Authorization'] = `Bearer ${res.data.access_token}`;
          return api(originalRequest);
        } catch {
          clearTokens();
          redirectToLogin();
        }
      } else {
        redirectToLogin();
      }
    } else if (status === 403) {
      redirectToLogin();
    }
    return Promise.reject(error);
  }
);

export default api;
