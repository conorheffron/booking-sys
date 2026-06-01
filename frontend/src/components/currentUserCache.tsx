// Utility for caching current logged-in user in sessionStorage

const USER_KEY = 'current_user';
const USER_API_URL = '/api/user/';

/**
 * Get the cached current user from sessionStorage, if available.
 */
export function getCachedCurrentUser(): string | null {
  return sessionStorage.getItem(USER_KEY);
}

/**
 * Set the current user in sessionStorage.
 */
export function setCachedCurrentUser(username: string) {
  sessionStorage.setItem(USER_KEY, username);
}

/**
 * Remove the cached current user (e.g., on logout).
 */
export function clearCachedCurrentUser() {
  sessionStorage.removeItem(USER_KEY);
}

/**
 * Fetch the current user from the API and cache it.
 */
export async function fetchAndCacheCurrentUser(): Promise<string> {
  const res = await fetch(USER_API_URL, { credentials: 'include' });
  if (!res.ok) throw new Error('Failed to fetch current user');
  const username = (await res.text()).trim();
  setCachedCurrentUser(username);
  return username;
}

/**
 * Get the current user: first tries sessionStorage cache, then falls back to fetching.
 */
export async function getCurrentUser(): Promise<string> {
  const cached = getCachedCurrentUser();
  if (cached) return cached;
  try {
    return await fetchAndCacheCurrentUser();
  } catch {
    return 'unknown';
  }
}
