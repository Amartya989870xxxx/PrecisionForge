import { display, body, mono } from "./fonts";
import "./globals.css";

export const metadata = { title: "Precision Memory Agent", description: "Deterministic two-regime precision controller." };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable} ${mono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
