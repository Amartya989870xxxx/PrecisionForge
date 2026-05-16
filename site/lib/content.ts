import { modules, type Module } from "@/content/modules";
import { narratives, type Narrative } from "@/content/narrative";
export const getModules = (): Module[] => modules;
export const getModule = (slug: string): Module | undefined => modules.find((m) => m.slug === slug);
export const getNarrative = (slug: string): Narrative | undefined => narratives.find((n) => n.slug === slug);
