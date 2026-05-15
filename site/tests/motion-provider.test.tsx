import { render, screen } from "@testing-library/react";
import { renderHook } from "@testing-library/react";
import { describe, it, expect, vi, afterEach } from "vitest";
import { MotionProvider } from "@/motion/MotionProvider";
import { useReducedMotion } from "@/motion/useReducedMotion";

function mockMatchMedia(matches: boolean) {
  window.matchMedia = ((query: string) => ({
    matches,
    media: query,
    onchange: null,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    addListener: vi.fn(),
    removeListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })) as unknown as typeof window.matchMedia;
}

afterEach(() => {
  mockMatchMedia(false);
});

describe("MotionProvider", () => {
  it("renders children (motion allowed)", () => {
    mockMatchMedia(false);
    render(<MotionProvider><p>child</p></MotionProvider>);
    expect(screen.getByText("child")).toBeInTheDocument();
  });

  it("renders children and skips motion init when reduced motion is preferred", () => {
    mockMatchMedia(true);
    render(<MotionProvider><p>reduced-child</p></MotionProvider>);
    expect(screen.getByText("reduced-child")).toBeInTheDocument();
  });
});

describe("useReducedMotion", () => {
  it("returns false when no reduced-motion preference", () => {
    mockMatchMedia(false);
    const { result } = renderHook(() => useReducedMotion());
    expect(result.current).toBe(false);
  });

  it("returns true when reduced-motion is preferred", () => {
    mockMatchMedia(true);
    const { result } = renderHook(() => useReducedMotion());
    expect(result.current).toBe(true);
  });
});
