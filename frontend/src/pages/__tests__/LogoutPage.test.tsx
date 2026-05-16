import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { LogoutPage } from "../LogoutPage";

jest.mock("../../components/Navbar", () => ({
  Navbar: () => <nav>Navbar</nav>,
}));
jest.mock("../../components/Utils", () => ({
  getCSRFToken: jest.fn().mockResolvedValue("csrf-token"),
}));
jest.mock("../../components/auth", () => ({
  logoutUser: jest.fn().mockResolvedValue({ success: true }),
}));

import { logoutUser } from "../../components/auth";

describe("LogoutPage", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("calls logout and redirects home", async () => {
    render(
      <MemoryRouter initialEntries={["/logout"]}>
        <Routes>
          <Route path="/logout" element={<LogoutPage />} />
          <Route path="/" element={<div>Home Page</div>} />
        </Routes>
      </MemoryRouter>
    );

    await waitFor(() => expect(logoutUser).toHaveBeenCalledWith("csrf-token"));
    await waitFor(() => expect(screen.getByText(/Home Page/i)).toBeInTheDocument());
  });

  it("shows error if logout fails", async () => {
    (logoutUser as jest.Mock).mockRejectedValueOnce(new Error("Logout failed"));

    render(
      <MemoryRouter initialEntries={["/logout"]}>
        <Routes>
          <Route path="/logout" element={<LogoutPage />} />
        </Routes>
      </MemoryRouter>
    );

    await waitFor(() => expect(screen.getByText(/Logout failed/i)).toBeInTheDocument());
  });
});
