import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";

describe("layout", () => {
  it("Header renders wordmark and primary nav", () => {
    render(<Header />);
    expect(screen.getByText("Precision Memory Agent")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Method" })).toBeInTheDocument();
  });
  it("Footer renders 5 column headings", () => {
    render(<Footer />);
    ["Project", "Sitemap", "Resources", "Modules", "Social"].forEach((h) =>
      expect(screen.getByRole("heading", { name: h })).toBeInTheDocument()
    );
  });
});
