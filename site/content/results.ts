export const results = [
  { label: "Mean Δ accuracy", value: 0.142, decimals: 3, prefix: "+" },
  { label: "Min Δ accuracy", value: 0.047, decimals: 3, prefix: "+", note: "every seed > 0; no halving" },
  { label: "Mean spread reduction", value: 1.03, decimals: 2, suffix: "×" },
  { label: "Total automated", value: 70.22, decimals: 2, suffix: " / 90" },
];
export const honestNote =
  "On the public synthetic operator, a ≥10× spread reduction is not reachable by any diagonal precision vector — it is a property of the operator, not a solver limitation. The geometry branch reports its true ceiling here while remaining the correct construction for the anisotropic held-out evaluation.";
