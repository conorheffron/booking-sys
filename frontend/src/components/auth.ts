export interface AuthStatus {
  authenticated: boolean;
  username?: string | null;
}

export async function getAuthStatus(): Promise<AuthStatus> {
  const response = await fetch('/api/auth/status', {
    credentials: 'include',
  });
  if (!response.ok) {
    return { authenticated: false, username: null };
  }
  return response.json();
}

export async function loginUser(username: string, password: string, csrfToken: string) {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({ username, password }),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'Login failed');
  }
  return data;
}

export async function logoutUser(csrfToken: string) {
  const response = await fetch('/api/auth/logout', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'X-CSRFToken': csrfToken,
    },
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'Logout failed');
  }
  return data;
}
