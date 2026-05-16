import { describe, it, expect } from "vitest";
import { getNotes } from "@/lib/notes";

describe("notes", () => {
  it("lists notes with frontmatter", () => {
    const n = getNotes();
    expect(n.length).toBeGreaterThanOrEqual(1);
    expect(n[0]).toMatchObject({ slug: "precision-regimes", kind: "Guides" });
  });
});
