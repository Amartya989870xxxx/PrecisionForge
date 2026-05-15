"use client";
import dynamic from "next/dynamic";
import Link from "next/link";
import { Container } from "@/components/layout/Container";
import { useReducedMotion } from "@/motion/useReducedMotion";

const HeroScene = dynamic(() => import("@/three/HeroScene").then((m) => m.HeroScene), { ssr: false });

export function Hero() {
  const reduced = useReducedMotion();
  return (
    <section className="relative isolate min-h-[88vh] overflow-hidden">
      <div className="absolute inset-0 -z-10">
        {reduced ? (
          <div className="h-full w-full bg-[radial-gradient(ellipse_at_center,#1c1408_0%,#0b0b0c_70%)]" />
        ) : (
          <HeroScene />
        )}
      </div>
      <Container className="flex min-h-[88vh] flex-col items-center justify-center text-center">
        <h1 className="max-w-4xl font-display text-5xl font-bold leading-tight md:text-7xl">
          Precision where memory matters most
        </h1>
        <p className="mt-6 max-w-xl text-lg text-text-muted">
          A deterministic two-regime precision controller — NumPy only, no retraining.
        </p>
        <div className="mt-10 flex gap-4">
          <Link href="/method" className="rounded-md bg-accent px-6 py-3 font-medium text-bg">See the method</Link>
          <Link href="/modules" className="rounded-md border border-border px-6 py-3 font-medium text-text">Explore modules</Link>
        </div>
      </Container>
    </section>
  );
}
