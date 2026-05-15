import type { Metadata } from "next";
import { display, body, mono } from "./fonts";
import "./globals.css";

export const metadata: Metadata = {
  title: "Precision Memory Agent",
  description: "Deterministic two-regime precision controller.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable} ${mono.variable} antialiased`}>
      <body>{children}</body>
    </html>
  );
}
