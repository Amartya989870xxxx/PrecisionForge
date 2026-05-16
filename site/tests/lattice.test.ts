import { describe, it, expect } from "vitest";
import { latticePositions } from "@/three/lattice";

describe("latticePositions", () => {
  it("returns a Float32Array of length n*3", () => {
    const n = 128;
    const arr = latticePositions(n);
    expect(arr).toBeInstanceOf(Float32Array);
    expect(arr.length).toBe(n * 3);
  });

  it("bounds values within the spread", () => {
    const spread = 4;
    const arr = latticePositions(200, spread);
    for (let i = 0; i < arr.length; i += 3) {
      expect(Math.abs(arr[i])).toBeLessThanOrEqual(spread); // x: ±spread*2/2
      expect(Math.abs(arr[i + 1])).toBeLessThanOrEqual(spread / 2);
      expect(Math.abs(arr[i + 2])).toBeLessThanOrEqual(spread);
    }
  });

  it("handles a zero count", () => {
    expect(latticePositions(0).length).toBe(0);
  });
});
