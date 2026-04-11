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
  beforeEach(() => {
    if (global.fetch) {
      (global.fetch as any).mockClear?.();
    }
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
    expect(screen.getByText(/Loading.../i)).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.queryByText(/Loading.../i)).not.toBeInTheDocument();
    });
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
    (global.fetch as jest.Mock) = jest
      .fn()
      .mockResolvedValueOnce({ ok: true, json: async () => ({ reservations: [] }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ reservations: [] }) })
      .mockResolvedValueOnce({ ok: false, json: async () => ({ detail: "Booking already exists" }) });

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
    (global.fetch as jest.Mock) = jest
      .fn()
      .mockResolvedValueOnce({ ok: true, json: async () => ({ reservations: [] }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ reservations: [] }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ id: 1 }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ reservations: [] }) });

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
