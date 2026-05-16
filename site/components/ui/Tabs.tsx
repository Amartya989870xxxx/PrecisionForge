"use client";
import { useState } from "react";
export function Tabs({ tabs }: { tabs: { id: string; label: string; content: React.ReactNode }[] }) {
  const [active, setActive] = useState(tabs[0]?.id);
  return (
    <div>
      <div role="tablist" className="flex gap-2 border-b border-border">
        {tabs.map((t) => (
          <button key={t.id} role="tab" aria-selected={active === t.id} onClick={() => setActive(t.id)}
            className={`px-4 py-3 text-sm transition-colors duration-300 ${active === t.id ? "border-b-2 border-accent text-text" : "text-text-muted"}`}>
            {t.label}
          </button>
        ))}
      </div>
      <div role="tabpanel" className="pt-8">{tabs.find((t) => t.id === active)?.content}</div>
    </div>
  );
}
