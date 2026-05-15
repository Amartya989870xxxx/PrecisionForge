"""Benchmark harness for P-02."""
from __future__ import annotations

import time
from dataclasses import asdict
from typing import Any

from adapter import Adapter
from generator import Dataset, GenConfig, generate
from metrics import IncidentScore, aggregate, score_match, score_remediation
from schema import Context, IncidentSignal


# Indicative axis weights. Council may rebalance before the event.
WEIGHTS: dict[str, float] = {
    "recall@5":         0.30,
    "precision@5_mean": 0.15,
    "remediation_acc":  0.20,
    "latency_p95_ms":   0.15,  # scored against the budget below
    "manual_context":   0.10,  # panel-graded, stub in automated run
    "manual_explain":   0.10,  # panel-graded, stub in automated run
}

LATENCY_BUDGET_MS: dict[str, float] = {
    "fast": 2000.0,
    "deep": 6000.0,
}


def _run_one_seed(
    adapter_factory,
    cfg: GenConfig,
    mode: str,
    warmup: int,
) -> dict[str, Any]:
    """Run a single seed in isolation. Adapter is freshly constructed
    so cached state from prior seeds cannot leak."""
    adapter: Adapter = adapter_factory()
    try:
        ds: Dataset = generate(cfg)

        t0 = time.monotonic()
        adapter.ingest(ds.train_events)
        adapter.ingest(ds.eval_events)
        ingest_ms = (time.monotonic() - t0) * 1000.0

        # warmup: discard timings on the first few queries so caches / JIT settle
        for sig in ds.eval_signals[:warmup]:
            signal: IncidentSignal = {
                "incident_id": sig["incident_id"],
                "ts":          sig["ts"],
                "trigger":     sig.get("trigger", ""),
                "service":     sig.get("service", ""),
            }
            adapter.reconstruct_context(signal, mode=mode)  # type: ignore[arg-type]

        scores: list[IncidentScore] = []
        for sig, gt in zip(ds.eval_signals, ds.ground_truth):
            signal = {
                "incident_id": sig["incident_id"],
                "ts":          sig["ts"],
                "trigger":     sig.get("trigger", ""),
                "service":     sig.get("service", ""),
            }
            q0 = time.monotonic()
            ctx: Context = adapter.reconstruct_context(signal, mode=mode)  # type: ignore[arg-type]
            latency = (time.monotonic() - q0) * 1000.0

            in_top_k, precision = score_match(ctx, gt, k=5)
            rem_ok = score_remediation(ctx, gt)

            scores.append(IncidentScore(
                incident_id=sig["incident_id"],
                correct_family_in_top_k=in_top_k,
                precision_at_k=precision,
                remediation_matches=rem_ok,
                latency_ms=latency,
            ))

        summary = aggregate(scores)
        return {
            "seed":         cfg.seed,
            "config":       asdict(cfg),
            "ingest_ms":    round(ingest_ms, 2),
            "n_train":      len(ds.train_events),
            "n_eval":       len(ds.eval_events),
            "n_signals":    len(ds.eval_signals),
            "mode":         mode,
            "per_incident": [asdict(s) for s in scores],
            "summary":      summary,
        }
    finally:
        adapter.close()


def run(
    adapter_factory,
    cfg: GenConfig | None = None,
    mode: str = "fast",
    seeds: list[int] | None = None,
    warmup: int = 2,
) -> dict[str, Any]:
    """Run across one or many seeds. Each seed is run in a fresh adapter
    instance to ensure no information leaks between seeds — this is also
    what makes the bench robust to in-memory caching tricks."""
    cfg = cfg or GenConfig()
    if seeds is None:
        seeds = [cfg.seed]

    per_seed: list[dict[str, Any]] = []
    for s in seeds:
        seed_cfg = GenConfig(**{**asdict(cfg), "seed": s})
        per_seed.append(_run_one_seed(adapter_factory, seed_cfg, mode, warmup))

    # aggregate across seeds (mean of per-seed metrics)
    def _mean(key: str) -> float:
        vals = [r["summary"].get(key, 0.0) for r in per_seed if r["summary"].get("n", 0) > 0]
        return round(sum(vals) / len(vals), 4) if vals else 0.0

    n_total = sum(r["n_signals"] for r in per_seed)
    aggregated_summary = {
        "recall@5":         _mean("recall@5"),
        "precision@5_mean": _mean("precision@5_mean"),
        "remediation_acc":  _mean("remediation_acc"),
        "latency_p95_ms":   round(max(r["summary"].get("latency_p95_ms", 0.0) for r in per_seed), 2),
        "latency_mean_ms":  _mean("latency_mean_ms"),
        "n_seeds":          len(per_seed),
        "n_signals_total":  n_total,
        "n":                n_total,
    }
    final = compute_score(aggregated_summary, mode)

    return {
        "mode":       mode,
        "seeds":      seeds,
        "per_seed":   per_seed,
        "aggregated": aggregated_summary,
        "score":      final,
    }


def compute_score(summary: dict[str, Any], mode: str) -> dict[str, Any]:
    """Compose a weighted score from the automated metrics. Manual axes
    are reserved (panel-graded) and surfaced as None in the report."""
    if not summary or summary.get("n", 0) == 0:
        return {"weighted_score": 0.0, "axes": {}}

    budget = LATENCY_BUDGET_MS.get(mode, 2000.0)
    latency_ratio = max(0.0, min(1.0, budget / max(summary["latency_p95_ms"], 1e-6)))

    axes = {
        "recall@5":         summary["recall@5"],
        "precision@5_mean": summary["precision@5_mean"],
        "remediation_acc":  summary["remediation_acc"],
        "latency_p95_ms":   round(latency_ratio, 4),
        "manual_context":   None,
        "manual_explain":   None,
    }

    weighted = 0.0
    for k, v in axes.items():
        if isinstance(v, (int, float)):
            weighted += WEIGHTS[k] * v

    return {
        "axes":           axes,
        "weighted_score": round(weighted, 4),
        "max_automated":  round(sum(w for k, w in WEIGHTS.items()
                                    if not k.startswith("manual_")), 4),
        "note":           "manual_* axes are panel-graded and excluded from "
                          "the automated score",
    }
