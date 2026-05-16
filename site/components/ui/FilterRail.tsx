"use client";
export function FilterRail({ options, value, onChange }: { options: { id: string; label: string }[]; value: string; onChange: (v: string) => void }) {
  return (
    <div className="flex flex-wrap gap-2 md:flex-col">
      {options.map((o) => (
        <button key={o.id} onClick={() => onChange(o.id)}
          className={`rounded-md px-4 py-2 text-left text-sm transition-colors duration-300 ${value === o.id ? "bg-accent text-bg" : "border border-border text-text-muted hover:text-text"}`}>
          {o.label}
        </button>
      ))}
    </div>
  );
}
