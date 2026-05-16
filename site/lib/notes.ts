import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
const DIR = path.join(process.cwd(), "content/notes");
export type Note = { slug: string; title: string; date: string; kind: "Guides" | "News" };
export function getNotes(): Note[] {
  return fs.readdirSync(DIR).filter((f) => f.endsWith(".mdx")).map((f) => {
    const { data } = matter(fs.readFileSync(path.join(DIR, f), "utf8"));
    return { slug: f.replace(/\.mdx$/, ""), title: data.title, date: data.date, kind: data.kind };
  }).sort((a, b) => b.date.localeCompare(a.date));
}
