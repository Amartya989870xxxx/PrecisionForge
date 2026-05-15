# Precision Memory Agent Site — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a premium, animation-rich Next.js marketing/docs site for the Precision Memory Agent project, recreating coffee-tech.com's layout/motion as a structural reference only with 100% original branding and content.

**Architecture:** Next.js 15 App Router + TypeScript, static-export compatible, in the `site/` subfolder. Brand is token-driven (one CSS-variable file). Motion stack: Lenis (scroll) + Framer Motion (reveal/stagger/route) + GSAP/ScrollTrigger (pin/scrub) + Swiper (carousels) + @react-three/fiber (procedural hero). Phased build: foundation → shared systems → pages → QA.

**Tech Stack:** next, react, typescript, tailwindcss, framer-motion, gsap, lenis, swiper, three, @react-three/fiber, @react-three/drei, @react-three/postprocessing, @next/mdx, vitest, @testing-library/react, playwright.

**Reference/IP boundary (binding):** Recreate layout/section/motion *patterns* only. Never reproduce the reference site's copy, media, product names, or logo. All content is original, derived from this repo's `w/README.md`. See spec §2.

**Spec:** `docs/superpowers/specs/2026-05-16-precision-memory-agent-site-design.md`

**Working dir for all paths below:** `/Users/aks/Precision_Memory_Agent/`. App lives at `site/`. Run app commands from `site/`.

---

## Phase 0 — Foundation (sequential; blocks all other phases)

### Task 0.1: Scaffold Next.js app

**Files:**
- Create: `site/` (entire Next.js scaffold)

- [ ] **Step 1: Scaffold**

Run from repo root:
```bash
npx create-next-app@latest site --typescript --tailwind --eslint --app --src-dir=false --import-alias "@/*" --use-npm --no-turbopack
```
Accept defaults for any extra prompts.

- [ ] **Step 2: Verify dev server boots**

```bash
cd site && npm run dev &
sleep 8 && curl -sf http://localhost:3000 >/dev/null && echo "DEV OK" ; kill %1
```
Expected: `DEV OK`

- [ ] **Step 3: Verify production build**

Run: `cd site && npm run build`
Expected: build completes with no errors.

- [ ] **Step 4: Commit**

```bash
git add site && git commit -m "feat: scaffold Next.js app for Precision Memory Agent site"
```

### Task 0.2: Install dependencies

**Files:** Modify: `site/package.json`

- [ ] **Step 1: Install runtime + dev deps**

```bash
cd site
npm i framer-motion gsap lenis swiper three @react-three/fiber @react-three/drei @react-three/postprocessing
npm i @next/mdx @mdx-js/loader @mdx-js/react gray-matter
npm i -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom @vitejs/plugin-react vite-tsconfig-paths @playwright/test
```

- [ ] **Step 2: Verify install + build still green**

Run: `cd site && npm run build`
Expected: build succeeds.

- [ ] **Step 3: Commit**

```bash
git add site/package.json site/package-lock.json && git commit -m "chore: add motion, 3D, MDX, and test dependencies"
```

### Task 0.3: Test harness (Vitest + RTL)

**Files:**
- Create: `site/vitest.config.ts`
- Create: `site/vitest.setup.ts`
- Create: `site/tests/smoke.test.tsx`
- Modify: `site/package.json` (scripts)

- [ ] **Step 1: Write the failing test**

`site/tests/smoke.test.tsx`:
```tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

function Hello() {
  return <h1>Precision Memory Agent</h1>;
}

describe("test harness", () => {
  it("renders a component", () => {
    render(<Hello />);
    expect(screen.getByRole("heading", { name: "Precision Memory Agent" })).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Add config + setup**

`site/vitest.config.ts`:
```ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    environment: "jsdom",
    setupFiles: ["./vitest.setup.ts"],
    globals: true,
    css: false,
    coverage: { reporter: ["text", "lcov"], lines: 80, functions: 80 },
  },
});
```

`site/vitest.setup.ts`:
```ts
import "@testing-library/jest-dom/vitest";
import { vi } from "vitest";

// jsdom lacks matchMedia; default to "no reduced motion".
window.matchMedia =
  window.matchMedia ||
  ((query: string) =>
    ({
      matches: false,
      media: query,
      onchange: null,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      addListener: vi.fn(),
      removeListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }) as unknown as MediaQueryList);

window.scrollTo = vi.fn();
```

Add to `site/package.json` `"scripts"`:
```json
"test": "vitest run",
"test:watch": "vitest",
"e2e": "playwright test"
```

- [ ] **Step 3: Run test to verify it passes**

Run: `cd site && npm test`
Expected: 1 passed.

- [ ] **Step 4: Commit**

```bash
git add site && git commit -m "test: add Vitest + RTL harness with reduced-motion matchMedia mock"
```

### Task 0.4: Design tokens + fonts + Tailwind wiring

**Files:**
- Create: `site/styles/tokens.css`
- Create: `site/app/fonts.ts`
- Modify: `site/app/globals.css`
- Modify: `site/tailwind.config.ts`
- Modify: `site/app/layout.tsx`
- Create: `site/tests/tokens.test.tsx`

- [ ] **Step 1: Write the failing test**

`site/tests/tokens.test.tsx`:
```tsx
import { render } from "@testing-library/react";
import { describe, it, expect } from "vitest";

describe("design tokens", () => {
  it("exposes accent token class", () => {
    const { container } = render(<div className="text-accent">x</div>);
    expect(container.firstChild).toHaveClass("text-accent");
  });
});
```

- [ ] **Step 2: Create tokens**

`site/styles/tokens.css`:
```css
:root {
  --bg: #0b0b0c;
  --surface: #15161a;
  --text: #f4f4f5;
  --text-muted: #8a8a93;
  --accent: #f5a524;
  --accent-2: #c9821b;
  --border: rgba(255, 255, 255, 0.08);
  --container-max: 1280px;
  --gutter: 24px;
  --side-pad: 20px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 14px;
  --ease: cubic-bezier(0.22, 1, 0.36, 1);
}
@media (min-width: 768px) {
  :root { --side-pad: 40px; }
}
```

`site/app/fonts.ts`:
```ts
import { Space_Grotesk, Inter, JetBrains_Mono } from "next/font/google";

export const display = Space_Grotesk({ subsets: ["latin"], variable: "--font-display", display: "swap" });
export const body = Inter({ subsets: ["latin"], variable: "--font-body", display: "swap" });
export const mono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono", display: "swap" });
```

Replace `site/app/globals.css` content with:
```css
@import "../styles/tokens.css";
@tailwind base;
@tailwind components;
@tailwind utilities;

html { scroll-behavior: auto; }
body { background: var(--bg); color: var(--text); font-family: var(--font-body), system-ui, sans-serif; }
h1,h2,h3,h4 { font-family: var(--font-display), system-ui, sans-serif; }
@media (prefers-reduced-motion: reduce) {
  *,*::before,*::after { animation-duration: .001ms !important; transition-duration: .001ms !important; }
}
```

`site/tailwind.config.ts` — set `theme.extend`:
```ts
import type { Config } from "tailwindcss";
const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "var(--bg)", surface: "var(--surface)", text: "var(--text)",
        "text-muted": "var(--text-muted)", accent: "var(--accent)",
        "accent-2": "var(--accent-2)", border: "var(--border)",
      },
      fontFamily: {
        display: ["var(--font-display)", "system-ui", "sans-serif"],
        body: ["var(--font-body)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
      maxWidth: { container: "var(--container-max)" },
      transitionTimingFunction: { brand: "cubic-bezier(0.22,1,0.36,1)" },
    },
  },
  plugins: [],
};
export default config;
```

In `site/app/layout.tsx` import fonts and apply variable classes to `<html>`:
```tsx
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
```

- [ ] **Step 3: Run test + build**

Run: `cd site && npm test && npm run build`
Expected: tests pass, build succeeds.

- [ ] **Step 4: Commit**

```bash
git add site && git commit -m "feat: add design tokens, brand fonts, Tailwind token wiring"
```

### Task 0.5: MotionProvider (Lenis + GSAP registry + reduced-motion)

**Files:**
- Create: `site/motion/useReducedMotion.ts`
- Create: `site/motion/MotionProvider.tsx`
- Create: `site/tests/motion-provider.test.tsx`

- [ ] **Step 1: Write the failing test**

`site/tests/motion-provider.test.tsx`:
```tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { MotionProvider } from "@/motion/MotionProvider";

describe("MotionProvider", () => {
  it("renders children", () => {
    render(<MotionProvider><p>child</p></MotionProvider>);
    expect(screen.getByText("child")).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/motion-provider.test.tsx`
Expected: FAIL — cannot resolve `@/motion/MotionProvider`.

- [ ] **Step 3: Implement**

`site/motion/useReducedMotion.ts`:
```ts
"use client";
import { useEffect, useState } from "react";

export function useReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReduced(mq.matches);
    update();
    mq.addEventListener("change", update);
    return () => mq.removeEventListener("change", update);
  }, []);
  return reduced;
}
```

`site/motion/MotionProvider.tsx`:
```tsx
"use client";
import { useEffect } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "./useReducedMotion";

export function MotionProvider({ children }: { children: React.ReactNode }) {
  const reduced = useReducedMotion();
  useEffect(() => {
    if (reduced) return;
    gsap.registerPlugin(ScrollTrigger);
    let lenis: import("lenis").default | undefined;
    let raf = 0;
    let cancelled = false;
    (async () => {
      const Lenis = (await import("lenis")).default;
      if (cancelled) return;
      lenis = new Lenis({ lerp: 0.1, duration: 1.2 });
      lenis.on("scroll", ScrollTrigger.update);
      const loop = (t: number) => { lenis?.raf(t); raf = requestAnimationFrame(loop); };
      raf = requestAnimationFrame(loop);
    })();
    return () => { cancelled = true; cancelAnimationFrame(raf); lenis?.destroy(); ScrollTrigger.getAll().forEach((t) => t.kill()); };
  }, [reduced]);
  return <>{children}</>;
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd site && npx vitest run tests/motion-provider.test.tsx`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: add MotionProvider with Lenis + GSAP and reduced-motion guard"
```

### Task 0.6: Layout primitives (Container, Header, Footer, ScrollToTop, root)

**Files:**
- Create: `site/components/layout/Container.tsx`
- Create: `site/components/layout/Header.tsx`
- Create: `site/components/layout/Footer.tsx`
- Create: `site/components/layout/ScrollToTop.tsx`
- Create: `site/lib/nav.ts`
- Modify: `site/app/layout.tsx`
- Create: `site/tests/layout.test.tsx`

- [ ] **Step 1: Write the failing test**

`site/tests/layout.test.tsx`:
```tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";

describe("layout", () => {
  it("Header renders wordmark and primary nav", () => {
    render(<Header />);
    expect(screen.getByText("Precision Memory Agent")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Method" })).toBeInTheDocument();
  });
  it("Footer renders 5 column headings", () => {
    render(<Footer />);
    ["Project", "Sitemap", "Resources", "Modules", "Social"].forEach((h) =>
      expect(screen.getByRole("heading", { name: h })).toBeInTheDocument()
    );
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/layout.test.tsx`
Expected: FAIL — modules not found.

- [ ] **Step 3: Implement**

`site/lib/nav.ts`:
```ts
export const primaryNav = [
  { href: "/about", label: "About" },
  { href: "/method", label: "Method" },
  { href: "/performance", label: "Performance" },
  { href: "/reproducibility", label: "Reproducibility" },
] as const;
export const utilityNav = [
  { href: "/modules", label: "Modules" },
  { href: "/contact", label: "Contact" },
] as const;
export const footerCols = [
  { heading: "Project", links: [{ href: "/about", label: "About" }, { href: "/method", label: "Method" }] },
  { heading: "Sitemap", links: [{ href: "/", label: "Home" }, { href: "/notes", label: "Notes" }, { href: "/faq", label: "FAQ" }] },
  { heading: "Resources", links: [{ href: "/performance", label: "Performance" }, { href: "/reproducibility", label: "Reproducibility" }] },
  { heading: "Modules", links: [{ href: "/modules", label: "All modules" }] },
  { heading: "Social", links: [{ href: "/contact", label: "Contact" }, { href: "/legal", label: "Legal" }] },
] as const;
```

`site/components/layout/Container.tsx`:
```tsx
export function Container({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`mx-auto w-full max-w-container px-[var(--side-pad)] ${className}`}>{children}</div>
  );
}
```

`site/components/layout/Header.tsx`:
```tsx
import Link from "next/link";
import { Container } from "./Container";
import { primaryNav, utilityNav } from "@/lib/nav";

export function Header() {
  return (
    <header className="relative z-30 py-6">
      <Container className="flex items-center justify-between gap-6">
        <Link href="/" className="font-display text-lg font-bold tracking-tight">Precision Memory Agent</Link>
        <nav aria-label="Primary" className="hidden gap-7 md:flex">
          {primaryNav.map((i) => (
            <Link key={i.href} href={i.href} className="text-sm text-text-muted transition-colors duration-300 ease-brand hover:text-text">{i.label}</Link>
          ))}
        </nav>
        <nav aria-label="Utility" className="flex items-center gap-4">
          {utilityNav.map((i) => (
            <Link key={i.href} href={i.href} className="text-sm font-medium text-text">{i.label}</Link>
          ))}
        </nav>
      </Container>
    </header>
  );
}
```

`site/components/layout/Footer.tsx`:
```tsx
import Link from "next/link";
import { Container } from "./Container";
import { footerCols } from "@/lib/nav";

export function Footer() {
  return (
    <footer className="mt-32 border-t border-border bg-surface py-16">
      <Container className="grid grid-cols-2 gap-10 md:grid-cols-5">
        {footerCols.map((c) => (
          <div key={c.heading}>
            <h3 className="mb-4 font-display text-sm font-semibold text-text">{c.heading}</h3>
            <ul className="space-y-2">
              {c.links.map((l) => (
                <li key={l.href}><Link href={l.href} className="text-sm text-text-muted hover:text-text">{l.label}</Link></li>
              ))}
            </ul>
          </div>
        ))}
      </Container>
      <Container className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-border pt-6 text-xs text-text-muted md:flex-row">
        <span>© {new Date().getFullYear()} Precision Memory Agent</span>
        <Link href="/legal" className="hover:text-text">Privacy &amp; Terms</Link>
      </Container>
    </footer>
  );
}
```

`site/components/layout/ScrollToTop.tsx`:
```tsx
"use client";
import { useEffect, useState } from "react";

export function ScrollToTop() {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const onScroll = () => setShow(window.scrollY > window.innerHeight);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  if (!show) return null;
  return (
    <button
      aria-label="Scroll to top"
      onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
      className="fixed bottom-6 right-6 z-40 rounded-md border border-border bg-surface px-3 py-2 text-sm text-text"
    >↑</button>
  );
}
```

Update `site/app/layout.tsx` body to wrap content:
```tsx
import { display, body, mono } from "./fonts";
import "./globals.css";
import { MotionProvider } from "@/motion/MotionProvider";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { ScrollToTop } from "@/components/layout/ScrollToTop";

export const metadata = { title: "Precision Memory Agent", description: "Deterministic two-regime precision controller." };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable} ${mono.variable}`}>
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
```

- [ ] **Step 4: Run test + build**

Run: `cd site && npm test && npm run build`
Expected: all pass, build succeeds.

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: add layout primitives (Container, Header, Footer, ScrollToTop)"
```

---

## Phase 1 — Shared systems (3 tasks; parallelizable across agents)

### Task 1.1: Motion primitives

**Files:**
- Create: `site/motion/variants.ts`
- Create: `site/motion/Reveal.tsx`
- Create: `site/motion/Stagger.tsx`
- Create: `site/motion/CountUp.tsx`
- Create: `site/motion/ScrollPin.tsx`
- Create: `site/tests/motion-primitives.test.tsx`

- [ ] **Step 1: Write the failing test**

`site/tests/motion-primitives.test.tsx`:
```tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Reveal } from "@/motion/Reveal";
import { CountUp } from "@/motion/CountUp";

describe("motion primitives", () => {
  it("Reveal renders its children", () => {
    render(<Reveal><span>revealed</span></Reveal>);
    expect(screen.getByText("revealed")).toBeInTheDocument();
  });
  it("CountUp renders the final value as accessible text immediately", () => {
    render(<CountUp to={70.22} suffix=" / 90" />);
    expect(screen.getByText(/70\.22 \/ 90/)).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/motion-primitives.test.tsx`
Expected: FAIL — modules not found.

- [ ] **Step 3: Implement**

`site/motion/variants.ts`:
```ts
import type { Variants } from "framer-motion";
export const fadeUp: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] } },
};
export const staggerParent: Variants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } },
};
```

`site/motion/Reveal.tsx`:
```tsx
"use client";
import { motion } from "framer-motion";
import { fadeUp } from "./variants";
import { useReducedMotion } from "./useReducedMotion";

export function Reveal({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  const reduced = useReducedMotion();
  if (reduced) return <div className={className}>{children}</div>;
  return (
    <motion.div className={className} variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }}>
      {children}
    </motion.div>
  );
}
```

`site/motion/Stagger.tsx`:
```tsx
"use client";
import { motion } from "framer-motion";
import { staggerParent, fadeUp } from "./variants";
import { useReducedMotion } from "./useReducedMotion";

export function Stagger({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  const reduced = useReducedMotion();
  if (reduced) return <div className={className}>{children}</div>;
  return (
    <motion.div className={className} variants={staggerParent} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.2 }}>
      {children}
    </motion.div>
  );
}
export function StaggerItem({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <motion.div className={className} variants={fadeUp}>{children}</motion.div>;
}
```

`site/motion/CountUp.tsx`:
```tsx
"use client";
import { useEffect, useRef, useState } from "react";
import { useReducedMotion } from "./useReducedMotion";

export function CountUp({ to, prefix = "", suffix = "", decimals = 2 }: { to: number; prefix?: string; suffix?: string; decimals?: number }) {
  const reduced = useReducedMotion();
  const [val, setVal] = useState(reduced ? to : 0);
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    if (reduced) { setVal(to); return; }
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting) return;
      io.disconnect();
      const start = performance.now();
      const tick = (t: number) => {
        const p = Math.min(1, (t - start) / 900);
        setVal(to * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }, { threshold: 0.5 });
    io.observe(el);
    return () => io.disconnect();
  }, [to, reduced]);
  return <span ref={ref}>{prefix}{val.toFixed(decimals)}{suffix}</span>;
}
```

`site/motion/ScrollPin.tsx`:
```tsx
"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "./useReducedMotion";

export function ScrollPin({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  const reduced = useReducedMotion();
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (reduced || !ref.current) return;
    gsap.registerPlugin(ScrollTrigger);
    const st = ScrollTrigger.create({ trigger: ref.current, start: "top top", end: "+=80%", pin: true, pinSpacing: true });
    return () => st.kill();
  }, [reduced]);
  return <div ref={ref} className={className}>{children}</div>;
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd site && npx vitest run tests/motion-primitives.test.tsx`
Expected: PASS (reduced-motion is false in jsdom; CountUp shows final value because IntersectionObserver does not fire in jsdom — add IO mock).

Add to `site/vitest.setup.ts` (append):
```ts
class IO {
  observe() {}
  disconnect() {}
  unobserve() {}
}
// @ts-expect-error test shim
window.IntersectionObserver = window.IntersectionObserver || IO;
```
Then change the CountUp test expectation: when IO never fires and motion not reduced, value stays 0. To keep the test meaningful, render with reduced motion. Update the second test:
```tsx
import { vi } from "vitest";
it("CountUp shows final value under reduced motion", () => {
  window.matchMedia = ((q: string) => ({ matches: true, media: q, onchange: null, addEventListener: vi.fn(), removeEventListener: vi.fn(), addListener: vi.fn(), removeListener: vi.fn(), dispatchEvent: vi.fn() })) as never;
  render(<CountUp to={70.22} suffix=" / 90" />);
  expect(screen.getByText(/70\.22 \/ 90/)).toBeInTheDocument();
});
```
Re-run: `cd site && npx vitest run tests/motion-primitives.test.tsx` → PASS.

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: add motion primitives (Reveal, Stagger, CountUp, ScrollPin)"
```

### Task 1.2: R3F hero scene + reduced-motion fallback

**Files:**
- Create: `site/three/lattice.ts`
- Create: `site/three/HeroScene.tsx`
- Create: `site/components/sections/Hero.tsx`
- Create: `site/tests/hero.test.tsx`

- [ ] **Step 1: Write the failing test**

`site/tests/hero.test.tsx`:
```tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { Hero } from "@/components/sections/Hero";

vi.mock("@/three/HeroScene", () => ({ HeroScene: () => <div data-testid="r3f-scene" /> }));

describe("Hero", () => {
  it("renders headline + CTA over the scene", () => {
    render(<Hero />);
    expect(screen.getByRole("heading", { level: 1 })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /method/i })).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/hero.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

`site/three/lattice.ts`:
```ts
export function latticePositions(count: number, spread = 8): Float32Array {
  const arr = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    arr[i * 3] = (Math.random() - 0.5) * spread * 2;
    arr[i * 3 + 1] = (Math.random() - 0.5) * spread;
    arr[i * 3 + 2] = (Math.random() - 0.5) * spread * 2;
  }
  return arr;
}
```

`site/three/HeroScene.tsx`:
```tsx
"use client";
import { Canvas, useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";
import { latticePositions } from "./lattice";

function Points() {
  const ref = useRef<THREE.Points>(null);
  const positions = useMemo(() => latticePositions(2400), []);
  useFrame((s) => {
    if (!ref.current) return;
    ref.current.rotation.y = s.clock.elapsedTime * 0.05;
    ref.current.position.x = s.pointer.x * 0.6;
    ref.current.position.y = s.pointer.y * 0.4;
  });
  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial color="#f5a524" size={0.03} sizeAttenuation transparent opacity={0.85} />
    </points>
  );
}

export function HeroScene() {
  return (
    <Canvas dpr={[1, 2]} camera={{ position: [0, 0, 10], fov: 55 }} aria-hidden>
      <Points />
    </Canvas>
  );
}
```

`site/components/sections/Hero.tsx`:
```tsx
"use client";
import dynamic from "next/dynamic";
import Link from "next/link";
import { Container } from "@/components/layout/Container";
import { useReducedMotion } from "@/motion/useReducedMotion";

const HeroScene = dynamic(() => import("@/three/HeroScene").then((m) => m.HeroScene), { ssr: false });

export function Hero() {
  const reduced = useReducedMotion();
  return (
    <section className="relative isolate min-h-[88vh] overflow-hidden">
      <div className="absolute inset-0 -z-10">
        {reduced ? (
          <div className="h-full w-full bg-[radial-gradient(ellipse_at_center,#1c1408_0%,#0b0b0c_70%)]" />
        ) : (
          <HeroScene />
        )}
      </div>
      <Container className="flex min-h-[88vh] flex-col items-center justify-center text-center">
        <h1 className="max-w-4xl font-display text-5xl font-bold leading-tight md:text-7xl">
          Precision where memory matters most
        </h1>
        <p className="mt-6 max-w-xl text-lg text-text-muted">
          A deterministic two-regime precision controller — NumPy only, no retraining.
        </p>
        <div className="mt-10 flex gap-4">
          <Link href="/method" className="rounded-md bg-accent px-6 py-3 font-medium text-bg">See the method</Link>
          <Link href="/modules" className="rounded-md border border-border px-6 py-3 font-medium text-text">Explore modules</Link>
        </div>
      </Container>
    </section>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd site && npx vitest run tests/hero.test.tsx`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: add procedural R3F hero with reduced-motion fallback"
```

### Task 1.3: UI kit (Button, Card, Carousel, Accordion, Tabs, FilterRail, Field)

**Files:**
- Create: `site/components/ui/Button.tsx`
- Create: `site/components/ui/Card.tsx`
- Create: `site/components/ui/Carousel.tsx`
- Create: `site/components/ui/Accordion.tsx`
- Create: `site/components/ui/Tabs.tsx`
- Create: `site/components/ui/FilterRail.tsx`
- Create: `site/components/ui/Field.tsx`
- Create: `site/tests/ui-kit.test.tsx`

- [ ] **Step 1: Write the failing test**

`site/tests/ui-kit.test.tsx`:
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import { Accordion } from "@/components/ui/Accordion";
import { Tabs } from "@/components/ui/Tabs";
import { FilterRail } from "@/components/ui/FilterRail";

describe("UI kit logic", () => {
  it("Accordion toggles a panel", async () => {
    render(<Accordion items={[{ id: "a", q: "Q1", a: "A1" }]} />);
    expect(screen.queryByText("A1")).not.toBeVisible();
    await userEvent.click(screen.getByRole("button", { name: "Q1" }));
    expect(screen.getByText("A1")).toBeVisible();
  });
  it("Tabs switches active panel", async () => {
    render(<Tabs tabs={[{ id: "x", label: "X", content: <p>xc</p> }, { id: "y", label: "Y", content: <p>yc</p> }]} />);
    expect(screen.getByText("xc")).toBeInTheDocument();
    await userEvent.click(screen.getByRole("tab", { name: "Y" }));
    expect(screen.getByText("yc")).toBeInTheDocument();
  });
  it("FilterRail emits selection", async () => {
    let selected = "";
    render(<FilterRail options={[{ id: "all", label: "All" }, { id: "ret", label: "Retrieval" }]} value="all" onChange={(v) => (selected = v)} />);
    await userEvent.click(screen.getByRole("button", { name: "Retrieval" }));
    expect(selected).toBe("ret");
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/ui-kit.test.tsx`
Expected: FAIL — modules not found.

- [ ] **Step 3: Implement**

`site/components/ui/Button.tsx`:
```tsx
import Link from "next/link";
type Props = { href?: string; variant?: "primary" | "ghost"; children: React.ReactNode; onClick?: () => void; type?: "button" | "submit" };
export function Button({ href, variant = "primary", children, onClick, type = "button" }: Props) {
  const cls = `inline-block rounded-md px-6 py-3 font-medium transition-colors duration-300 ease-brand ${variant === "primary" ? "bg-accent text-bg hover:bg-accent-2" : "border border-border text-text hover:bg-surface"}`;
  if (href) return <Link href={href} className={cls}>{children}</Link>;
  return <button type={type} onClick={onClick} className={cls}>{children}</button>;
}
```

`site/components/ui/Card.tsx`:
```tsx
import Link from "next/link";
export function Card({ title, body, href }: { title: string; body: string; href?: string }) {
  const inner = (
    <div className="group h-full rounded-lg border border-border bg-surface p-6 transition-transform duration-300 ease-brand hover:-translate-y-1">
      <h3 className="font-display text-xl font-semibold">{title}</h3>
      <p className="mt-3 text-sm text-text-muted">{body}</p>
    </div>
  );
  return href ? <Link href={href}>{inner}</Link> : inner;
}
```

`site/components/ui/Carousel.tsx`:
```tsx
"use client";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination, Autoplay } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";

export function Carousel({ slides, perView = 1, autoplay = false }: { slides: React.ReactNode[]; perView?: number; autoplay?: boolean }) {
  return (
    <Swiper
      modules={[Navigation, Pagination, Autoplay]}
      navigation
      pagination={{ type: "fraction" }}
      autoplay={autoplay ? { delay: 4000 } : false}
      slidesPerView={1}
      breakpoints={{ 768: { slidesPerView: perView } }}
      speed={600}
    >
      {slides.map((s, i) => <SwiperSlide key={i}>{s}</SwiperSlide>)}
    </Swiper>
  );
}
```

`site/components/ui/Accordion.tsx`:
```tsx
"use client";
import { useState } from "react";
export function Accordion({ items }: { items: { id: string; q: string; a: string }[] }) {
  const [open, setOpen] = useState<string | null>(null);
  return (
    <div className="divide-y divide-border border-y border-border">
      {items.map((it) => {
        const isOpen = open === it.id;
        return (
          <div key={it.id}>
            <button className="flex w-full items-center justify-between py-5 text-left font-medium" aria-expanded={isOpen} onClick={() => setOpen(isOpen ? null : it.id)}>
              {it.q}
              <span className={`transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`}>▾</span>
            </button>
            <div hidden={!isOpen} className="pb-5 text-sm text-text-muted">{it.a}</div>
          </div>
        );
      })}
    </div>
  );
}
```

`site/components/ui/Tabs.tsx`:
```tsx
"use client";
import { useState } from "react";
export function Tabs({ tabs }: { tabs: { id: string; label: string; content: React.ReactNode }[] }) {
  const [active, setActive] = useState(tabs[0]?.id);
  return (
    <div>
      <div role="tablist" className="flex gap-2 border-b border-border">
        {tabs.map((t) => (
          <button key={t.id} role="tab" aria-selected={active === t.id} onClick={() => setActive(t.id)}
            className={`px-4 py-3 text-sm transition-colors duration-300 ${active === t.id ? "border-b-2 border-accent text-text" : "text-text-muted"}`}>
            {t.label}
          </button>
        ))}
      </div>
      <div role="tabpanel" className="pt-8">{tabs.find((t) => t.id === active)?.content}</div>
    </div>
  );
}
```

`site/components/ui/FilterRail.tsx`:
```tsx
"use client";
export function FilterRail({ options, value, onChange }: { options: { id: string; label: string }[]; value: string; onChange: (v: string) => void }) {
  return (
    <div className="flex flex-wrap gap-2 md:flex-col">
      {options.map((o) => (
        <button key={o.id} onClick={() => onChange(o.id)}
          className={`rounded-md px-4 py-2 text-left text-sm transition-colors duration-300 ${value === o.id ? "bg-accent text-bg" : "border border-border text-text-muted hover:text-text"}`}>
          {o.label}
        </button>
      ))}
    </div>
  );
}
```

`site/components/ui/Field.tsx`:
```tsx
export function Field({ label, name, type = "text", required = false, textarea = false }: { label: string; name: string; type?: string; required?: boolean; textarea?: boolean }) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm text-text-muted">{label}{required && " *"}</span>
      {textarea ? (
        <textarea name={name} required={required} rows={5} className="w-full rounded-md border border-border bg-surface px-4 py-3 outline-none focus:border-accent" />
      ) : (
        <input name={name} type={type} required={required} className="w-full rounded-md border border-border bg-surface px-4 py-3 outline-none focus:border-accent" />
      )}
    </label>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd site && npx vitest run tests/ui-kit.test.tsx`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: add UI kit (Button, Card, Carousel, Accordion, Tabs, FilterRail, Field)"
```

---

## Phase 2 — Pages (parallelizable: 2.1 first, then 2.2–2.6)

### Task 2.1: Content model + MDX pipeline

**Files:**
- Create: `site/content/modules.ts`
- Create: `site/content/results.ts`
- Create: `site/content/faq.ts`
- Create: `site/content/narrative.ts`
- Create: `site/content/notes/precision-regimes.mdx`
- Create: `site/lib/content.ts`
- Modify: `site/next.config.ts` (MDX)
- Create: `site/tests/content.test.ts`

All copy below is original and derived from `w/README.md` (this repo's own document).

- [ ] **Step 1: Write the failing test**

`site/tests/content.test.ts`:
```ts
import { describe, it, expect } from "vitest";
import { getModules, getModule } from "@/lib/content";

describe("content model", () => {
  it("lists modules with slugs", () => {
    const m = getModules();
    expect(m.length).toBeGreaterThanOrEqual(4);
    expect(m[0]).toHaveProperty("slug");
  });
  it("resolves a module by slug", () => {
    expect(getModule("geometry-branch")?.title).toMatch(/Geometry/);
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/content.test.ts`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement content + loaders**

`site/content/modules.ts`:
```ts
export type Module = { slug: string; title: string; domain: "Retrieval" | "Anisotropy" | "Robustness" | "Tools"; summary: string; detail: string };
export const modules: Module[] = [
  { slug: "anvil-p-e", title: "Anvil-P-E", domain: "Tools", summary: "Benchmark and evaluation harness used to score the controller.", detail: "Runs the public self-check across seeds and reports per-seed retrieval and spread metrics without halving regressions." },
  { slug: "w-adapter", title: "w Adapter (Engine)", domain: "Tools", summary: "Single-file deterministic adapter exposing the precision controller.", detail: "Uses only NumPy, the provided stored patterns, and frozen model parameters. No retraining, no external state." },
  { slug: "corruption-map-controller", title: "Corruption-Map Controller", domain: "Retrieval", summary: "Estimates likely-masked coordinates and raises their precision.", detail: "Compares each query magnitude to typical per-coordinate magnitude; small-magnitude coordinates get higher precision so the gradient refills missing signal. A class-conditional shape prior adds a small attractor-aware nudge." },
  { slug: "geometry-branch", title: "Geometry Branch", domain: "Anisotropy", summary: "Hessian-aware diagonal preconditioner for near-clean probes.", detail: "Builds the frozen-model Hessian at the nearest pattern and solves for the positive diagonal that minimises the eigen-spread of the isotropised operator via projected subgradient on log-precision, warm-started from four analytic preconditioners. Non-SPD Hessians are PSD-regularised, never degenerating to identity precision." },
];
```

`site/content/results.ts`:
```ts
export const results = [
  { label: "Mean Δ accuracy", value: 0.142, decimals: 3, prefix: "+" },
  { label: "Min Δ accuracy", value: 0.047, decimals: 3, prefix: "+", note: "every seed > 0; no halving" },
  { label: "Mean spread reduction", value: 1.03, decimals: 2, suffix: "×" },
  { label: "Total automated", value: 70.22, decimals: 2, suffix: " / 90" },
];
export const honestNote =
  "On the public synthetic operator, a ≥10× spread reduction is not reachable by any diagonal precision vector — it is a property of the operator, not a solver limitation. The geometry branch reports its true ceiling here while remaining the correct construction for the anisotropic held-out evaluation.";
```

`site/content/faq.ts`:
```ts
export const faq = [
  { id: "deps", q: "What are the dependencies?", a: "NumPy only — the same as the starter kit." },
  { id: "deterministic", q: "Is the output deterministic?", a: "Yes. The solution is deterministic and cached per attractor; degenerate queries return unit precision." },
  { id: "branches", q: "How is the regime chosen?", a: "By nearest-pattern cosine confidence, with a geometrically blended transition band so the two objectives do not interfere." },
];
```

`site/content/narrative.ts`:
```ts
export type Narrative = { slug: string; title: string; lede: string; sections: { h: string; p: string }[] };
export const narratives: Narrative[] = [
  { slug: "about", title: "About", lede: "A deterministic two-regime precision controller.", sections: [
    { h: "What it is", p: "A precision controller that adapts per-coordinate precision using only NumPy, stored patterns, and frozen model parameters." },
    { h: "Design stance", p: "No retraining and no external state — the agent is a pure function of its inputs." }] },
  { slug: "method", title: "Method", lede: "Two regimes, one principled controller.", sections: [
    { h: "Corruption regime", p: "For corrupted retrieval queries, a per-coordinate corruption map raises precision on likely-masked coordinates so the gradient refills missing signal quickly." },
    { h: "Geometry regime", p: "For near-clean probes, the Hessian at the nearest pattern is isotropised by solving for the optimal positive diagonal precision." }] },
  { slug: "performance", title: "Performance", lede: "Honest, reproducible figures.", sections: [
    { h: "Retrieval", p: "Full retrieval credit on the public self-check with no per-seed regression." },
    { h: "Anisotropy", p: "The branch computes the genuinely optimal diagonal for the exact scored spread; the public operator's ceiling is reported honestly." }] },
  { slug: "reproducibility", title: "Reproducibility", lede: "Deterministic and easy to run.", sections: [
    { h: "Setup", p: "Install requirements (NumPy) and run the self-check adapter entry point." },
    { h: "Determinism", p: "Every iterate is scored with the exact harness metric; the returned vector is the best actually observed and is cached per attractor." }] },
];
```

`site/content/notes/precision-regimes.mdx`:
```mdx
---
title: "Why two regimes beat one"
date: "2026-05-16"
kind: "Guides"
---

Corrupted queries and near-clean probes need opposite things from a precision
vector. Treating them with one rule blurs both. This note sketches the
confidence-gated split and why the transition is blended geometrically.
```

`site/lib/content.ts`:
```ts
import { modules, type Module } from "@/content/modules";
import { narratives, type Narrative } from "@/content/narrative";
export const getModules = (): Module[] => modules;
export const getModule = (slug: string): Module | undefined => modules.find((m) => m.slug === slug);
export const getNarrative = (slug: string): Narrative | undefined => narratives.find((n) => n.slug === slug);
```

Update `site/next.config.ts`:
```ts
import createMDX from "@next/mdx";
import type { NextConfig } from "next";
const nextConfig: NextConfig = { pageExtensions: ["ts", "tsx", "mdx"] };
export default createMDX()(nextConfig);
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd site && npx vitest run tests/content.test.ts`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: add typed content model, MDX pipeline, content loaders"
```

### Task 2.2: Homepage (9 sections)

**Files:**
- Create: `site/components/sections/ValueProp.tsx`, `ModulesGrid.tsx`, `DomainsToggle.tsx`, `MethodCarousel.tsx`, `ResultsBand.tsx`, `Approach.tsx`, `NotesCarousel.tsx`, `FooterCta.tsx`
- Modify: `site/app/page.tsx`
- Create: `site/tests/homepage.test.tsx`

- [ ] **Step 1: Write the failing test**

`site/tests/homepage.test.tsx`:
```tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
vi.mock("@/three/HeroScene", () => ({ HeroScene: () => <div /> }));
import Home from "@/app/page";

describe("homepage", () => {
  it("renders hero + modules grid + results", () => {
    render(<Home />);
    expect(screen.getByRole("heading", { level: 1 })).toBeInTheDocument();
    expect(screen.getByText("Geometry Branch")).toBeInTheDocument();
    expect(screen.getByText(/70\.22/)).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/homepage.test.tsx`
Expected: FAIL.

- [ ] **Step 3: Implement sections + compose page**

`site/components/sections/ValueProp.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
import { Reveal } from "@/motion/Reveal";
import Link from "next/link";
export function ValueProp() {
  return (
    <Container className="py-28">
      <Reveal>
        <p className="max-w-3xl font-display text-3xl leading-snug md:text-4xl">
          One controller, two regimes: it refills corrupted memory and isotropises near-clean geometry — deterministically.
          <Link href="/method" className="ml-3 text-accent">Read more →</Link>
        </p>
      </Reveal>
    </Container>
  );
}
```

`site/components/sections/ModulesGrid.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Stagger, StaggerItem } from "@/motion/Stagger";
import { getModules } from "@/lib/content";
export function ModulesGrid() {
  const mods = getModules();
  return (
    <Container className="py-20">
      <Stagger className="grid gap-6 md:grid-cols-4">
        {mods.map((m) => (
          <StaggerItem key={m.slug}><Card title={m.title} body={m.summary} href={`/modules/${m.slug}`} /></StaggerItem>
        ))}
      </Stagger>
      <div className="mt-10"><Button href="/modules" variant="ghost">See all modules</Button></div>
    </Container>
  );
}
```

`site/components/sections/DomainsToggle.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
import { Tabs } from "@/components/ui/Tabs";
export function DomainsToggle() {
  return (
    <Container className="py-20">
      <Tabs tabs={[
        { id: "ret", label: "Retrieval", content: <p className="max-w-2xl text-text-muted">Per-coordinate corruption maps raise precision on likely-masked coordinates.</p> },
        { id: "ani", label: "Anisotropy", content: <p className="max-w-2xl text-text-muted">Hessian isotropisation finds the optimal diagonal preconditioner.</p> },
        { id: "rob", label: "Robustness", content: <p className="max-w-2xl text-text-muted">Confidence-gated blending keeps the two objectives from interfering.</p> },
      ]} />
    </Container>
  );
}
```

`site/components/sections/MethodCarousel.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
import { Carousel } from "@/components/ui/Carousel";
const steps = [
  "01 — Estimate the corruption map from per-coordinate magnitude.",
  "02 — Add a small class-conditional attractor-shape nudge.",
  "03 — For near-clean probes, build the frozen-model Hessian.",
  "04 — Solve for the optimal diagonal; blend the branch decision.",
];
export function MethodCarousel() {
  return (
    <Container className="py-20">
      <Carousel slides={steps.map((s) => (
        <div key={s} className="rounded-lg border border-border bg-surface p-12 font-display text-2xl">{s}</div>
      ))} />
    </Container>
  );
}
```

`site/components/sections/ResultsBand.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
import { Carousel } from "@/components/ui/Carousel";
import { CountUp } from "@/motion/CountUp";
import { results, honestNote } from "@/content/results";
export function ResultsBand() {
  return (
    <Container className="py-20">
      <Carousel autoplay perView={3} slides={results.map((r) => (
        <div key={r.label} className="p-10 text-center">
          <div className="font-display text-4xl text-accent">
            <CountUp to={r.value} decimals={r.decimals} prefix={r.prefix ?? ""} suffix={r.suffix ?? ""} />
          </div>
          <div className="mt-2 text-sm text-text-muted">{r.label}</div>
        </div>
      ))} />
      <p className="mx-auto mt-10 max-w-2xl text-center text-xs text-text-muted">{honestNote}</p>
    </Container>
  );
}
```

`site/components/sections/Approach.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";
import { Stagger, StaggerItem } from "@/motion/Stagger";
const blocks = [
  { t: "Method", b: "Two regimes, one principled controller.", h: "/method" },
  { t: "Performance", b: "Honest, reproducible figures.", h: "/performance" },
  { t: "Reproducibility", b: "Deterministic and easy to run.", h: "/reproducibility" },
];
export function Approach() {
  return (
    <Container className="py-20">
      <Stagger className="grid gap-6 md:grid-cols-3">
        {blocks.map((x) => <StaggerItem key={x.t}><Card title={x.t} body={x.b} href={x.h} /></StaggerItem>)}
      </Stagger>
    </Container>
  );
}
```

`site/components/sections/NotesCarousel.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
import { Carousel } from "@/components/ui/Carousel";
const notes = [
  { t: "Why two regimes beat one", h: "/notes/precision-regimes" },
];
export function NotesCarousel() {
  return (
    <Container className="py-20">
      <Carousel perView={3} slides={notes.map((n) => (
        <a key={n.h} href={n.h} className="block rounded-lg border border-border bg-surface p-8">{n.t}</a>
      ))} />
    </Container>
  );
}
```

`site/components/sections/FooterCta.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
import { Button } from "@/components/ui/Button";
import { Reveal } from "@/motion/Reveal";
export function FooterCta() {
  return (
    <Container className="py-28 text-center">
      <Reveal>
        <h2 className="font-display text-4xl">Want the full method?</h2>
        <div className="mt-8 flex justify-center gap-4">
          <Button href="/method">Read the method</Button>
          <Button href="/contact" variant="ghost">Contact</Button>
        </div>
      </Reveal>
    </Container>
  );
}
```

`site/app/page.tsx`:
```tsx
import { Hero } from "@/components/sections/Hero";
import { ValueProp } from "@/components/sections/ValueProp";
import { ModulesGrid } from "@/components/sections/ModulesGrid";
import { DomainsToggle } from "@/components/sections/DomainsToggle";
import { MethodCarousel } from "@/components/sections/MethodCarousel";
import { ResultsBand } from "@/components/sections/ResultsBand";
import { Approach } from "@/components/sections/Approach";
import { NotesCarousel } from "@/components/sections/NotesCarousel";
import { FooterCta } from "@/components/sections/FooterCta";

export default function Home() {
  return (
    <>
      <Hero /><ValueProp /><ModulesGrid /><DomainsToggle />
      <MethodCarousel /><ResultsBand /><Approach /><NotesCarousel /><FooterCta />
    </>
  );
}
```

- [ ] **Step 4: Run test + build**

Run: `cd site && npx vitest run tests/homepage.test.tsx && npm run build`
Expected: PASS; build succeeds.

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: implement homepage with all 9 sections"
```

### Task 2.3: Modules index + detail

**Files:**
- Create: `site/app/modules/page.tsx`
- Create: `site/app/modules/ModulesClient.tsx`
- Create: `site/app/modules/[slug]/page.tsx`
- Create: `site/tests/modules.test.tsx`

- [ ] **Step 1: Write the failing test**

`site/tests/modules.test.tsx`:
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import { ModulesClient } from "@/app/modules/ModulesClient";

describe("modules index", () => {
  it("filters by domain", async () => {
    render(<ModulesClient />);
    expect(screen.getByText("Geometry Branch")).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: "Retrieval" }));
    expect(screen.queryByText("Geometry Branch")).not.toBeInTheDocument();
    expect(screen.getByText("Corruption-Map Controller")).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/modules.test.tsx`
Expected: FAIL.

- [ ] **Step 3: Implement**

`site/app/modules/ModulesClient.tsx`:
```tsx
"use client";
import { useState } from "react";
import { Container } from "@/components/layout/Container";
import { FilterRail } from "@/components/ui/FilterRail";
import { Card } from "@/components/ui/Card";
import { getModules } from "@/lib/content";
const opts = [
  { id: "all", label: "All" }, { id: "Retrieval", label: "Retrieval" },
  { id: "Anisotropy", label: "Anisotropy" }, { id: "Robustness", label: "Robustness" }, { id: "Tools", label: "Tools" },
];
export function ModulesClient() {
  const [f, setF] = useState("all");
  const mods = getModules().filter((m) => f === "all" || m.domain === f);
  return (
    <Container className="grid gap-10 py-20 md:grid-cols-[220px_1fr]">
      <FilterRail options={opts} value={f} onChange={setF} />
      <div className="grid gap-6 sm:grid-cols-2">
        {mods.map((m) => <Card key={m.slug} title={m.title} body={m.summary} href={`/modules/${m.slug}`} />)}
      </div>
    </Container>
  );
}
```

`site/app/modules/page.tsx`:
```tsx
import { ModulesClient } from "./ModulesClient";
export const metadata = { title: "Modules — Precision Memory Agent" };
export default function ModulesPage() { return <ModulesClient />; }
```

`site/app/modules/[slug]/page.tsx`:
```tsx
import { notFound } from "next/navigation";
import { Container } from "@/components/layout/Container";
import { getModules, getModule } from "@/lib/content";
export function generateStaticParams() { return getModules().map((m) => ({ slug: m.slug })); }
export default async function ModuleDetail({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const m = getModule(slug);
  if (!m) notFound();
  return (
    <Container className="py-24">
      <p className="text-sm text-text-muted">Modules / {m.domain}</p>
      <h1 className="mt-3 font-display text-5xl">{m.title}</h1>
      <p className="mt-6 max-w-2xl text-lg text-text-muted">{m.summary}</p>
      <div className="mt-10 max-w-3xl border-t border-border pt-10">{m.detail}</div>
    </Container>
  );
}
```

- [ ] **Step 4: Run test + build**

Run: `cd site && npx vitest run tests/modules.test.tsx && npm run build`
Expected: PASS; build succeeds (static params generate detail pages).

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: add modules index (filterable) and module detail pages"
```

### Task 2.4: Notes index + article (MDX)

**Files:**
- Create: `site/lib/notes.ts`
- Create: `site/app/notes/page.tsx`
- Create: `site/app/notes/[slug]/page.tsx`
- Create: `site/components/notes/ReadingProgress.tsx`
- Create: `site/tests/notes.test.tsx`

- [ ] **Step 1: Write the failing test**

`site/tests/notes.test.tsx`:
```tsx
import { describe, it, expect } from "vitest";
import { getNotes } from "@/lib/notes";

describe("notes", () => {
  it("lists notes with frontmatter", () => {
    const n = getNotes();
    expect(n.length).toBeGreaterThanOrEqual(1);
    expect(n[0]).toMatchObject({ slug: "precision-regimes", kind: "Guides" });
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/notes.test.tsx`
Expected: FAIL.

- [ ] **Step 3: Implement**

`site/lib/notes.ts`:
```ts
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
```

`site/components/notes/ReadingProgress.tsx`:
```tsx
"use client";
import { useEffect, useState } from "react";
export function ReadingProgress() {
  const [p, setP] = useState(0);
  useEffect(() => {
    const on = () => {
      const h = document.documentElement;
      setP((h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100);
    };
    window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);
  return <div className="fixed left-0 top-0 z-50 h-1 bg-accent" style={{ width: `${p}%` }} />;
}
```

`site/app/notes/page.tsx`:
```tsx
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
```

`site/app/notes/[slug]/page.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
import { ReadingProgress } from "@/components/notes/ReadingProgress";
import { getNotes } from "@/lib/notes";
export function generateStaticParams() { return getNotes().map((n) => ({ slug: n.slug })); }
export default async function NotePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const { default: MDX } = await import(`@/content/notes/${slug}.mdx`);
  return (
    <>
      <ReadingProgress />
      <Container className="prose-invert mx-auto max-w-2xl py-24">
        <article className="space-y-5 leading-relaxed"><MDX /></article>
      </Container>
    </>
  );
}
```

- [ ] **Step 4: Run test + build**

Run: `cd site && npx vitest run tests/notes.test.tsx && npm run build`
Expected: PASS; build succeeds.

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: add notes index (tabs) and MDX article pages with reading progress"
```

### Task 2.5: Narrative template ×4

**Files:**
- Create: `site/components/templates/Narrative.tsx`
- Create: `site/app/about/page.tsx`, `site/app/method/page.tsx`, `site/app/performance/page.tsx`, `site/app/reproducibility/page.tsx`
- Create: `site/tests/narrative.test.tsx`

- [ ] **Step 1: Write the failing test**

`site/tests/narrative.test.tsx`:
```tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Narrative } from "@/components/templates/Narrative";
import { getNarrative } from "@/lib/content";

describe("narrative template", () => {
  it("renders method narrative", () => {
    render(<Narrative data={getNarrative("method")!} />);
    expect(screen.getByRole("heading", { level: 1, name: "Method" })).toBeInTheDocument();
    expect(screen.getByText(/Corruption regime/)).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/narrative.test.tsx`
Expected: FAIL.

- [ ] **Step 3: Implement**

`site/components/templates/Narrative.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
import { Reveal } from "@/motion/Reveal";
import type { Narrative as N } from "@/content/narrative";
export function Narrative({ data }: { data: N }) {
  return (
    <>
      <section className="border-b border-border bg-surface py-32">
        <Container>
          <h1 className="font-display text-6xl">{data.title}</h1>
          <p className="mt-6 max-w-2xl text-xl text-text-muted">{data.lede}</p>
        </Container>
      </section>
      <Container className="py-24">
        <div className="space-y-24">
          {data.sections.map((s, i) => (
            <Reveal key={s.h}>
              <div className={`grid gap-10 md:grid-cols-2 ${i % 2 ? "md:[direction:rtl]" : ""}`}>
                <h2 className="font-display text-3xl [direction:ltr]">{s.h}</h2>
                <p className="text-lg text-text-muted [direction:ltr]">{s.p}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </Container>
    </>
  );
}
```

`site/app/about/page.tsx`:
```tsx
import { Narrative } from "@/components/templates/Narrative";
import { getNarrative } from "@/lib/content";
export const metadata = { title: "About — Precision Memory Agent" };
export default function Page() { return <Narrative data={getNarrative("about")!} />; }
```

`site/app/method/page.tsx`:
```tsx
import { Narrative } from "@/components/templates/Narrative";
import { getNarrative } from "@/lib/content";
export const metadata = { title: "Method — Precision Memory Agent" };
export default function Page() { return <Narrative data={getNarrative("method")!} />; }
```

`site/app/performance/page.tsx`:
```tsx
import { Narrative } from "@/components/templates/Narrative";
import { getNarrative } from "@/lib/content";
export const metadata = { title: "Performance — Precision Memory Agent" };
export default function Page() { return <Narrative data={getNarrative("performance")!} />; }
```

`site/app/reproducibility/page.tsx`:
```tsx
import { Narrative } from "@/components/templates/Narrative";
import { getNarrative } from "@/lib/content";
export const metadata = { title: "Reproducibility — Precision Memory Agent" };
export default function Page() { return <Narrative data={getNarrative("reproducibility")!} />; }
```

- [ ] **Step 4: Run test + build**

Run: `cd site && npx vitest run tests/narrative.test.tsx && npm run build`
Expected: PASS; build succeeds.

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: add narrative template and About/Method/Performance/Reproducibility pages"
```

### Task 2.6: Contact + FAQ + Legal

**Files:**
- Create: `site/app/contact/page.tsx`, `site/app/contact/ContactForm.tsx`
- Create: `site/app/faq/page.tsx`, `site/app/faq/FaqClient.tsx`
- Create: `site/app/legal/page.tsx`
- Create: `site/tests/contact-faq.test.tsx`

- [ ] **Step 1: Write the failing test**

`site/tests/contact-faq.test.tsx`:
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import { FaqClient } from "@/app/faq/FaqClient";
import { ContactForm } from "@/app/contact/ContactForm";

describe("contact + faq", () => {
  it("FAQ search filters questions", async () => {
    render(<FaqClient />);
    expect(screen.getByText(/dependencies/i)).toBeInTheDocument();
    await userEvent.type(screen.getByRole("searchbox"), "deterministic");
    expect(screen.queryByText(/dependencies/i)).not.toBeInTheDocument();
  });
  it("Contact form blocks empty submit", async () => {
    render(<ContactForm />);
    await userEvent.click(screen.getByRole("button", { name: /send/i }));
    expect(screen.getByText(/please complete/i)).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/contact-faq.test.tsx`
Expected: FAIL.

- [ ] **Step 3: Implement**

`site/app/contact/ContactForm.tsx`:
```tsx
"use client";
import { useState } from "react";
import { Field } from "@/components/ui/Field";
import { Button } from "@/components/ui/Button";
export function ContactForm() {
  const [err, setErr] = useState("");
  const [sent, setSent] = useState(false);
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    if (!fd.get("name") || !fd.get("email") || !fd.get("message")) { setErr("Please complete all fields."); return; }
    setErr("");
    const endpoint = process.env.NEXT_PUBLIC_CONTACT_ENDPOINT;
    if (endpoint) await fetch(endpoint, { method: "POST", body: fd }).catch(() => {});
    setSent(true);
  }
  if (sent) return <p className="text-accent">Thanks — we’ll be in touch.</p>;
  return (
    <form onSubmit={onSubmit} className="space-y-5">
      <Field label="Name" name="name" required />
      <Field label="Email" name="email" type="email" required />
      <Field label="Message" name="message" textarea required />
      {err && <p className="text-sm text-accent">{err}</p>}
      <Button type="submit">Send message</Button>
    </form>
  );
}
```

`site/app/contact/page.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
import { ContactForm } from "./ContactForm";
export const metadata = { title: "Contact — Precision Memory Agent" };
export default function ContactPage() {
  return (
    <Container className="grid gap-16 py-24 md:grid-cols-2">
      <div><h1 className="font-display text-5xl">Contact</h1><p className="mt-6 text-text-muted">Questions about the controller or reproducibility? Send a note.</p></div>
      <ContactForm />
    </Container>
  );
}
```

`site/app/faq/FaqClient.tsx`:
```tsx
"use client";
import { useState } from "react";
import { Container } from "@/components/layout/Container";
import { Accordion } from "@/components/ui/Accordion";
import { faq } from "@/content/faq";
export function FaqClient() {
  const [q, setQ] = useState("");
  const items = faq.filter((f) => (f.q + f.a).toLowerCase().includes(q.toLowerCase()));
  return (
    <Container className="py-24">
      <h1 className="font-display text-5xl">FAQ</h1>
      <input type="search" aria-label="Search FAQ" placeholder="Search…" value={q} onChange={(e) => setQ(e.target.value)}
        className="mt-8 w-full max-w-md rounded-md border border-border bg-surface px-4 py-3 outline-none focus:border-accent" />
      <div className="mt-8"><Accordion items={items} /></div>
    </Container>
  );
}
```

`site/app/faq/page.tsx`:
```tsx
import { FaqClient } from "./FaqClient";
export const metadata = { title: "FAQ — Precision Memory Agent" };
export default function FaqPage() { return <FaqClient />; }
```

`site/app/legal/page.tsx`:
```tsx
import { Container } from "@/components/layout/Container";
export const metadata = { title: "Privacy & Terms — Precision Memory Agent" };
export default function LegalPage() {
  return (
    <Container className="prose-invert max-w-2xl py-24">
      <h1 className="font-display text-4xl">Privacy &amp; Terms</h1>
      <p className="mt-6 text-text-muted">This site presents an original research project. It collects no personal data beyond any message you choose to submit via the contact form, which is sent only to the configured project endpoint.</p>
    </Container>
  );
}
```

- [ ] **Step 4: Run test + build**

Run: `cd site && npx vitest run tests/contact-faq.test.tsx && npm run build`
Expected: PASS; build succeeds.

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: add Contact (validated form), FAQ (searchable), and Legal pages"
```

---

## Phase 3 — Integration & QA

### Task 3.1: Route transitions, active nav, SEO, sitemap

**Files:**
- Create: `site/components/layout/RouteTransition.tsx`
- Modify: `site/app/layout.tsx` (wrap main)
- Modify: `site/components/layout/Header.tsx` (active state)
- Create: `site/app/sitemap.ts`, `site/app/robots.ts`
- Create: `site/tests/seo.test.ts`

- [ ] **Step 1: Write the failing test**

`site/tests/seo.test.ts`:
```ts
import { describe, it, expect } from "vitest";
import sitemap from "@/app/sitemap";

describe("sitemap", () => {
  it("includes all primary routes", () => {
    const urls = sitemap().map((e) => e.url);
    ["/", "/modules", "/notes", "/about", "/method", "/performance", "/reproducibility", "/contact", "/faq", "/legal"]
      .forEach((p) => expect(urls.some((u) => u.endsWith(p) || (p === "/" && u.endsWith("/")))).toBe(true));
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd site && npx vitest run tests/seo.test.ts`
Expected: FAIL.

- [ ] **Step 3: Implement**

`site/app/sitemap.ts`:
```ts
import type { MetadataRoute } from "next";
import { getModules } from "@/lib/content";
import { getNotes } from "@/lib/notes";
const BASE = process.env.NEXT_PUBLIC_SITE_URL ?? "https://example.com";
export default function sitemap(): MetadataRoute.Sitemap {
  const routes = ["/", "/modules", "/notes", "/about", "/method", "/performance", "/reproducibility", "/contact", "/faq", "/legal"];
  const mod = getModules().map((m) => `/modules/${m.slug}`);
  const notes = getNotes().map((n) => `/notes/${n.slug}`);
  return [...routes, ...mod, ...notes].map((p) => ({ url: `${BASE}${p}`, lastModified: new Date() }));
}
```

`site/app/robots.ts`:
```ts
import type { MetadataRoute } from "next";
const BASE = process.env.NEXT_PUBLIC_SITE_URL ?? "https://example.com";
export default function robots(): MetadataRoute.Robots {
  return { rules: { userAgent: "*", allow: "/" }, sitemap: `${BASE}/sitemap.xml` };
}
```

`site/components/layout/RouteTransition.tsx`:
```tsx
"use client";
import { AnimatePresence, motion } from "framer-motion";
import { usePathname } from "next/navigation";
import { useReducedMotion } from "@/motion/useReducedMotion";
export function RouteTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const reduced = useReducedMotion();
  if (reduced) return <>{children}</>;
  return (
    <AnimatePresence mode="wait">
      <motion.div key={pathname} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.35 }}>
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

Wrap `main` in `site/app/layout.tsx`: `<main><RouteTransition>{children}</RouteTransition></main>`.

In `site/components/layout/Header.tsx`, make it a client component (`"use client";` at top), import `usePathname`, and add `aria-current={pathname === i.href ? "page" : undefined}` plus `text-text` when active for `primaryNav` links.

- [ ] **Step 4: Run test + build**

Run: `cd site && npm test && npm run build`
Expected: all tests pass; build succeeds.

- [ ] **Step 5: Commit**

```bash
git add site && git commit -m "feat: add route transitions, active nav, sitemap, robots"
```

### Task 3.2: E2E critical flows + responsive/reduced-motion sweep

**Files:**
- Create: `site/playwright.config.ts`
- Create: `site/e2e/critical.spec.ts`

- [ ] **Step 1: Write the E2E spec**

`site/playwright.config.ts`:
```ts
import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./e2e",
  webServer: { command: "npm run build && npm run start", port: 3000, reuseExistingServer: false, timeout: 120000 },
  use: { baseURL: "http://localhost:3000" },
});
```

`site/e2e/critical.spec.ts`:
```ts
import { test, expect } from "@playwright/test";
test("home loads with hero and nav", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await page.getByRole("link", { name: "Explore modules" }).click();
  await expect(page).toHaveURL(/\/modules/);
});
test("module filter then detail", async ({ page }) => {
  await page.goto("/modules");
  await page.getByRole("button", { name: "Anisotropy" }).click();
  await page.getByText("Geometry Branch").click();
  await expect(page.getByRole("heading", { level: 1, name: "Geometry Branch" })).toBeVisible();
});
test("reduced motion renders static hero", async ({ browser }) => {
  const ctx = await browser.newContext({ reducedMotion: "reduce" });
  const page = await ctx.newPage();
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await ctx.close();
});
```

- [ ] **Step 2: Install browsers + run**

Run:
```bash
cd site && npx playwright install --with-deps chromium && npm run e2e
```
Expected: 3 passed.

- [ ] **Step 3: Commit**

```bash
git add site && git commit -m "test: add Playwright E2E for critical flows incl. reduced motion"
```

### Task 3.3: Final quality gate

- [ ] **Step 1: Full test + coverage**

Run: `cd site && npm test`
Expected: all suites pass; coverage lines ≥ 80%. If below, add tests for any uncovered loader/logic in `lib/` and `components/ui/`.

- [ ] **Step 2: Production build + lint**

Run: `cd site && npm run build && npm run lint`
Expected: both succeed with no errors.

- [ ] **Step 3: Code review pass**

Dispatch the `code-reviewer` agent on the `site/` diff for branch `feat/precision-memory-agent-site`. Address CRITICAL/HIGH findings; re-run tests + build after fixes.

- [ ] **Step 4: IP boundary check**

Run: `cd site && grep -rIn -iE "coffee[- ]?tech|fz94|silon|ghibli" --include=*.tsx --include=*.ts --include=*.mdx . ; echo done`
Expected: no matches (no reference-site names anywhere). If matches, replace with original PMA content.

- [ ] **Step 5: Final commit**

```bash
git add site && git commit -m "chore: final QA — tests, build, lint, code review, IP check green" --allow-empty
```

---

## Self-Review (completed by plan author)

**Spec coverage:** §4 tokens → 0.4 · §5 IA/routes → 0.6, 2.3–2.6, 3.1 · §6 homepage 9 sections → 2.2 · §7 inner templates → 2.3 (detail+index), 2.4 (notes), 2.5 (narrative), 2.6 (contact/faq/legal) · §8 motion system → 0.5, 1.1, 1.2, 3.1 · §9 architecture → 0.1–0.6, 2.1 · §10 multi-agent phases → plan phase structure · §11 deps → 0.2 · §12 testing → every task TDD + 3.2/3.3 · §13 non-goals → respected (no CMS/auth/i18n) · §14 risks → addressed (lazy R3F, motion ownership, reduced-motion, IP check 3.3) · §15 acceptance → 3.1–3.3 gates.

**Placeholder scan:** No TBD/TODO; every code step contains full code; commands have expected output.

**Type consistency:** `getModules/getModule/getNarrative` (lib/content), `getNotes` (lib/notes), `Module.domain` values match `FilterRail` option ids in 2.3, `Narrative` shape consistent across 2.5, motion primitive names stable.

**Gap added:** Task 3.4 not needed — IP boundary verification folded into 3.3 step 4 (spec §2/§15.6).
