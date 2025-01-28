import { describe, expect, test, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "./App";

describe("App", () => {
  test("should render without errors", async () => {
    const errorLog = vi.spyOn(console, "error");
    const warningLog = vi.spyOn(console, "warn");
    // Avoid fakerest logs
    vi.spyOn(console, "log").mockImplementation(() => {});

    render(<App />);
    await screen.findByText("Need invoice");

    expect(errorLog).not.toHaveBeenCalled();
    expect(warningLog).not.toHaveBeenCalled();
  });
});
