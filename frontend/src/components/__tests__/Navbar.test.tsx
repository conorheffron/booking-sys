import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Navbar } from '../Navbar';

// If you have moduleNameMapper for images, you can remove this manual mock
jest.mock('../img/robot-logo.png', () => 'robot-logo.png');

// Mock appVersionCache
jest.mock('../../components/appVersionCache', () => ({
  getAppVersion: jest.fn(),
}));

import { getAppVersion } from '../../components/appVersionCache';

// Helper to render with router context
function renderWithRouter(ui: React.ReactElement) {
  return render(<BrowserRouter>{ui}</BrowserRouter>);
}

describe('Navbar', () => {
  afterEach(() => {
    jest.restoreAllMocks();
    jest.clearAllMocks();
  });

  it('renders logo, brand, and navigation links', () => {
    (getAppVersion as jest.Mock).mockResolvedValue('1.2.3');
    renderWithRouter(<Navbar />);
    expect(screen.getByAltText('Logo')).toBeInTheDocument();
    expect(screen.getByText('Booking System')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Home' })).toHaveAttribute('href', '/');
    expect(screen.getByRole('link', { name: 'Bookings' })).toHaveAttribute('href', '/reservations');
    expect(screen.getByRole('link', { name: 'Django-Admin' })).toHaveAttribute('href', '/admin');
    expect(screen.getByRole('link', { name: 'Swagger' })).toHaveAttribute('href', '/api/docs/');
  });

  it('renders initial version as ellipsis', () => {
    (getAppVersion as jest.Mock).mockImplementation(() => new Promise(() => {}));
    renderWithRouter(<Navbar />);
    expect(screen.getByText(/Version: …/)).toBeInTheDocument();
  });

  it('fetches and displays the app version on success', async () => {
    (getAppVersion as jest.Mock).mockResolvedValue('1.2.3');
    renderWithRouter(<Navbar />);
    await waitFor(() => {
      expect(screen.getByText('Version: 1.2.3')).toBeInTheDocument();
    });
  });

  it('displays "unknown" if fetch fails', async () => {
    (getAppVersion as jest.Mock).mockRejectedValue(new Error('Network error'));
    renderWithRouter(<Navbar />);
    await waitFor(() => {
      expect(screen.getByRole('link', { name: /unknown/i })).toBeInTheDocument();
    });
  });

  it('has external link to the GitHub repo', () => {
    (getAppVersion as jest.Mock).mockResolvedValue('1.2.3');
    renderWithRouter(<Navbar />);
    const link = screen.getByRole('link', { name: /Version:/ });
    expect(link).toHaveAttribute('href', 'https://github.com/conorheffron/booking-sys');
    expect(link).toHaveAttribute('target', '_blank');
    expect(link).toHaveAttribute('rel', expect.stringContaining('noopener'));
  });
});
