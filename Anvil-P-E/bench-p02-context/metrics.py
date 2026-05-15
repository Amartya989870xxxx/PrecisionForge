"""Scoring metrics for P-02."""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any

from schema import Context


@dataclass
class IncidentScore:
    incident_id: str
    correct_family_in_top_k: bool
    precision_at_k: float
    remediation_matches: bool
    latency_ms: float


def _family_from_incident_id(iid: str) -> int | None:
    try:
        return int(iid.rsplit("-", 1)[-1])
    except (ValueError, IndexError):
        return None


def score_match(
    ctx: Context,
    ground_truth: dict[str, Any],
    k: int = 5,
) -> tuple[bool, float]:
    matches = (ctx.get("similar_past_incidents") or [])[:k]
    target = ground_truth["family"]
    hits = [
        _family_from_incident_id(m.get("incident_id", "")) == target
        for m in matches
    ]
    in_top_k = any(hits)
    precision = (sum(hits) / k) if hits else 0.0
    return in_top_k, precision


def score_remediation(ctx: Context, ground_truth: dict[str, Any]) -> bool:
    expected = ground_truth["expected_remediation"]
    return any(
        s.get("action") == expected
        for s in (ctx.get("suggested_remediations") or [])
    )


def aggregate(scores: list[IncidentScore]) -> dict[str, Any]:
    if not scores:
        return {"n": 0}
    sorted_latencies = sorted(s.latency_ms for s in scores)
    p95_idx = max(0, int(0.95 * len(sorted_latencies)) - 1)
    return {
        "recall@5":          round(mean(1.0 if s.correct_family_in_top_k else 0.0 for s in scores), 4),
        "precision@5_mean":  round(mean(s.precision_at_k for s in scores), 4),
        "remediation_acc":   round(mean(1.0 if s.remediation_matches else 0.0 for s in scores), 4),
        "latency_p95_ms":    round(sorted_latencies[p95_idx], 2),
        "latency_mean_ms":   round(mean(s.latency_ms for s in scores), 2),
        "n":                 len(scores),
    }
