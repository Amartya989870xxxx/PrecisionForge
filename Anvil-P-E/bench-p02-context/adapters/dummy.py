"""
Naive baseline adapter for P-02.

Stores all events in memory. On reconstruct_context it returns last-30-min
events from the trigger service, plus any past incident_signals whose
service field matches by exact name (no rename handling). Picks the most
recent matching remediation as a suggestion.

Exists to validate the harness end-to-end. Submissions that match this
approach score near the floor by design — particularly on topology drift
recall.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Literal

from adapter import Adapter
from schema import Context, Event, IncidentSignal


def _parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


class DummyAdapter(Adapter):
    def __init__(self) -> None:
        self.events: list[Event] = []
        self.by_service: dict[str, list[Event]] = defaultdict(list)
        self.incidents_by_service: dict[str, list[Event]] = defaultdict(list)
        self.remediations: dict[str, Event] = {}

    def ingest(self, events: Iterable[Event]) -> None:
        for e in events:
            self.events.append(e)
            svc = e.get("service") or e.get("target") or e.get("from_")
            if svc:
                self.by_service[svc].append(e)
            kind = e.get("kind")
            if kind == "incident_signal":
                self.incidents_by_service[e.get("service", "")].append(e)
            elif kind == "remediation":
                self.remediations[e["incident_id"]] = e

    def reconstruct_context(
        self,
        signal: IncidentSignal,
        mode: Literal["fast", "deep"] = "fast",
    ) -> Context:
        svc = signal.get("service", "")
        ts = _parse(signal["ts"])
        window = timedelta(minutes=30)

        related = [
            e for e in self.by_service.get(svc, [])
            if abs(_parse(e["ts"]) - ts) <= window
        ][:20]

        matches = [
            {
                "incident_id": past["incident_id"],
                "similarity":  0.5,
                "rationale":   f"same service name '{svc}'",
            }
            for past in self.incidents_by_service.get(svc, [])
            if past["incident_id"] != signal["incident_id"]
        ][:5]

        suggestions = []
        for m in matches:
            rem = self.remediations.get(m["incident_id"])
            if rem:
                suggestions.append({
                    "action":             rem["action"],
                    "target":             rem.get("target", svc),
                    "historical_outcome": rem.get("outcome", "unknown"),
                    "confidence":         0.3,
                })
                break

        return {
            "related_events":         related,
            "causal_chain":           [],
            "similar_past_incidents": matches,
            "suggested_remediations": suggestions,
            "confidence":             0.3,
            "explain":                f"naive baseline: matched by exact service name '{svc}'",
        }

    def close(self) -> None:
        self.events.clear()
        self.by_service.clear()
        self.incidents_by_service.clear()
        self.remediations.clear()
