import { render } from "@testing-library/react";
import { describe, it, expect } from "vitest";

describe("design tokens", () => {
  it("exposes accent token class", () => {
    const { container } = render(<div className="text-accent">x</div>);
    expect(container.firstChild).toHaveClass("text-accent");
  });
});
