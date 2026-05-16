"use client";
import { useState } from "react";
import { Container } from "@/components/layout/Container";
import { Accordion } from "@/components/ui/Accordion";
import { faq } from "@/content/faq";
export function FaqClient() {
  const [q, setQ] = useState("");
  const items = faq.filter((f) => (f.q + f.a).toLowerCase().includes(q.toLowerCase()));
  return (
    <Container className="py-24">
      <h1 className="font-display text-5xl">FAQ</h1>
      <input type="search" aria-label="Search FAQ" placeholder="Search…" value={q} onChange={(e) => setQ(e.target.value)}
        className="mt-8 w-full max-w-md rounded-md border border-border bg-surface px-4 py-3 outline-none focus:border-accent" />
      <div className="mt-8"><Accordion items={items} /></div>
    </Container>
  );
}
