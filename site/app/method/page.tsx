import { Narrative } from "@/components/templates/Narrative";
import { getNarrative } from "@/lib/content";
export const metadata = { title: "Method — Precision Memory Agent" };
export default function Page() { return <Narrative data={getNarrative("method")!} />; }
