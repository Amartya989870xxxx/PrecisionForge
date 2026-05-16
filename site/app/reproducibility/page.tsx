import { Narrative } from "@/components/templates/Narrative";
import { getNarrative } from "@/lib/content";
export const metadata = { title: "Reproducibility — Precision Memory Agent" };
export default function Page() { return <Narrative data={getNarrative("reproducibility")!} />; }
