import api from './apiClient';
export const getAccessToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('accessToken');
};

export const getRefreshToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('refreshToken');
};

export const setTokens = (access: string, refresh: string) => {
  if (typeof window === 'undefined') return;
  localStorage.setItem('accessToken', access);
  localStorage.setItem('refreshToken', refresh);
};

export const clearTokens = () => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
};

export const logout = () => {
  clearTokens();
  if (typeof window !== 'undefined') {
    window.location.href = '/login';
  }
};

export const ensureValidTokens = async (): Promise<boolean> => {
  const access = getAccessToken();
  if (access) return true;

  const refresh = getRefreshToken();
  if (refresh) {
    try {
      const res = await api.post<{ access_token: string; refresh_token: string }>('/auth/refresh', { refresh_token: refresh });
      setTokens(res.data.access_token, res.data.refresh_token);
      return true;
    } catch {
      clearTokens();
    }
  }

  return false;
};
