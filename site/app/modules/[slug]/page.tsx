import { notFound } from "next/navigation";
import { Container } from "@/components/layout/Container";
import { getModules, getModule } from "@/lib/content";
export function generateStaticParams() { return getModules().map((m) => ({ slug: m.slug })); }
export default async function ModuleDetail({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const m = getModule(slug);
  if (!m) notFound();
  return (
    <Container className="py-24">
      <p className="text-sm text-text-muted">Modules / {m.domain}</p>
      <h1 className="mt-3 font-display text-5xl">{m.title}</h1>
      <p className="mt-6 max-w-2xl text-lg text-text-muted">{m.summary}</p>
      <div className="mt-10 max-w-3xl border-t border-border pt-10">{m.detail}</div>
    </Container>
  );
}
