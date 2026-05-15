import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

function Hello() {
  return <h1>Precision Memory Agent</h1>;
}

describe("test harness", () => {
  it("renders a component", () => {
    render(<Hello />);
    expect(screen.getByRole("heading", { name: "Precision Memory Agent" })).toBeInTheDocument();
  });
});
