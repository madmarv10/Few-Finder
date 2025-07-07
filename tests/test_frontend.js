import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import SearchBar from "../frontend/src/components/SearchBar";
import App from "../frontend/src/App";

// Mock fetch so App can call backend safely
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () =>
      Promise.resolve({
        video_url: "https://www.youtube.com/watch?v=abc123&t=42s",
        transcript_text: "Cats live 12-15 years on average.",
        start_time: 42.0,
      }),
  })
);

// Mock lodash debounce
jest.mock('lodash', () => ({
  debounce: (fn) => fn
}));

describe("SearchBar", () => {
  it("renders input and calls onSearch when submitted with valid input", () => {
    const mockSearch = jest.fn();
    render(<SearchBar onSearch={mockSearch} />);

    const input = screen.getByPlaceholderText(/Ask a question/);
    fireEvent.change(input, { target: { value: "How long do cats live?" } });
    fireEvent.submit(input);

    expect(mockSearch).toHaveBeenCalledWith("How long do cats live?");
  });

  it("shows error for short input", () => {
    const mockSearch = jest.fn();
    render(<SearchBar onSearch={mockSearch} />);

    const input = screen.getByPlaceholderText(/Ask a question/);
    fireEvent.change(input, { target: { value: "Hi" } });
    fireEvent.submit(input);

    expect(screen.getByText(/Please enter at least 3 characters/)).toBeInTheDocument();
    expect(mockSearch).not.toHaveBeenCalled();
  });

  it("shows hint for input that's too short", () => {
    const mockSearch = jest.fn();
    render(<SearchBar onSearch={mockSearch} />);

    const input = screen.getByPlaceholderText(/Ask a question/);
    fireEvent.change(input, { target: { value: "Ho" } });

    expect(screen.getByText(/Type at least 1 more character/)).toBeInTheDocument();
  });

  it("disables search when disabled prop is true", () => {
    const mockSearch = jest.fn();
    render(<SearchBar onSearch={mockSearch} disabled={true} />);

    const input = screen.getByPlaceholderText(/Ask a question/);
    const button = screen.getByRole("button");

    expect(input).toBeDisabled();
    expect(button).toBeDisabled();
  });
});

describe("App", () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it("renders and fetches results on search", async () => {
    render(<App />);

    const input = screen.getByPlaceholderText(/Ask a question/);
    fireEvent.change(input, { target: { value: "How long do cats live?" } });
    fireEvent.submit(input);

    // Check loading state
    expect(screen.getByText(/Searching for answers/)).toBeInTheDocument();

    // Wait for results
    await waitFor(() => {
      expect(screen.getByText(/Cats live 12-15 years on average/)).toBeInTheDocument();
    });

    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/api/search",
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: "How long do cats live?" })
      })
    );
  });

  it("shows error when API call fails", async () => {
    fetch.mockImplementationOnce(() =>
      Promise.reject(new Error("Network error"))
    );

    render(<App />);

    const input = screen.getByPlaceholderText(/Ask a question/);
    fireEvent.change(input, { target: { value: "How long do cats live?" } });
    fireEvent.submit(input);

    await waitFor(() => {
      expect(screen.getByText(/An error occurred while searching/)).toBeInTheDocument();
    });
  });

  it("shows empty state when no search has been performed", () => {
    render(<App />);

    expect(screen.getByText(/Enter a question above to find answers/)).toBeInTheDocument();
  });
});
