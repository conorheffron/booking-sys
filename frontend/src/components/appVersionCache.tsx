// Utility for caching app version in localStorage with expiry

const VERSION_KEY = 'app_version_number';
const VERSION_EXPIRY_KEY = 'app_version_number_expiry';
const VERSION_API_URL = '/api/version/';

// CACHE TTL in milliseconds (e.g., 1 hours)
const CACHE_TTL = 60 * 60 * 1000; // 1 hours

/**
 * Get the cached app version from localStorage, if available and not expired.
 */
export function getCachedAppVersion(): string | null {
  const expiry = localStorage.getItem(VERSION_EXPIRY_KEY);
  if (expiry && Date.now() > Number(expiry)) {
    // Expired
    clearCachedAppVersion();
    return null;
  }
  return localStorage.getItem(VERSION_KEY);
}

/**
 * Set the app version in localStorage and update expiry.
 */
export function setCachedAppVersion(version: string) {
  localStorage.setItem(VERSION_KEY, version);
  localStorage.setItem(VERSION_EXPIRY_KEY, (Date.now() + CACHE_TTL).toString());
}

/**
 * Remove the cached app version (e.g., on logout or manual invalidation).
 */
export function clearCachedAppVersion() {
  localStorage.removeItem(VERSION_KEY);
  localStorage.removeItem(VERSION_EXPIRY_KEY);
}

/**
 * Fetch the app version from the API and cache it.
 */
export async function fetchAndCacheAppVersion(): Promise<string> {
  const res = await fetch(VERSION_API_URL);
  if (!res.ok) throw new Error('Failed to fetch version');
  const version = (await res.text()).trim();
  setCachedAppVersion(version);
  return version;
}

/**
 * Get the app version: first tries cache (with expiry), then falls back to fetching.
 */
export async function getAppVersion(): Promise<string> {
  const cached = getCachedAppVersion();
  if (cached) return cached;
  try {
    return await fetchAndCacheAppVersion();
  } catch {
    return 'unknown';
  }
}
