import Link from "next/link";
import { Hero } from "@/components/sections/Hero";
import { Container } from "@/components/layout/Container";
import { Reveal } from "@/motion/Reveal";
import { Stagger, StaggerItem } from "@/motion/Stagger";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { CountUp } from "@/motion/CountUp";

const modules = [
  {
    title: "Anvil-P-E",
    body: "Benchmark and evaluation harness that scores the controller across seeds with no per-seed regression.",
    href: "/modules",
  },
  {
    title: "w Adapter (Engine)",
    body: "Single-file deterministic adapter — NumPy, stored patterns, frozen params. No retraining, no external state.",
    href: "/modules",
  },
  {
    title: "Corruption-Map Controller",
    body: "Estimates likely-masked coordinates from per-coordinate magnitude and raises their precision so the gradient refills missing signal.",
    href: "/modules",
  },
  {
    title: "Geometry Branch",
    body: "Hessian-aware diagonal preconditioner for near-clean probes; non-SPD Hessians are PSD-regularised, never degenerating to identity.",
    href: "/modules",
  },
];

const results = [
  { label: "Mean Δ accuracy", to: 0.142, prefix: "+", decimals: 3 },
  { label: "Min Δ accuracy", to: 0.047, prefix: "+", decimals: 3 },
  { label: "Mean spread reduction", to: 1.03, suffix: "×", decimals: 2 },
  { label: "Total automated", to: 70.22, suffix: " / 90", decimals: 2 },
];

const approach = [
  { title: "Method", body: "Two regimes, one principled controller — corruption-map precision and Hessian isotropisation.", href: "/method" },
  { title: "Performance", body: "Honest, reproducible figures from the public self-check, including the anisotropy ceiling.", href: "/performance" },
  { title: "Reproducibility", body: "Deterministic output, cached per attractor, runnable from a single adapter entry point.", href: "/reproducibility" },
];

export default function Home() {
  return (
    <>
      <Hero />

      <Container className="py-28">
        <Reveal>
          <p className="max-w-3xl font-display text-3xl leading-snug md:text-4xl">
            One controller, two regimes: it refills corrupted memory and isotropises
            near-clean geometry — deterministically, with NumPy alone.
            <Link href="/method" className="ml-3 text-accent">Read the method →</Link>
          </p>
        </Reveal>
      </Container>

      <Container className="py-12">
        <h2 className="mb-10 font-display text-2xl text-text-muted">Core modules</h2>
        <Stagger className="grid gap-6 md:grid-cols-4">
          {modules.map((m) => (
            <StaggerItem key={m.title}>
              <Card title={m.title} body={m.body} href={m.href} />
            </StaggerItem>
          ))}
        </Stagger>
        <div className="mt-10">
          <Button href="/modules" variant="ghost">See all modules</Button>
        </div>
      </Container>

      <section className="border-y border-border bg-surface py-24">
        <Container>
          <h2 className="mb-12 text-center font-display text-2xl text-text-muted">
            Public self-check — honest results
          </h2>
          <div className="grid gap-10 sm:grid-cols-2 md:grid-cols-4">
            {results.map((r) => (
              <div key={r.label} className="text-center">
                <div className="font-display text-4xl font-bold text-accent">
                  <CountUp to={r.to} prefix={r.prefix ?? ""} suffix={r.suffix ?? ""} decimals={r.decimals} />
                </div>
                <div className="mt-2 text-sm text-text-muted">{r.label}</div>
              </div>
            ))}
          </div>
          <p className="mx-auto mt-12 max-w-2xl text-center text-xs text-text-muted">
            A ≥10× spread reduction is not reachable by any diagonal precision vector on the
            public synthetic operator — a property of the operator, not a solver limitation.
            The geometry branch reports its true ceiling here while remaining the correct
            construction for the anisotropic held-out evaluation.
          </p>
        </Container>
      </section>

      <Container className="py-24">
        <Stagger className="grid gap-6 md:grid-cols-3">
          {approach.map((a) => (
            <StaggerItem key={a.title}>
              <Card title={a.title} body={a.body} href={a.href} />
            </StaggerItem>
          ))}
        </Stagger>
      </Container>

      <Container className="py-28 text-center">
        <Reveal>
          <h2 className="font-display text-4xl">Want the full method?</h2>
          <p className="mx-auto mt-4 max-w-xl text-text-muted">
            Read how the two-regime controller is constructed, or explore the modules.
          </p>
          <div className="mt-10 flex justify-center gap-4">
            <Button href="/method">Read the method</Button>
            <Button href="/contact" variant="ghost">Contact</Button>
          </div>
        </Reveal>
      </Container>
    </>
  );
}
