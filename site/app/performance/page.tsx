import { Narrative } from "@/components/templates/Narrative";
import { getNarrative } from "@/lib/content";
export const metadata = { title: "Performance — Precision Memory Agent" };
export default function Page() { return <Narrative data={getNarrative("performance")!} />; }
