import Link from "next/link";

export interface CardProps {
  title: string;
  body: string;
  href?: string;
}

export function Card({ title, body, href }: CardProps) {
  const inner = (
    <div className="group h-full rounded-lg border border-border bg-surface p-6 transition-transform duration-300 ease-brand hover:-translate-y-1">
      <h3 className="font-display text-xl font-semibold">{title}</h3>
      <p className="mt-3 text-sm text-text-muted">{body}</p>
    </div>
  );
  return href ? <Link href={href}>{inner}</Link> : inner;
}
