import Link from "next/link";
import { Container } from "@/components/layout/Container";
import { Tabs } from "@/components/ui/Tabs";
import { getNotes } from "@/lib/notes";
export const metadata = { title: "Notes — Precision Memory Agent" };
function List({ kind }: { kind?: string }) {
  const notes = getNotes().filter((n) => !kind || n.kind === kind);
  return <ul className="mt-6 space-y-4">{notes.map((n) => (
    <li key={n.slug}><Link href={`/notes/${n.slug}`} className="text-lg hover:text-accent">{n.title}</Link>
      <span className="ml-3 text-xs text-text-muted">{n.date}</span></li>
  ))}</ul>;
}
export default function NotesPage() {
  return (
    <Container className="py-24">
      <h1 className="font-display text-5xl">Notes</h1>
      <div className="mt-10">
        <Tabs tabs={[
          { id: "all", label: "All", content: <List /> },
          { id: "g", label: "Guides", content: <List kind="Guides" /> },
          { id: "n", label: "News", content: <List kind="News" /> },
        ]} />
      </div>
    </Container>
  );
}
