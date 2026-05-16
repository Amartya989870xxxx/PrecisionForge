import { Container } from "@/components/layout/Container";
import { ReadingProgress } from "@/components/notes/ReadingProgress";
import { getNotes } from "@/lib/notes";
export function generateStaticParams() { return getNotes().map((n) => ({ slug: n.slug })); }
export default async function NotePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const { default: MDX } = await import(`@/content/notes/${slug}.mdx`);
  return (
    <>
      <ReadingProgress />
      <Container className="prose-invert mx-auto max-w-2xl py-24">
        <article className="space-y-5 leading-relaxed"><MDX /></article>
      </Container>
    </>
  );
}
