import React from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { ErrorPage } from "../ErrorPage";

// Only mock what is necessary for component to render
jest.mock("../../components/Navbar", () => ({
  Navbar: () => <nav>Navbar</nav>,
}));
jest.mock("bootstrap/dist/css/bootstrap.min.css", () => ({}));

describe("ErrorPage", () => {
  it("renders not found message and Navbar", () => {
    render(
      <MemoryRouter initialEntries={["/some/unknown/path"]}>
        <ErrorPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Page Not Found/i)).toBeInTheDocument();
    expect(screen.getByText("Navbar")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /Page Not Found/i })).toBeInTheDocument();
  });

  it("shows the unknown URL in the message", () => {
    render(
      <MemoryRouter initialEntries={["/test/404"]}>
        <ErrorPage />
      </MemoryRouter>
    );
    expect(screen.getByText("/test/404")).toBeInTheDocument();
    expect(screen.getByText((txt) => txt.includes("was not found on this server"))).toBeInTheDocument();
  });

  it("renders a link to the home page", () => {
    render(
      <MemoryRouter initialEntries={["/nowhere/land"]}>
        <ErrorPage />
      </MemoryRouter>
    );
    const homeLink = screen.getByRole("link", { name: /Return Home/i });
    expect(homeLink).toBeInTheDocument();
    expect(homeLink.getAttribute("href")).toBe("/");
  });

  it("has expected Bootstrap/card classes", () => {
    render(
      <MemoryRouter initialEntries={["/abc"]}>
        <ErrorPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Page Not Found/i).closest(".card")).toBeInTheDocument();
    expect(screen.getByText(/Page Not Found/i).className).toMatch(/display-4/);
    expect(screen.getByRole("link", { name: /Return Home/i }).className).toMatch(/btn-primary/);
  });

  it("renders correctly for root path as well", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <ErrorPage />
      </MemoryRouter>
    );
    expect(screen.getByText("/")).toBeInTheDocument();
  });
});
