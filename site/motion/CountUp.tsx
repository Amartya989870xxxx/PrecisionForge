"use client";
import { useEffect, useRef, useState } from "react";
import { useReducedMotion } from "./useReducedMotion";

export interface CountUpProps {
  to: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
}

export function CountUp({ to, prefix = "", suffix = "", decimals = 2 }: CountUpProps) {
  const reduced = useReducedMotion();
  const [val, setVal] = useState(() => (reduced ? to : 0));
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    if (reduced) return;
    const el = ref.current;
    if (!el) return;

    let rafId = 0;
    let start: number | null = null;

    const io = new IntersectionObserver(
      (entries) => {
        if (!entries[0].isIntersecting) return;
        io.disconnect();
        const tick = (t: number) => {
          if (start === null) start = t;
          const p = Math.min(1, (t - start) / 900);
          setVal(to * (1 - Math.pow(1 - p, 3)));
          if (p < 1) rafId = requestAnimationFrame(tick);
        };
        rafId = requestAnimationFrame(tick);
      },
      { threshold: 0.5 },
    );
    io.observe(el);

    return () => {
      io.disconnect();
      cancelAnimationFrame(rafId);
    };
  }, [to, reduced]);

  // Reduced-motion: render the final value without a setState-in-effect.
  const display = reduced ? to : val;
  return (
    <span ref={ref}>
      {prefix}
      {display.toFixed(decimals)}
      {suffix}
    </span>
  );
}
