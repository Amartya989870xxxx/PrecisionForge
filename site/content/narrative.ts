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
