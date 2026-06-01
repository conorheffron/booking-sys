import {
  getCurrentUser,
  getCachedCurrentUser,
  setCachedCurrentUser,
  clearCachedCurrentUser,
  fetchAndCacheCurrentUser,
} from '../currentUserCache';

describe('currentUserCache', () => {
  const USER_KEY = 'current_user';

  beforeEach(() => {
    sessionStorage.clear();
    jest.resetAllMocks();
  });

  afterEach(() => {
    sessionStorage.clear();
    jest.resetAllMocks();
  });

  it('returns cached user if available', () => {
    setCachedCurrentUser('test-user');
    expect(getCachedCurrentUser()).toBe('test-user');
  });

  it('returns null if no user cached', () => {
    expect(getCachedCurrentUser()).toBeNull();
  });

  it('clears cached user', () => {
    setCachedCurrentUser('test-user');
    clearCachedCurrentUser();
    expect(sessionStorage.getItem(USER_KEY)).toBeNull();
  });

  it('fetches and caches user from API', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      text: () => Promise.resolve('api-user'),
    } as any);

    const user = await fetchAndCacheCurrentUser();
    expect(user).toBe('api-user');
    expect(getCachedCurrentUser()).toBe('api-user');
    expect(global.fetch).toHaveBeenCalledWith('/api/user/', { credentials: 'include' });
  });

  it('throws if API returns non-ok response', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
    } as any);

    await expect(fetchAndCacheCurrentUser()).rejects.toThrow('Failed to fetch current user');
  });

  it('does not call API if cache is populated', async () => {
    setCachedCurrentUser('cached-user');
    global.fetch = jest.fn();
    const user = await getCurrentUser();
    expect(user).toBe('cached-user');
    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('calls API if cache is empty', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      text: () => Promise.resolve('fetched-user'),
    } as any);

    const user = await getCurrentUser();
    expect(user).toBe('fetched-user');
    expect(global.fetch).toHaveBeenCalled();
  });

  it('returns "unknown" if fetch fails', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('Network error'));
    const user = await getCurrentUser();
    expect(user).toBe('unknown');
  });
});
