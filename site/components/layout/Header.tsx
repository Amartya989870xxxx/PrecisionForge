import Link from "next/link";
import { Container } from "./Container";
import { primaryNav, utilityNav } from "@/lib/nav";

export function Header() {
  return (
    <header className="relative z-30 py-6">
      <Container className="flex items-center justify-between gap-6">
        <Link href="/" className="font-display text-lg font-bold tracking-tight">Precision Memory Agent</Link>
        <nav aria-label="Primary" className="hidden gap-7 md:flex">
          {primaryNav.map((i) => (
            <Link key={i.href} href={i.href} className="text-sm text-text-muted transition-colors duration-300 ease-brand hover:text-text">{i.label}</Link>
          ))}
        </nav>
        <nav aria-label="Utility" className="flex items-center gap-4">
          {utilityNav.map((i) => (
            <Link key={i.href} href={i.href} className="text-sm font-medium text-text">{i.label}</Link>
          ))}
        </nav>
      </Container>
    </header>
  );
}
