"use client";
import { useRef, useState } from "react";

export interface TabItem {
  id: string;
  label: string;
  content: React.ReactNode;
}

export interface TabsProps {
  tabs: TabItem[];
}

export function Tabs({ tabs }: TabsProps) {
  const [active, setActive] = useState(tabs[0]?.id);
  const btnRefs = useRef<Record<string, HTMLButtonElement | null>>({});

  const onKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
    e.preventDefault();
    const idx = tabs.findIndex((t) => t.id === active);
    if (idx === -1) return;
    const nextIdx = e.key === "ArrowRight" ? (idx + 1) % tabs.length : (idx - 1 + tabs.length) % tabs.length;
    const next = tabs[nextIdx];
    setActive(next.id);
    btnRefs.current[next.id]?.focus();
  };

  return (
    <div>
      <div role="tablist" className="flex gap-2 border-b border-border" onKeyDown={onKeyDown}>
        {tabs.map((t) => (
          <button
            key={t.id}
            id={`tab-${t.id}`}
            ref={(el) => {
              btnRefs.current[t.id] = el;
            }}
            role="tab"
            aria-selected={active === t.id}
            aria-controls={`panel-${t.id}`}
            tabIndex={active === t.id ? 0 : -1}
            onClick={() => setActive(t.id)}
            className={`px-4 py-3 text-sm transition-colors duration-300 ${active === t.id ? "border-b-2 border-accent text-text" : "text-text-muted"}`}
          >
            {t.label}
          </button>
        ))}
      </div>
      <div
        id={`panel-${active}`}
        role="tabpanel"
        aria-labelledby={`tab-${active}`}
        tabIndex={0}
        className="pt-8"
      >
        {tabs.find((t) => t.id === active)?.content}
      </div>
    </div>
  );
}
