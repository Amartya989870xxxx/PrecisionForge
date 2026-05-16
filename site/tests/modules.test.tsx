import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import { ModulesClient } from "@/app/modules/ModulesClient";

describe("modules index", () => {
  it("filters by domain", async () => {
    render(<ModulesClient />);
    expect(screen.getByText("Geometry Branch")).toBeInTheDocument();
    await userEvent.click(screen.getByRole("radio", { name: "Retrieval" }));
    expect(screen.queryByText("Geometry Branch")).not.toBeInTheDocument();
    expect(screen.getByText("Corruption-Map Controller")).toBeInTheDocument();
  });
});
