import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import { Accordion } from "@/components/ui/Accordion";
import { Tabs } from "@/components/ui/Tabs";
import { FilterRail } from "@/components/ui/FilterRail";

describe("UI kit logic", () => {
  it("Accordion toggles a panel", async () => {
    render(<Accordion items={[{ id: "a", q: "Q1", a: "A1" }]} />);
    expect(screen.queryByText("A1")).not.toBeVisible();
    await userEvent.click(screen.getByRole("button", { name: "Q1" }));
    expect(screen.getByText("A1")).toBeVisible();
  });
  it("Tabs switches active panel", async () => {
    render(<Tabs tabs={[{ id: "x", label: "X", content: <p>xc</p> }, { id: "y", label: "Y", content: <p>yc</p> }]} />);
    expect(screen.getByText("xc")).toBeInTheDocument();
    await userEvent.click(screen.getByRole("tab", { name: "Y" }));
    expect(screen.getByText("yc")).toBeInTheDocument();
  });
  it("FilterRail emits selection", async () => {
    let selected = "";
    render(<FilterRail options={[{ id: "all", label: "All" }, { id: "ret", label: "Retrieval" }]} value="all" onChange={(v) => (selected = v)} />);
    await userEvent.click(screen.getByRole("radio", { name: "Retrieval" }));
    expect(selected).toBe("ret");
  });
});
