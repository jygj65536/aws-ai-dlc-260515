const TOKEN_KEY = 'auth_token';
const AUTH_INFO_KEY = 'auth_info';

export interface StoredAuthInfo {
  user_type: 'admin' | 'table';
  store_id: string;
  username?: string;
  table_id?: string;
  session_id?: string;
  table_number?: number;
}

export function saveToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(TOKEN_KEY, token);
}

export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function removeToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(TOKEN_KEY);
}

export function saveAuthInfo(info: StoredAuthInfo): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(AUTH_INFO_KEY, JSON.stringify(info));
}

export function getAuthInfo(): StoredAuthInfo | null {
  if (typeof window === 'undefined') return null;
  const raw = localStorage.getItem(AUTH_INFO_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function removeAuthInfo(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(AUTH_INFO_KEY);
}

export function clearAuth(): void {
  removeToken();
  removeAuthInfo();
}

export function isAuthenticated(): boolean {
  return getToken() !== null;
}
