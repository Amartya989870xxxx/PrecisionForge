import { describe, it, expect } from "vitest";
import { getModules, getModule } from "@/lib/content";

describe("content model", () => {
  it("lists modules with slugs", () => {
    const m = getModules();
    expect(m.length).toBeGreaterThanOrEqual(4);
    expect(m[0]).toHaveProperty("slug");
  });
  it("resolves a module by slug", () => {
    expect(getModule("geometry-branch")?.title).toMatch(/Geometry/);
  });
});
