import { getCSRFToken } from '../Utils';

describe('getCSRFToken', () => {
  const originalCookie = Object.getOwnPropertyDescriptor(document, 'cookie');

  afterEach(() => {
    // Restore original document.cookie descriptor if it existed
    if (originalCookie) {
      Object.defineProperty(document, 'cookie', originalCookie);
    }
  });

  it('should return the CSRF token value if present in the cookie', () => {
    Object.defineProperty(document, 'cookie', {
      writable: true,
      value: 'username=foo; csrftoken=mytoken123; sessionid=bar',
    });
    expect(getCSRFToken()).toBe('mytoken123');
  });

  it('should return an empty string if CSRF token is not present in the cookie', () => {
    Object.defineProperty(document, 'cookie', {
      writable: true,
      value: 'username=foo; sessionid=bar',
    });
    expect(getCSRFToken()).toBe('');
  });

  it('should return the first CSRF token if multiple are present', () => {
    Object.defineProperty(document, 'cookie', {
      writable: true,
      value: 'csrftoken=first; csrftoken=second;',
    });
    expect(getCSRFToken()).toBe('first');
  });

  it('should handle cookies with extra spaces', () => {
    Object.defineProperty(document, 'cookie', {
      writable: true,
      value: '  csrftoken=spacey ;',
    });
    expect(getCSRFToken()).toBe('spacey ');
  });
});
