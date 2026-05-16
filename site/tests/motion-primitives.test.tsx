import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeAll } from "vitest";
import { Reveal } from "@/motion/Reveal";
import { CountUp } from "@/motion/CountUp";

// Local IntersectionObserver shim (do NOT edit shared vitest.setup.ts)
beforeAll(() => {
  class IO { observe() {} disconnect() {} unobserve() {} }
  // @ts-expect-error test shim
  window.IntersectionObserver = window.IntersectionObserver || IO;
});

describe("motion primitives", () => {
  it("Reveal renders its children", () => {
    render(<Reveal><span>revealed</span></Reveal>);
    expect(screen.getByText("revealed")).toBeInTheDocument();
  });
  it("CountUp shows final value under reduced motion", () => {
    window.matchMedia = ((q: string) => ({ matches: true, media: q, onchange: null, addEventListener: vi.fn(), removeEventListener: vi.fn(), addListener: vi.fn(), removeListener: vi.fn(), dispatchEvent: vi.fn() })) as never;
    render(<CountUp to={70.22} suffix=" / 90" />);
    expect(screen.getByText(/70\.22 \/ 90/)).toBeInTheDocument();
  });
});
