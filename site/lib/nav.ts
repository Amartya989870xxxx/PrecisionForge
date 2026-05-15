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
