# Precision Memory Agent — Marketing Site Design Spec

- **Date:** 2026-05-16
- **Status:** Approved (brainstorm complete) — ready for implementation planning
- **Branch:** `feat/precision-memory-agent-site`
- **Author:** brainstorm session with the user

## 1. Summary

Build a premium, animation-rich marketing/documentation website for the
**Precision Memory Agent** project. The **layout system, section structure,
and motion design** are recreated from the public reference site
`coffee-tech.com` (a Webflow-built industrial product site) as a *structural
and behavioural reference only*. The site ships with **100% original
branding and content** about the actual project (the PCAM two-regime
precision controller, `Anvil-P-E`, and the `w` adapter).

## 2. Legal & content boundary (binding constraint)

The user confirmed the reference is **"reference only"** — not their site, no
permission to copy assets.

- ✅ **Recreate:** layout patterns, section ordering, grid/composition,
  scroll/reveal/transition behaviour, carousel and interaction mechanics.
  These are functional/idea-level and not the protected expression.
- ❌ **Never reproduce:** the reference site's copy, headlines, photographs,
  logo/wordmark, product names, testimonial text, or any media asset.
- All text, imagery, product/module names, and the 3D hero are **original**,
  derived from the project's own `w/README.md` and `Anvil-P-E/` material.
- Brand identity = **"Precision Memory Agent"** (this repository's project),
  restyled into the referenced layout/motion language.

## 3. Locked decisions (from brainstorm)

| Decision | Choice |
|---|---|
| Asset rights | Reference only — recreate patterns, original assets/content |
| Stack | New Next.js (App Router) + React + TypeScript app |
| Location | `/Users/aks/Precision_Memory_Agent/site/` (subfolder, never repo root) |
| Scope | Full site — all templates |
| Branding | Tie to this project: "Precision Memory Agent" |
| Hero 3D | Procedural WebGL via `@react-three/fiber` |
| Build method | Multi-agent, phased (foundation → shared → pages → QA) |
| Implementation approach | **A** — App Router · SSG · token-driven · full motion stack |
| Content source | Local typed data + MDX (no CMS — YAGNI) |

## 4. Brand & design tokens

Industrial-premium, amber-on-near-black, flat surfaces, minimal radius,
generous whitespace. Tokens live in one file (`styles/tokens.css`) as CSS
variables so the brand can be reskinned in one place.

```
color.bg        #0B0B0C      color.surface   #15161A
color.text      #F4F4F5      color.text-muted#8A8A93
color.accent    #F5A524      color.accent-2  #C9821B
color.border    rgba(255,255,255,.08)
font.display    "Space Grotesk"   font.body "Inter"   font.mono "JetBrains Mono"
radius.sm 4px / md 8px / lg 14px
space.base 8px  scale 4/8/12/16/24/32/48/64/96/128
container.max 1280px  gutter 24px  side-pad 20px (mobile) / 40px (desktop)
shadow.sm/md (subtle, low-opacity)  motion.ease [0.22,1,0.36,1]
```

Type scale (modular ~1.25, fluid `clamp()`): H1 hero 56–80px · H2 36–48px ·
H3 24–30px · H4 18–20px · body 16–18px · small 14px · mono labels 12–13px.

## 5. Information architecture & routes

Header: wordmark left · centred primary nav · right utility nav ·
language affordance (UI only, English content). **Not sticky** (matches
reference) — header sits at top and scrolls away; a slim scroll-to-top
control appears after first viewport.

| Route | Template | Purpose |
|---|---|---|
| `/` | Homepage | 9-section narrative |
| `/modules` | Modules Index/Filter | Filterable module grid |
| `/modules/[slug]` | Module Detail | Per-module deep dive |
| `/notes` | Notes Index | Research notes hub (Guides/News tabs) |
| `/notes/[slug]` | Note Article | MDX long-form |
| `/about` | Narrative | Project overview |
| `/method` | Narrative | How the controller works |
| `/performance` | Narrative | Benchmarks & honest results |
| `/reproducibility` | Narrative | Setup, determinism, run instructions |
| `/contact` | Contact | Form + info |
| `/faq` | FAQ | Accordion + search |
| `/legal` | Legal | Privacy & Terms |

Footer: 5 columns (Project · Sitemap · Resources · Modules · Social) +
bottom bar (copyright · legal link · scroll-to-top).

## 6. Homepage — 9 sections

Each section: layout pattern · original PMA content mapping · motion.

1. **Hero** — full-bleed R3F "precision memory lattice" particle field +
   centred headline + sub-line + dual CTA. *Content:* the agent's one-line
   value proposition. *Motion:* session preloader curtain → staggered
   headline reveal; lattice mouse-parallax; subtle scroll-coupled camera.
2. **Value prop** — single bold statement + "Read more" link. *Content:*
   deterministic two-regime precision controller, NumPy-only, no retraining.
   *Motion:* fade + upward reveal on enter.
3. **Modules grid** — 4 cards + "See all". *Content:* Anvil-P-E ·
   `w`-adapter (`Engine`) · Corruption-map controller · Geometry branch.
   *Motion:* staggered card rise; hover lift.
4. **Domains toggle** — 3-column switch (image/diagram + text per tab).
   *Content:* Retrieval · Anisotropy · Robustness. *Motion:* crossfade +
   content slide on toggle.
5. **Method carousel** — numbered slides, prev/next. *Content:* corruption
   map → class-conditional nudge → geometry/Hessian branch → blended branch
   decision. *Motion:* Swiper slide; animated step number.
6. **Results band** — honest benchmark figures carousel (NOT testimonials —
   no fabricated quotes). *Content:* public self-check figures from the
   repo README (mean Δacc +0.142, min +0.047, mean spread 1.03×, total
   70.22/90) + the honest anisotropy-ceiling note. *Motion:* count-up on
   enter; auto-advance; manual arrows.
7. **Approach** — 3 linked blocks. *Content:* Method · Performance ·
   Reproducibility (link to the narrative pages). *Motion:* hover lift +
   image zoom; reveal stagger.
8. **Notes** — research-notes carousel with arrows. *Content:* original
   short notes derived from the approach/honest-result sections. *Motion:*
   drag/inertia carousel.
9. **Footer CTA** — centred prompt + 2 buttons → then global footer.
   *Motion:* reveal; button magnetic hover (reduced-motion safe).

## 7. Inner templates (8)

1. **Module Detail** — breadcrumb · hero (name · tagline · spec chips ·
   small R3F/diagram) · sticky spec rail + long-form (overview, method,
   equations, benchmark table) · related modules · CTA. *Motion:* sticky
   rail, scroll-reveal sections, count-up benchmarks.
2. **Modules Index/Filter** — filter rail (All · Retrieval · Anisotropy ·
   Robustness · Tools) + responsive card grid. *Motion:* animated filter
   (Framer layout), staggered grid.
3. **Notes Index** — hero + Guides/News tabs + featured + card grid.
   *Motion:* tab crossfade, staggered cards, hover image-zoom.
4. **Note Article** — cover + meta · sticky TOC · MDX body (code, figures)
   · prev/next · related. *Motion:* reading-progress bar, TOC active-state,
   figure reveal.
5. **Narrative** (serves `/about`, `/method`, `/performance`,
   `/reproducibility` — one template, four content sets) — full-bleed
   narrative hero · pinned scrollytelling · alternating 2-col · stats band.
   *Motion:* GSAP pin + scrub, parallax layers, count-up.
6. **Contact** — split form (name/email/message, client-validated) + info
   column. *Motion:* input focus states; submit → success transition.
   Submission posts to a configurable endpoint (env var); no secret in code.
7. **FAQ** — search filter + accordion. *Motion:* smooth height expand,
   chevron rotate.
8. **Legal** — TOC + long-form typography. *Motion:* anchor smooth-scroll
   only.

## 8. Motion system

Site-wide, accessibility-first. Every effect has a static
`prefers-reduced-motion` fallback.

| Concern | Library | Responsibility | Key params |
|---|---|---|---|
| Smooth/inertia scroll | Lenis | Eased scroll; drives ScrollTrigger | lerp 0.1, duration 1.2 |
| Reveal/stagger/route transition | Framer Motion | Section reveals, stagger, `AnimatePresence` route crossfade | y:24→0, opacity 0→1, dur .6, ease [0.22,1,0.36,1], stagger .08 |
| Pin/scrub scrollytelling | GSAP + ScrollTrigger | Narrative pinning, parallax, count-up, hero scroll-coupling | scrub 1, pin spacing, start "top top" |
| Carousels | Swiper | Method/results/notes sliders, drag, numbered indicators | responsive slidesPerView, speed 600 |
| Hero 3D | @react-three/fiber + drei + postprocessing | Instanced particle lattice, mouse-parallax, bloom | DPR clamp [1,2], demand frameloop on idle, mobile static snapshot |
| Preloader/curtain | Framer Motion | First-paint curtain → hero reveal | once/session, dur .9 |

**Performance guardrails:** R3F via `next/dynamic` `ssr:false` +
IntersectionObserver pause when offscreen; instanced points (single draw
call); `next/image` AVIF/WebP; lazy-mount below-fold sections; targets
Lighthouse Performance ≥ 90, Accessibility = 100, no CLS from hero.

## 9. Architecture

New app at `site/` (subfolder; never repo root):

```
site/
  app/                 # App Router routes (one folder per route)
  components/
    layout/            # Header, Footer, Container, ScrollTop
    sections/          # Homepage + template section components
    ui/                # Button, Card, Carousel, Accordion, Tabs, FilterRail, Field
  motion/              # MotionProvider (Lenis+GSAP), variants, Reveal, Stagger, ScrollPin, CountUp
  three/               # HeroScene, lattice geometry, shaders, reduced-motion fallback
  content/             # Typed data (modules, results, faq, narrative) + notes/*.mdx
  lib/                 # utils, mdx, seo, validation
  styles/              # tokens.css, globals.css
  tests/               # Vitest + RTL setup
  public/              # original generated/placeholder media (AVIF/SVG)
```

- Next.js 15 App Router, TypeScript strict, static-export compatible.
- Tailwind configured to read CSS-variable tokens.
- Content typed in `content/*.ts`; notes authored as MDX.
- Component files < 500 lines, one component per file, immutable data flow.
- SEO: per-route metadata, OpenGraph, sitemap, robots.

## 10. Multi-agent decomposition

Phased; each phase is one parallel batch, reviewed before the next. No
status-polling — agents return results.

- **Phase 0 — Foundation (1 agent, blocking):** scaffold Next.js +
  TypeScript + Tailwind + tokens; ESLint/Prettier/Vitest; `MotionProvider`
  (Lenis + GSAP registry); `Layout/Header/Footer/Container`.
- **Phase 1 — Shared systems (3 agents ∥):** (a) motion primitives
  (variants, `Reveal`, `Stagger`, `ScrollPin`, `CountUp`, route
  transition); (b) R3F hero scene + reduced-motion fallback; (c) UI kit
  (Button, Card, Carousel/Swiper wrapper, Accordion, Tabs, FilterRail,
  form fields) — all TDD (Vitest + RTL).
- **Phase 2 — Pages (5 agents ∥):** (1) Homepage 9 sections; (2) Modules
  index + detail; (3) Notes index + article (MDX pipeline); (4) Narrative
  template + 4 content sets; (5) Contact + FAQ + Legal.
- **Phase 3 — Integration & QA (1 agent):** route transitions, nav wiring,
  responsive sweep, Lighthouse + a11y pass; `code-reviewer` and
  `build-error-resolver` gates; full `build` + `test` green.

## 11. Dependencies

`next` `react` `react-dom` `typescript` · `tailwindcss` `postcss`
`autoprefixer` · `framer-motion` · `gsap` (ScrollTrigger) · `lenis` ·
`swiper` · `three` `@react-three/fiber` `@react-three/drei`
`@react-three/postprocessing` · `@next/mdx` + MDX toolchain · dev:
`vitest` `@testing-library/react` `@testing-library/jest-dom` `jsdom`
`eslint` `prettier`. All installed during Phase 0.

## 12. Testing & quality gates

- Unit/component tests (Vitest + RTL) for UI kit, motion primitives
  (reduced-motion branches), content loaders — target ≥ 80% coverage.
- Integration: route rendering, MDX pipeline, filter/tab/accordion logic.
- E2E (Phase 3): critical flows — nav, hero load, carousel, contact submit,
  reduced-motion. Framework chosen at plan time (Playwright default).
- Build must pass and tests green before Phase 3 closes; `code-reviewer`
  on each phase's output.

## 13. Non-goals (YAGNI)

No CMS, no i18n content (UI affordance only), no auth/accounts, no
e-commerce, no blog authoring UI, no server backend beyond a single
configurable contact endpoint, no exact pixel-cloning of reference media.

## 14. Risks & mitigations

| Risk | Mitigation |
|---|---|
| R3F hero hurts perf/LCP | Lazy `ssr:false`, instancing, DPR clamp, mobile static snapshot, IO pause |
| Motion-library overlap (Framer vs GSAP) | Clear ownership: Framer = reveal/stagger/route; GSAP = pin/scrub; Lenis owns scroll |
| Scope (12 routes) large | Phased multi-agent; Narrative template reused ×4; shared UI kit first |
| Accidental reference-content leakage | Content boundary §2; all copy original from repo README; review gate checks |
| Motion sickness/accessibility | `prefers-reduced-motion` static fallbacks everywhere; a11y = 100 gate |

## 15. Acceptance criteria

1. All 12 routes implemented with the specified layout + motion.
2. Brand reskinnable from `styles/tokens.css` alone.
3. R3F hero runs ≥ 50 fps desktop, static fallback on reduced-motion/mobile.
4. Lighthouse: Performance ≥ 90, Accessibility = 100; no hero CLS.
5. `npm run build` succeeds; `npm test` green; coverage ≥ 80%.
6. Zero reference-site copy, media, names, or logo present anywhere.
7. Content is accurate to the project (honest benchmark figures, honest
   anisotropy-ceiling note included).
