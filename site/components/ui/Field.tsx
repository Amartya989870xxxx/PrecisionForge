export interface FieldProps {
  label: string;
  name: string;
  type?: React.HTMLInputTypeAttribute;
  required?: boolean;
  textarea?: boolean;
}

export function Field({ label, name, type = "text", required = false, textarea = false }: FieldProps) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm text-text-muted">{label}{required && " *"}</span>
      {textarea ? (
        <textarea name={name} required={required} rows={5} className="w-full rounded-md border border-border bg-surface px-4 py-3 outline-none focus:border-accent" />
      ) : (
        <input name={name} type={type} required={required} className="w-full rounded-md border border-border bg-surface px-4 py-3 outline-none focus:border-accent" />
      )}
    </label>
  );
}
