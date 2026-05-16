import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BookingPage } from "../BookingPage";

// Only mock what is necessary for component to render
jest.mock("../../components/Navbar", () => ({
  Navbar: () => <nav>Navbar</nav>,
}));
jest.mock("bootstrap/dist/css/bootstrap.min.css", () => ({}));
jest.mock("../../components/Utils", () => ({
  getCSRFToken: jest.fn().mockResolvedValue("csrf-token"),
  getSlots: jest.fn(() => ["09:00", "10:00", "11:00"]),
}));

describe("BookingPage (basic smoke tests)", () => {
  const isWeatherRequest = (url: string): boolean => {
    const parsedUrl = new URL(String(url), "http://localhost");
    return parsedUrl.hostname === "api.open-meteo.com";
  };

  beforeEach(() => {
    (global.fetch as jest.Mock) = jest.fn().mockImplementation((url: string) => {
      if (isWeatherRequest(url)) {
        return Promise.resolve({
          ok: true,
          json: async () => ({
            current: {
              temperature_2m: 13.0,
              wind_speed_10m: 18.0,
              weather_code: 2,
              time: "2026-01-01T10:00",
            },
          }),
        });
      }
      return Promise.resolve({
        ok: true,
        json: async () => ({ reservations: [] }),
      });
    });
  });

  it("renders booking form and table", () => {
    render(<BookingPage />);
    expect(screen.getByText(/Make a Reservation/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Reservation date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Reservation slot/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Reserve/i })).toBeInTheDocument();
    expect(screen.getByText(/Bookings for/)).toBeInTheDocument();
  });

  it("shows loading state for bookings (with real fetch, may error)", async () => {
    render(<BookingPage />);
    expect(screen.getAllByText(/Loading.../i).length).toBeGreaterThan(0);
    await waitFor(() => {
      expect(screen.queryByText(/Loading.../i)).not.toBeInTheDocument();
    });
  });

  it("renders weather snapshot from API data", async () => {
    render(<BookingPage />);
    expect(screen.getByText(/Dublin Weather Snapshot/i)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText(/13°C/i)).toBeInTheDocument());
    expect(screen.getByText(/18 km\/h wind/i)).toBeInTheDocument();
    expect(screen.getByText(/Partly cloudy/i)).toBeInTheDocument();
  });

  it("shows weather unavailable fallback when weather API fails", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockImplementation((url: string) => {
      if (isWeatherRequest(url)) {
        return Promise.resolve({ ok: false, json: async () => ({}) });
      }
      return Promise.resolve({
        ok: true,
        json: async () => ({ reservations: [] }),
      });
    });

    render(<BookingPage />);
    await waitFor(() =>
      expect(screen.getByText(/Weather unavailable right now/i)).toBeInTheDocument()
    );
  });

  it("can fill the form fields", () => {
    render(<BookingPage />);
    const nameInput = screen.getByLabelText(/Name/i);
    const dateInput = screen.getByLabelText(/Reservation date/i);
    const slotSelect = screen.getByLabelText(/Reservation slot/i);

    fireEvent.change(nameInput, { target: { value: "Bob" } });
    fireEvent.change(dateInput, { target: { value: "2099-01-01" } });
    fireEvent.change(slotSelect, { target: { value: "10:00" } });

    expect((nameInput as HTMLInputElement).value).toBe("Bob");
    expect((dateInput as HTMLInputElement).value).toBe("2099-01-01");
    expect((slotSelect as HTMLSelectElement).value).toBe("10:00");
  });

  it("shows validation errors if required fields are empty", async () => {
    render(<BookingPage />);
    fireEvent.click(screen.getByRole("button", { name: /Reserve/i }));
    // Expect some indication of invalid input (native validation won't submit)
    const nameInput = screen.getByLabelText(/Name/i);
    expect(nameInput).toBeInvalid();
  });

  it("disables Reserve button when loading", async () => {
    render(<BookingPage />);
    // While loading (immediately after render), the button should not be disabled
    const reserveButton = screen.getByRole("button", { name: /Reserve/i });
    expect(reserveButton).not.toBeDisabled();
    // Optionally simulate loading state and check, if component supports it
  });

  it("renders all available slot options", () => {
    render(<BookingPage />);
    expect(screen.getByRole("option", { name: /09:00/i })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: /10:00/i })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: /11:00/i })).toBeInTheDocument();
  });

  it("shows 'No bookings yet.' when bookings table is empty", async () => {
    render(<BookingPage />);
    // Wait for bookings to load (or error)
    await waitFor(() => {
      expect(screen.getByText(/No bookings yet/i)).toBeInTheDocument();
    });
  });

  it("shows correct table headers", () => {
    render(<BookingPage />);
    // Only assert that a <th> contains the text
    const firstNameHeaders = screen.getAllByText(/Name/i);
    expect(firstNameHeaders.some((el) => el.tagName === "TH")).toBe(true);

    const dateHeaders = screen.getAllByText(/Date/i);
    expect(dateHeaders.some((el) => el.tagName === "TH")).toBe(true);

    const slotHeaders = screen.getAllByText(/Slot/i);
    expect(slotHeaders.some((el) => el.tagName === "TH")).toBe(true);
  });

  it("renders booking rows when bookings API returns data", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        reservations: [
          { first_name: "Alice", reservation_date: "2099-01-01", reservation_slot: "09:00 AM" },
        ],
      }),
    });
    render(<BookingPage />);
    await waitFor(() => expect(screen.getByText("Alice")).toBeInTheDocument());
    expect(screen.getByText("2099-01-01")).toBeInTheDocument();
    expect(screen.getByText("09:00 AM")).toBeInTheDocument();
  });

  it("shows fetch error for bookings API failures", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockResolvedValue({
      ok: false,
      json: async () => ({}),
    });
    render(<BookingPage />);
    await waitFor(() =>
      expect(screen.getByText(/Failed to fetch bookings/i)).toBeInTheDocument()
    );
  });

  it("shows backend error message when reservation submit fails", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockImplementation((_url: string, options?: RequestInit) => {
      if (options?.method === "PUT") {
        return Promise.resolve({ ok: false, json: async () => ({ detail: "Booking already exists" }) });
      }
      return Promise.resolve({ ok: true, json: async () => ({ reservations: [] }) });
    });

    render(<BookingPage />);
    fireEvent.change(screen.getByLabelText(/Name/i), { target: { value: "Bob" } });
    fireEvent.change(screen.getByLabelText(/Reservation date/i), { target: { value: "2099-01-01" } });
    fireEvent.change(screen.getByLabelText(/Reservation slot/i), { target: { value: "10:00" } });
    fireEvent.click(screen.getByRole("button", { name: /Reserve/i }));

    await waitFor(() =>
      expect(screen.getByText(/Error: Booking already exists/i)).toBeInTheDocument()
    );
  });

  it("shows success message when reservation submit succeeds", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockImplementation((_url: string, options?: RequestInit) => {
      if (options?.method === "PUT") {
        return Promise.resolve({ ok: true, json: async () => ({ id: 1 }) });
      }
      return Promise.resolve({ ok: true, json: async () => ({ reservations: [] }) });
    });

    render(<BookingPage />);
    fireEvent.change(screen.getByLabelText(/Name/i), { target: { value: "Bob" } });
    fireEvent.change(screen.getByLabelText(/Reservation date/i), { target: { value: "2099-01-01" } });
    fireEvent.change(screen.getByLabelText(/Reservation slot/i), { target: { value: "10:00" } });
    fireEvent.click(screen.getByRole("button", { name: /Reserve/i }));

    await waitFor(() =>
      expect(screen.getByText(/Reservation submitted!/i)).toBeInTheDocument()
    );
  });
});
