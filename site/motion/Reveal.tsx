"use client";
import { motion } from "framer-motion";
import { fadeUp } from "./variants";
import { useReducedMotion } from "./useReducedMotion";

export function Reveal({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  const reduced = useReducedMotion();
  if (reduced) return <div className={className}>{children}</div>;
  return (
    <motion.div className={className} variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }}>
      {children}
    </motion.div>
  );
}
