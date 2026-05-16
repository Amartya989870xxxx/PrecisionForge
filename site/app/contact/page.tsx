import { Container } from "@/components/layout/Container";
import { ContactForm } from "./ContactForm";
export const metadata = { title: "Contact — Precision Memory Agent" };
export default function ContactPage() {
  return (
    <Container className="grid gap-16 py-24 md:grid-cols-2">
      <div><h1 className="font-display text-5xl">Contact</h1><p className="mt-6 text-text-muted">Questions about the controller or reproducibility? Send a note.</p></div>
      <ContactForm />
    </Container>
  );
}
