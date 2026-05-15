import type { Metadata } from "next";
import { display, body, mono } from "./fonts";
import "./globals.css";
import { MotionProvider } from "@/motion/MotionProvider";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { ScrollToTop } from "@/components/layout/ScrollToTop";

export const metadata: Metadata = {
  title: "Precision Memory Agent",
  description: "Deterministic two-regime precision controller.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable} ${mono.variable} antialiased`}>
      <body>
        <MotionProvider>
          <Header />
          <main>{children}</main>
          <Footer />
          <ScrollToTop />
        </MotionProvider>
      </body>
    </html>
  );
}
