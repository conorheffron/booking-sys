import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { LoginPage } from "../LoginPage";

jest.mock("../../components/Navbar", () => ({
  Navbar: () => <nav>Navbar</nav>,
}));
jest.mock("../../components/Utils", () => ({
  getCSRFToken: jest.fn().mockResolvedValue("csrf-token"),
}));
jest.mock("../../components/auth", () => ({
  loginUser: jest.fn().mockResolvedValue({ success: true }),
}));

import { loginUser } from "../../components/auth";

describe("LoginPage", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("submits credentials and navigates on success", async () => {
    render(
      <MemoryRouter initialEntries={["/login"]}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/reservations" element={<div>Reservations List</div>} />
        </Routes>
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/Username/i), { target: { value: "apiuser" } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: "safe-password-123" } });
    fireEvent.click(screen.getByRole("button", { name: /Login/i }));

    await waitFor(() => expect(loginUser).toHaveBeenCalledWith("apiuser", "safe-password-123", "csrf-token"));
    await waitFor(() => expect(screen.getByText(/Reservations List/i)).toBeInTheDocument());
  });

  it("shows error when login fails", async () => {
    (loginUser as jest.Mock).mockRejectedValueOnce(new Error("Invalid credentials."));

    render(
      <MemoryRouter initialEntries={["/login"]}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/Username/i), { target: { value: "apiuser" } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: "bad-password" } });
    fireEvent.click(screen.getByRole("button", { name: /Login/i }));

    await waitFor(() => expect(screen.getByText(/Invalid credentials/i)).toBeInTheDocument());
  });
});
