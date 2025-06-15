import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Navbar } from '../Navbar';

// If you have moduleNameMapper for images, you can remove this manual mock
jest.mock('../img/robot-logo.png', () => 'robot-logo.png');

// Helper to render with router context
function renderWithRouter(ui: React.ReactElement) {
  return render(<BrowserRouter>{ui}</BrowserRouter>);
}

describe('Navbar', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('renders logo, brand, and navigation links', () => {
    // Mock fetch (prevent it from running for this test)
    jest.spyOn(global, 'fetch').mockImplementation(() =>
      Promise.resolve({
        ok: true,
        text: () => Promise.resolve('1.2.3'),
      } as Response)
    );
    renderWithRouter(<Navbar />);
    expect(screen.getByAltText('Logo')).toBeInTheDocument();
    expect(screen.getByText('Booking System')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Home' })).toHaveAttribute('href', '/');
    expect(screen.getByRole('link', { name: 'Bookings' })).toHaveAttribute('href', '/reservations');
    expect(screen.getByRole('link', { name: 'Login' })).toHaveAttribute('href', '/admin');
  });

  it('renders initial version as ellipsis', () => {
    jest.spyOn(global, 'fetch').mockImplementation(() =>
      new Promise(() => {}) // never resolves
    );
    renderWithRouter(<Navbar />);
    expect(screen.getByText(/Version: …/)).toBeInTheDocument();
  });

  it('fetches and displays the app version on success', async () => {
    jest.spyOn(global, 'fetch').mockResolvedValue({
      ok: true,
      text: () => Promise.resolve('1.2.3\n'),
    } as Response);

    renderWithRouter(<Navbar />);
    await waitFor(() => {
      expect(screen.getByText('Version: 1.2.3')).toBeInTheDocument();
    });
  });

  it('displays "unknown" if fetch fails', async () => {
    jest.spyOn(global, 'fetch').mockRejectedValue(new Error('Network error'));

    renderWithRouter(<Navbar />);
    await waitFor(() => {
      expect(screen.getByText('Version: unknown')).toBeInTheDocument();
    });
  });

  it('displays "unknown" if fetch response is not ok', async () => {
    jest.spyOn(global, 'fetch').mockResolvedValue({
      ok: false,
      text: () => Promise.resolve('should not be used'),
    } as Response);

    renderWithRouter(<Navbar />);
    await waitFor(() => {
      expect(screen.getByText('Version: unknown')).toBeInTheDocument();
    });
  });

  it('has external link to the GitHub repo', () => {
    jest.spyOn(global, 'fetch').mockImplementation(() =>
      Promise.resolve({
        ok: true,
        text: () => Promise.resolve('1.2.3'),
      } as Response)
    );
    renderWithRouter(<Navbar />);
    const link = screen.getByRole('link', { name: /Version:/ });
    expect(link).toHaveAttribute('href', 'https://github.com/conorheffron/booking-sys');
    expect(link).toHaveAttribute('target', '_blank');
    expect(link).toHaveAttribute('rel', expect.stringContaining('noopener'));
  });
});
