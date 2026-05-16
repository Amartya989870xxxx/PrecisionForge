import { Container } from "@/components/layout/Container";
export const metadata = { title: "Privacy & Terms — Precision Memory Agent" };
export default function LegalPage() {
  return (
    <Container className="prose-invert max-w-2xl py-24">
      <h1 className="font-display text-4xl">Privacy &amp; Terms</h1>
      <p className="mt-6 text-text-muted">This site presents an original research project. It collects no personal data beyond any message you choose to submit via the contact form, which is sent only to the configured project endpoint.</p>
    </Container>
  );
}
