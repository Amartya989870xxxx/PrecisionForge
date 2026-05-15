"""
Event and Context types for P-02.

Mirrors the interface declared in Annex A of the problem statement.
"""
from __future__ import annotations

from typing import Any, Literal, TypedDict


# ---- input shapes ----

class Event(TypedDict, total=False):
    ts: str
    kind: Literal[
        "log", "metric", "trace",
        "deploy", "topology",
        "incident_signal", "remediation",
    ]
    service: str

    # kind-specific fields (all optional)
    level: str
    msg: str
    trace_id: str
    name: str
    value: float
    spans: list[dict[str, Any]]

    version: str
    actor: str

    change: str
    from_: str
    to: str

    incident_id: str
    trigger: str

    action: str
    target: str
    outcome: str

    attrs: dict[str, Any]


class IncidentSignal(TypedDict, total=False):
    incident_id: str
    ts: str
    trigger: str
    service: str


# ---- output shapes ----

class CausalEdge(TypedDict, total=False):
    cause_event_id: str
    effect_event_id: str
    evidence: str
    confidence: float


class IncidentMatch(TypedDict, total=False):
    incident_id: str
    similarity: float
    rationale: str


class Remediation(TypedDict, total=False):
    action: str
    target: str
    historical_outcome: str
    confidence: float


class Context(TypedDict, total=False):
    related_events: list[Event]
    causal_chain: list[CausalEdge]
    similar_past_incidents: list[IncidentMatch]
    suggested_remediations: list[Remediation]
    confidence: float
    explain: str
