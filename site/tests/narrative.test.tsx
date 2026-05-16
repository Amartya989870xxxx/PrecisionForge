import { render, screen } from "@testing-library/react";
import { describe, it, expect, beforeAll } from "vitest";
import { Narrative } from "@/components/templates/Narrative";
import { getNarrative } from "@/lib/content";

// Local IntersectionObserver shim (do NOT edit shared vitest.setup.ts).
// Narrative renders <Reveal>, which uses framer-motion whileInView.
beforeAll(() => {
  function IO(this: unknown) {
    return { observe() {}, disconnect() {}, unobserve() {}, takeRecords() { return []; } };
  }
  window.IntersectionObserver =
    window.IntersectionObserver || (IO as unknown as typeof IntersectionObserver);
});

describe("narrative template", () => {
  it("renders method narrative", () => {
    render(<Narrative data={getNarrative("method")!} />);
    expect(screen.getByRole("heading", { level: 1, name: "Method" })).toBeInTheDocument();
    expect(screen.getByText(/Corruption regime/)).toBeInTheDocument();
  });
});
