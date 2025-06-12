import { getSlots, getCSRFToken } from '../Utils';

// Mock global fetch for getCSRFToken
global.fetch = jest.fn();

// Helper to reset date mutations if needed
const originalDate = global.Date;

describe('getSlots', () => {
  it('should return all 30-minute intervals from 09:00 AM to 07:00 PM (inclusive)', () => {
    const slots = getSlots();
    // 09:00 to 19:00 is 10 hours, 21 intervals (including both ends)
    expect(slots.length).toBe(21);
    expect(slots[0]).toBe('9:00 AM');
    expect(slots[1]).toBe('9:30 AM');
    expect(slots[2]).toBe('10:00 AM');
    expect(slots[10]).toBe('2:00 PM');
    expect(slots[20]).toBe('7:00 PM');
  });

  it('should return a fresh array each time', () => {
    const slots1 = getSlots();
    const slots2 = getSlots();
    expect(slots1).not.toBe(slots2);
    // Mutate one, should not affect the other
    slots1[0] = 'foo';
    expect(slots2[0]).toBe('9:00 AM');
  });
});

describe('getCSRFToken', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should fetch CSRF token from /api/csrf/', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      json: async () => ({ csrfToken: 'abc123' })
    });
    const token = await getCSRFToken();
    expect(fetch).toHaveBeenCalledWith('/api/csrf/', { credentials: 'include' });
    expect(token).toBe('abc123');
  });

  it('should throw if response is not as expected', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      json: async () => ({ wrongKey: 'oops' })
    });
    const token = await getCSRFToken();
    expect(token).toBeUndefined();
  });
});
