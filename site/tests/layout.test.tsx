import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { ScrollToTop } from "@/components/layout/ScrollToTop";

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

describe("ScrollToTop", () => {
  it("is rendered but visually hidden initially, and reveals after scrolling past one viewport", () => {
    const { getByRole } = render(<ScrollToTop />);
    const btn = getByRole("button", { name: "Scroll to top" });
    expect(btn).toBeInTheDocument();
    expect(btn.className).toContain("opacity-0");
    Object.defineProperty(window, "scrollY", { value: window.innerHeight + 10, configurable: true });
    fireEvent.scroll(window);
    expect(btn.className).toContain("opacity-100");
  });
});
