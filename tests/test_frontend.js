import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import SearchBar from "../frontend/src/components/SearchBar";
import App from "../frontend/src/App";

// Mock fetch so App can call backend safely
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve({
        results: [
          {
            id: "1",
            video_id: "abc123",
            title: "How Long Do Cats Live?",
            text: "Cats live 12-15 years on average.",
            start: 42.0,
          },
        ],
      }),
  })
);

describe("SearchBar", () => {
  it("renders input and calls onSearch when submitted", () => {
    const mockSearch = jest.fn();
    render(<SearchBar onSearch={mockSearch} />);

    const input = screen.getByPlaceholderText("Ask a question...");
    fireEvent.change(input, { target: { value: "How long do cats live?" } });
    fireEvent.submit(input);

    expect(mockSearch).toHaveBeenCalledWith("How long do cats live?");
  });
});

describe("App", () => {
  it("renders and fetches results on search", async () => {
    render(<App />);

    const input = screen.getByPlaceholderText("Ask a question...");
    fireEvent.change(input, { target: { value: "How long do cats live?" } });
    fireEvent.submit(input);

    expect(await screen.findByText(/How Long Do Cats Live/i)).toBeInTheDocument();
    expect(await screen.findByText(/Cats live 12-15 years/i)).toBeInTheDocument();
  });
});
