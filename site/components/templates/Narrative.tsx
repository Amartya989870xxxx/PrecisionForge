import { Container } from "@/components/layout/Container";
import { Reveal } from "@/motion/Reveal";
import type { Narrative as N } from "@/content/narrative";
export function Narrative({ data }: { data: N }) {
  return (
    <>
      <section className="border-b border-border bg-surface py-32">
        <Container>
          <h1 className="font-display text-6xl">{data.title}</h1>
          <p className="mt-6 max-w-2xl text-xl text-text-muted">{data.lede}</p>
        </Container>
      </section>
      <Container className="py-24">
        <div className="space-y-24">
          {data.sections.map((s, i) => (
            <Reveal key={s.h}>
              <div className={`grid gap-10 md:grid-cols-2 ${i % 2 ? "md:[direction:rtl]" : ""}`}>
                <h2 className="font-display text-3xl [direction:ltr]">{s.h}</h2>
                <p className="text-lg text-text-muted [direction:ltr]">{s.p}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </Container>
    </>
  );
}
