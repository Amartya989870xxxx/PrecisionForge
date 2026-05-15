import { Space_Grotesk, Inter, JetBrains_Mono } from "next/font/google";

// Variable Google fonts: omitting `weight` loads the full variable weight axis (300–700).
export const display = Space_Grotesk({ subsets: ["latin"], variable: "--font-display", display: "swap" });
export const body = Inter({ subsets: ["latin"], variable: "--font-body", display: "swap" });
export const mono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono", display: "swap" });
