import Link from "next/link";
import { Container } from "./Container";
import { footerCols } from "@/lib/nav";

export function Footer() {
  return (
    <footer className="mt-32 border-t border-border bg-surface py-16">
      <Container className="grid grid-cols-2 gap-10 md:grid-cols-5">
        {footerCols.map((c) => (
          <div key={c.heading}>
            <h3 className="mb-4 font-display text-sm font-semibold text-text">{c.heading}</h3>
            <ul className="space-y-2">
              {c.links.map((l) => (
                <li key={l.href}><Link href={l.href} className="text-sm text-text-muted hover:text-text">{l.label}</Link></li>
              ))}
            </ul>
          </div>
        ))}
      </Container>
      <Container className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-border pt-6 text-xs text-text-muted md:flex-row">
        <span>© {new Date().getFullYear()} Precision Memory Agent</span>
        <Link href="/legal" className="hover:text-text">Privacy &amp; Terms</Link>
      </Container>
    </footer>
  );
}
