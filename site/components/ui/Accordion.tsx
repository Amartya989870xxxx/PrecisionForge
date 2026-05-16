"use client";
import { useState } from "react";

export interface AccordionItem {
  id: string;
  q: string;
  a: string;
}

export interface AccordionProps {
  items: AccordionItem[];
}

export function Accordion({ items }: AccordionProps) {
  const [open, setOpen] = useState<string | null>(null);
  return (
    <div className="divide-y divide-border border-y border-border">
      {items.map((it) => {
        const isOpen = open === it.id;
        return (
          <div key={it.id}>
            <button
              className="flex w-full items-center justify-between py-5 text-left font-medium"
              aria-expanded={isOpen}
              aria-controls={`acc-${it.id}`}
              onClick={() => setOpen(isOpen ? null : it.id)}
            >
              {it.q}
              <span aria-hidden="true" className={`transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`}>▾</span>
            </button>
            <div id={`acc-${it.id}`} hidden={!isOpen} className="pb-5 text-sm text-text-muted">{it.a}</div>
          </div>
        );
      })}
    </div>
  );
}
