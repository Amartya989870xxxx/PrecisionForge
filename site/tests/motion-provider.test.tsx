import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { MotionProvider } from "@/motion/MotionProvider";

describe("MotionProvider", () => {
  it("renders children", () => {
    render(<MotionProvider><p>child</p></MotionProvider>);
    expect(screen.getByText("child")).toBeInTheDocument();
  });
});
