import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, afterEach } from "vitest";
import { Hero } from "@/components/sections/Hero";

vi.mock("@/three/HeroScene", () => ({ HeroScene: () => <div data-testid="r3f-scene" /> }));

function setReducedMotion(matches: boolean) {
  window.matchMedia = ((q: string) => ({
    matches,
    media: q,
    onchange: null,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    addListener: vi.fn(),
    removeListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })) as never;
}

afterEach(() => {
  setReducedMotion(false);
});

describe("Hero", () => {
  it("renders headline + CTA over the scene", () => {
    render(<Hero />);
    expect(screen.getByRole("heading", { level: 1 })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /method/i })).toBeInTheDocument();
  });

  it("under reduced motion renders the static gradient, not the WebGL scene", () => {
    setReducedMotion(true);
    render(<Hero />);
    expect(screen.getByRole("heading", { level: 1 })).toBeInTheDocument();
    expect(screen.queryByTestId("r3f-scene")).not.toBeInTheDocument();
  });
});
