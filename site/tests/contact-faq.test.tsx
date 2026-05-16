import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import { FaqClient } from "@/app/faq/FaqClient";
import { ContactForm } from "@/app/contact/ContactForm";

describe("contact + faq", () => {
  it("FAQ search filters questions", async () => {
    render(<FaqClient />);
    expect(screen.getByText(/dependencies/i)).toBeInTheDocument();
    await userEvent.type(screen.getByRole("searchbox"), "deterministic");
    expect(screen.queryByText(/dependencies/i)).not.toBeInTheDocument();
  });
  it("Contact form blocks empty submit", async () => {
    render(<ContactForm />);
    await userEvent.click(screen.getByRole("button", { name: /send/i }));
    expect(screen.getByText(/please complete/i)).toBeInTheDocument();
  });
});
