import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { EditReservationPage } from "../EditReservationPage";

jest.mock("../../components/Navbar", () => ({
  Navbar: () => <nav>Navbar</nav>,
}));
jest.mock("bootstrap/dist/css/bootstrap.min.css", () => ({}));
jest.mock("../../components/Utils", () => ({
  getCSRFToken: jest.fn().mockResolvedValue("csrf-token"),
  getSlots: jest.fn(() => ["09:00", "10:00", "11:00"]),
}));

const renderWithRoute = (id = "123") =>
  render(
    <MemoryRouter initialEntries={[`/edit/${id}`]}>
      <Routes>
        <Route path="/edit/:id" element={<EditReservationPage />} />
        {/* Add a dummy /reservations route to avoid warning on redirect */}
        <Route path="/reservations" element={<div>Reservations List</div>} />
      </Routes>
    </MemoryRouter>
  );

describe("EditReservationPage", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset fetch mock between tests
    if (global.fetch) {
      (global.fetch as any).mockClear?.();
    }
  });

  it("renders loading state initially", async () => {
    (global.fetch as jest.Mock) = jest.fn(() =>
      new Promise(() => {}) // never resolves
    );
    renderWithRoute("42");
    expect(screen.getByText(/Loading.../i)).toBeInTheDocument();
  });

  it("shows error if reservation fetch fails", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockResolvedValueOnce({
      ok: false,
      json: async () => ({}),
    });
    renderWithRoute("42");
    await waitFor(() =>
      expect(screen.getByText(/Failed to fetch reservation/i)).toBeInTheDocument()
    );
  });

  it("renders form fields with fetched reservation data", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        id: 42,
        first_name: "Eve",
        reservation_date: "2099-12-31",
        reservation_slot: "10:00",
      }),
    });
    renderWithRoute("42");
    await waitFor(() => expect(screen.getByLabelText(/Name/i)).toHaveValue("Eve"));
    expect(screen.getByLabelText(/Date/i)).toHaveValue("2099-12-31");
    expect(screen.getByLabelText(/Slot/i)).toHaveValue("10:00");
    expect(screen.getByText(/Edit Reservation #42/i)).toBeInTheDocument();
  });

  it("shows validation error if required fields are empty", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        id: 1,
        first_name: "",
        reservation_date: "2099-01-01",
        reservation_slot: "09:00",
      }),
    });
    renderWithRoute("1");
    await waitFor(() => expect(screen.getByLabelText(/Name/i)).toBeInTheDocument());
    const nameInput = screen.getByLabelText(/Name/i);
    fireEvent.change(nameInput, { target: { value: "" } });
    fireEvent.click(screen.getByRole("button", { name: /Save/i }));
    expect(nameInput).toBeInvalid();
  });

  it("submits updated reservation and shows success, then navigates", async () => {
    // 1. fetch GET
    (global.fetch as jest.Mock) = jest.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 77,
          first_name: "OldName",
          reservation_date: "2099-10-01",
          reservation_slot: "09:00",
        }),
      })
      // 2. fetch PUT
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({}),
      });
    renderWithRoute("77");
    await waitFor(() => expect(screen.getByLabelText(/Name/i)).toHaveValue("OldName"));
    fireEvent.change(screen.getByLabelText(/Name/i), { target: { value: "NewName" } });
    fireEvent.click(screen.getByRole("button", { name: /Save/i }));
    await waitFor(() =>
      expect(screen.getByText(/Reservation updated successfully/i)).toBeInTheDocument()
    );
    // Should navigate to /reservations within 1.2s; check the dummy route
    await waitFor(() =>
      expect(screen.getByText(/Reservations List/i)).toBeInTheDocument(),
      { timeout: 1500 }
    );
  });

  it("shows backend error if update fails", async () => {
    // GET
    (global.fetch as jest.Mock) = jest.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 99,
          first_name: "X",
          reservation_date: "2099-03-01",
          reservation_slot: "10:00",
        }),
      })
      // PUT fails
      .mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: "Duplicate reservation" }),
      });
    renderWithRoute("99");
    await waitFor(() => expect(screen.getByLabelText(/Name/i)).toBeInTheDocument());
    fireEvent.click(screen.getByRole("button", { name: /Save/i }));
    await waitFor(() =>
      expect(screen.getByText(/Duplicate reservation/i)).toBeInTheDocument()
    );
  });

  it("renders slot options from getSlots", async () => {
    (global.fetch as jest.Mock) = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        id: 10,
        first_name: "Test",
        reservation_date: "2099-01-01",
        reservation_slot: "09:00",
      }),
    });
    renderWithRoute("10");
    await waitFor(() => expect(screen.getByLabelText(/Slot/i)).toBeInTheDocument());
    expect(screen.getByRole("option", { name: "09:00" })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "10:00" })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "11:00" })).toBeInTheDocument();
  });

  it("renders the Navbar always", () => {
    (global.fetch as jest.Mock) = jest.fn(() =>
      new Promise(() => {})
    );
    renderWithRoute("55");
    expect(screen.getByText("Navbar")).toBeInTheDocument();
  });
});
