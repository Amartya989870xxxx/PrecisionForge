import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { Hero } from "@/components/sections/Hero";

vi.mock("@/three/HeroScene", () => ({ HeroScene: () => <div data-testid="r3f-scene" /> }));

describe("Hero", () => {
  it("renders headline + CTA over the scene", () => {
    render(<Hero />);
    expect(screen.getByRole("heading", { level: 1 })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /method/i })).toBeInTheDocument();
  });
});
