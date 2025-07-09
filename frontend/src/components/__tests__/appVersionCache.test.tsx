import {
  getAppVersion,
  getCachedAppVersion,
  setCachedAppVersion,
  clearCachedAppVersion,
  fetchAndCacheAppVersion,
} from '../appVersionCache';

// Patch cache TTL to 1 hour for testing
jest.mock('../appVersionCache', () => {
  const original = jest.requireActual('../appVersionCache');
  return {
    ...original,
    // Override only CACHE_TTL for these tests
    CACHE_TTL: 60 * 60 * 1000, // 1 hour
  };
});

describe('appVersionCache with 1-hour TTL', () => {
  const VERSION_KEY = 'app_version_number';
  const VERSION_EXPIRY_KEY = 'app_version_number_expiry';

  beforeEach(() => {
    localStorage.clear();
    jest.useFakeTimers();
  });

  afterEach(() => {
    localStorage.clear();
    jest.useRealTimers();
    jest.resetAllMocks();
  });

  it('returns cached version if within 1 hour', () => {
    setCachedAppVersion('x.y.z');
    expect(getCachedAppVersion()).toBe('x.y.z');
  });

  it('returns null if expired after 1 hour', () => {
    setCachedAppVersion('x.y.z');
    // Advance fake timer by 1 hour + 1ms
    jest.advanceTimersByTime(60 * 60 * 1000 + 1);
    expect(getCachedAppVersion()).toBeNull();
  });

  it('fetches from API if cache expired', async () => {
    // Set up expired cache
    setCachedAppVersion('x.y.z');
    jest.advanceTimersByTime(60 * 60 * 1000 + 1);

    // Mock fetch
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      text: () => Promise.resolve('1.2.3'),
    } as any);

    const version = await getAppVersion();
    expect(version).toBe('1.2.3');
    expect(global.fetch).toHaveBeenCalled();
  });

  it('does not call API if cache is valid', async () => {
    setCachedAppVersion('x.y.z');
    global.fetch = jest.fn();
    const version = await getAppVersion();
    expect(version).toBe('x.y.z');
    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('clears both value and expiry', () => {
    setCachedAppVersion('abc');
    clearCachedAppVersion();
    expect(localStorage.getItem(VERSION_KEY)).toBeNull();
    expect(localStorage.getItem(VERSION_EXPIRY_KEY)).toBeNull();
  });
});
