"use client";
import { useEffect } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "./useReducedMotion";

export function MotionProvider({ children }: { children: React.ReactNode }) {
  const reduced = useReducedMotion();
  useEffect(() => {
    if (reduced) return;
    gsap.registerPlugin(ScrollTrigger);
    let lenis: import("lenis").default | undefined;
    let raf = 0;
    let cancelled = false;
    (async () => {
      const Lenis = (await import("lenis")).default;
      if (cancelled) return;
      lenis = new Lenis({ lerp: 0.1, duration: 1.2 });
      lenis.on("scroll", ScrollTrigger.update);
      const loop = (t: number) => { lenis?.raf(t); raf = requestAnimationFrame(loop); };
      raf = requestAnimationFrame(loop);
    })();
    return () => { cancelled = true; cancelAnimationFrame(raf); lenis?.destroy(); ScrollTrigger.getAll().forEach((t) => t.kill()); };
  }, [reduced]);
  return <>{children}</>;
}
