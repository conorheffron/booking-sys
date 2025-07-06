import React from "react";
import { within, render, screen, waitFor, fireEvent } from "@testing-library/react";
import { ReservationsPage } from "../ReservationsPage";

// Minimal mocks for dependencies
jest.mock("../../components/Navbar", () => ({
  Navbar: () => <nav>Navbar</nav>,
}));
jest.mock("bootstrap/dist/css/bootstrap.min.css", () => ({}));

describe("ReservationsPage", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    if (global.fetch) {
      (global.fetch as any).mockClear?.();
    }
  });

  it("renders loading state initially", () => {
    (global.fetch as jest.Mock) = jest.fn(() => new Promise(() => {}));
    render(<ReservationsPage />);
    expect(screen.getByText(/Loading.../i)).toBeInTheDocument();
  });

  it("shows error if fetching reservations fails", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockResolvedValueOnce({
      ok: false,
      json: async () => ({}),
    });
    render(<ReservationsPage />);
    await waitFor(() =>
      expect(screen.getByText(/Failed to fetch reservations/i)).toBeInTheDocument()
    );
  });

  it("renders empty table message if no reservations", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ reservations: [] }),
    });
    render(<ReservationsPage />);
    await waitFor(() =>
      expect(screen.getByText(/No reservations found/i)).toBeInTheDocument()
    );
  });

  it("renders reservations in table", async () => {
    const reservations = [
      {
        id: 1,
        first_name: "Alice",
        reservation_date: "2099-07-01",
        reservation_slot: "09:00",
      },
      {
        id: 2,
        first_name: "Bob",
        reservation_date: "2099-07-02",
        reservation_slot: "11:00",
      },
    ];
    (global.fetch as jest.Mock) = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ reservations }),
    });
    render(<ReservationsPage />);
    await waitFor(() => expect(screen.getByText("Alice")).toBeInTheDocument());
    expect(screen.getByText("Bob")).toBeInTheDocument();
    expect(screen.getByText("2099-07-01")).toBeInTheDocument();
    expect(screen.getByText("11:00")).toBeInTheDocument();
    // Test Edit button/link
    expect(screen.getAllByRole("link", { name: /Edit/i })[0].getAttribute("href")).toBe("/reservations/edit/1");
    expect(screen.getAllByRole("link", { name: /Edit/i })[1].getAttribute("href")).toBe("/reservations/edit/2");
  });

  it("renders correct table headers", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ reservations: [] }),
    });
    const { container } = render(<ReservationsPage />);
    await waitFor(() => expect(container.querySelector("table")).toBeInTheDocument());
    const table = container.querySelector("table")!;
    const headers = Array.from(table.querySelectorAll("th")).map(th => th.textContent?.trim());
    expect(headers).toEqual([
        "ID",
        "Name",
        "Booking Date",
        "Booking Time",
        "Actions",
    ]);
  });

  it("renders and disables Refresh button while loading", () => {
    (global.fetch as jest.Mock) = jest.fn(() => new Promise(() => {}));
    render(<ReservationsPage />);
    const refreshButton = screen.getByRole("button", { name: /Refresh/i });
    expect(refreshButton).toBeInTheDocument();
    expect(refreshButton).toBeDisabled();
  });

  it("calls fetchReservations again when Refresh button is clicked", async () => {
    // Always resolve (handle multiple calls)
    (global.fetch as jest.Mock) = jest
        .fn()
        .mockResolvedValue({
        ok: true,
        json: async () => ({ reservations: [] }),
        });

    render(<ReservationsPage />);
    // Wait for the table to appear (first fetch completes)
    await waitFor(() => expect(screen.getByText(/Refresh/i)).toBeEnabled());

    const refreshButton = screen.getByRole("button", { name: /Refresh/i });
    fireEvent.click(refreshButton);

    // Wait for the second fetch call
    await waitFor(() => {
        expect((global.fetch as jest.Mock).mock.calls.length).toBeGreaterThan(1);
    });
  });

  it("always renders the Navbar", () => {
    (global.fetch as jest.Mock) = jest.fn(() => new Promise(() => {}));
    render(<ReservationsPage />);
    expect(screen.getByText("Navbar")).toBeInTheDocument();
  });
});
