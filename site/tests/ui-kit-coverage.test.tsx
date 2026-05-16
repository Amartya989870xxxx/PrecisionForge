import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Field } from "@/components/ui/Field";
import { Tabs } from "@/components/ui/Tabs";
import { FilterRail } from "@/components/ui/FilterRail";
import { Accordion } from "@/components/ui/Accordion";

describe("Button", () => {
  it("renders an anchor in link mode", () => {
    render(<Button href="/x">go</Button>);
    const link = screen.getByRole("link", { name: "go" });
    expect(link).toBeInTheDocument();
    expect(link.tagName).toBe("A");
  });

  it("renders a button with the given type and fires onClick", async () => {
    const onClick = vi.fn();
    render(<Button type="submit" onClick={onClick}>save</Button>);
    const btn = screen.getByRole("button", { name: "save" });
    expect(btn).toHaveAttribute("type", "submit");
    await userEvent.click(btn);
    expect(onClick).toHaveBeenCalledOnce();
  });

  it("applies primary vs ghost variant classes", () => {
    const { rerender } = render(<Button>primary</Button>);
    expect(screen.getByRole("button", { name: "primary" }).className).toContain("bg-accent");
    rerender(<Button variant="ghost">ghost</Button>);
    expect(screen.getByRole("button", { name: "ghost" }).className).toContain("border-border");
  });
});

describe("Card", () => {
  it("wraps in a link when href is given", () => {
    render(<Card title="T" body="B" href="/c" />);
    expect(screen.getByRole("link")).toBeInTheDocument();
    expect(screen.getByText("T")).toBeInTheDocument();
  });

  it("renders a bare div without href", () => {
    render(<Card title="T2" body="B2" />);
    expect(screen.queryByRole("link")).not.toBeInTheDocument();
    expect(screen.getByText("B2")).toBeInTheDocument();
  });
});

describe("Field", () => {
  it("renders an input by default", () => {
    render(<Field label="Email" name="email" type="email" />);
    const input = document.querySelector("input[name='email']") as HTMLInputElement;
    expect(input).toBeInTheDocument();
    expect(input.type).toBe("email");
  });

  it("renders a textarea and a required marker", () => {
    render(<Field label="Msg" name="msg" textarea required />);
    expect(document.querySelector("textarea[name='msg']")).toBeInTheDocument();
    expect(screen.getByText(/Msg/).textContent).toContain("*");
  });
});

describe("Tabs a11y + keyboard", () => {
  const tabs = [
    { id: "x", label: "X", content: <p>xc</p> },
    { id: "y", label: "Y", content: <p>yc</p> },
  ];

  it("wires aria-controls / aria-labelledby / roving tabindex", () => {
    render(<Tabs tabs={tabs} />);
    const tabX = screen.getByRole("tab", { name: "X" });
    expect(tabX).toHaveAttribute("aria-controls", "panel-x");
    expect(tabX).toHaveAttribute("tabindex", "0");
    expect(screen.getByRole("tab", { name: "Y" })).toHaveAttribute("tabindex", "-1");
    const panel = screen.getByRole("tabpanel");
    expect(panel).toHaveAttribute("aria-labelledby", "tab-x");
  });

  it("ArrowRight / ArrowLeft move the active tab", async () => {
    render(<Tabs tabs={tabs} />);
    // Per the WAI-ARIA pattern, focus is on the active tab; the handler is on
    // the tablist and receives the event via bubbling.
    screen.getByRole("tab", { name: "X" }).focus();
    await userEvent.keyboard("{ArrowRight}");
    expect(screen.getByText("yc")).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: "Y" })).toHaveAttribute("aria-selected", "true");
    await userEvent.keyboard("{ArrowLeft}");
    expect(screen.getByText("xc")).toBeInTheDocument();
    await userEvent.keyboard("{ArrowLeft}");
    expect(screen.getByText("yc")).toBeInTheDocument();
  });
});

describe("FilterRail a11y", () => {
  it("uses radiogroup / radio roles and aria-checked", async () => {
    let selected = "";
    render(
      <FilterRail
        options={[{ id: "all", label: "All" }, { id: "ret", label: "Retrieval" }]}
        value="all"
        onChange={(v) => (selected = v)}
      />,
    );
    expect(screen.getByRole("radiogroup", { name: "Filter" })).toBeInTheDocument();
    const all = screen.getByRole("radio", { name: "All" });
    expect(all).toHaveAttribute("aria-checked", "true");
    await userEvent.click(screen.getByRole("radio", { name: "Retrieval" }));
    expect(selected).toBe("ret");
  });
});

describe("Accordion a11y", () => {
  it("wires aria-controls and panel id", () => {
    render(<Accordion items={[{ id: "a", q: "Q1", a: "A1" }]} />);
    const btn = screen.getByRole("button", { name: "Q1" });
    expect(btn).toHaveAttribute("aria-controls", "acc-a");
    const panel = document.getElementById("acc-a");
    expect(panel).toBeInTheDocument();
    expect(panel).toHaveTextContent("A1");
  });
});
