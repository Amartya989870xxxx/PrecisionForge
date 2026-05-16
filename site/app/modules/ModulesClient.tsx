"use client";
import { useState } from "react";
import { Container } from "@/components/layout/Container";
import { FilterRail } from "@/components/ui/FilterRail";
import { Card } from "@/components/ui/Card";
import { getModules } from "@/lib/content";
const opts = [
  { id: "all", label: "All" }, { id: "Retrieval", label: "Retrieval" },
  { id: "Anisotropy", label: "Anisotropy" }, { id: "Robustness", label: "Robustness" }, { id: "Tools", label: "Tools" },
];
export function ModulesClient() {
  const [f, setF] = useState("all");
  const mods = getModules().filter((m) => f === "all" || m.domain === f);
  return (
    <Container className="grid gap-10 py-20 md:grid-cols-[220px_1fr]">
      <FilterRail options={opts} value={f} onChange={setF} />
      <div className="grid gap-6 sm:grid-cols-2">
        {mods.map((m) => <Card key={m.slug} title={m.title} body={m.summary} href={`/modules/${m.slug}`} />)}
      </div>
    </Container>
  );
}
