"use client";

export interface FilterOption {
  id: string;
  label: string;
}

export interface FilterRailProps {
  options: FilterOption[];
  value: string;
  onChange: (v: string) => void;
}

export function FilterRail({ options, value, onChange }: FilterRailProps) {
  return (
    <div role="radiogroup" aria-label="Filter" className="flex flex-wrap gap-2 md:flex-col">
      {options.map((o) => (
        <button
          key={o.id}
          role="radio"
          aria-checked={value === o.id}
          onClick={() => onChange(o.id)}
          className={`rounded-md px-4 py-2 text-left text-sm transition-colors duration-300 ${value === o.id ? "bg-accent text-bg" : "border border-border text-text-muted hover:text-text"}`}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}
