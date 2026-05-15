"""
Synthetic telemetry generator for P-02 with deterministic seed.

Produces:
  - N services with renamed-over-time aliases
  - Background metrics (low signal)
  - Deployment events
  - Topology mutations (renames, dependency changes)
  - Incidents drawn from K recurring families. Each incident is a pattern
    of (deploy, latency metric, upstream error log, signal, remediation).
    Incident families repeat across the dataset with morphed signatures,
    so the engine must recognise the family even when the involved service
    has been renamed.

Train / eval split: 70 / 30 by time. Eval signals are held out — the
engine sees pre-signal context but not the remediation, which it must
predict.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from schema import Event


@dataclass
class GenConfig:
    seed: int = 42
    n_services: int = 12
    days: int = 7
    deploys: int = 30
    topology_mutations: int = 8
    incidents_train: int = 24
    incidents_eval: int = 10
    incident_families: int = 5
    background_density: int = 200  # events per service-day
    start_ts: str = "2026-05-01T00:00:00Z"


@dataclass
class Dataset:
    train_events: list[Event]
    eval_events: list[Event]
    eval_signals: list[Event]
    ground_truth: list[dict[str, Any]]
    config: GenConfig = field(default_factory=GenConfig)


def _parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate(cfg: GenConfig | None = None) -> Dataset:
    cfg = cfg or GenConfig()
    rng = random.Random(cfg.seed)

    start = _parse(cfg.start_ts)
    duration = timedelta(days=cfg.days)
    train_cutoff = start + duration * 0.7
    end = start + duration

    canonical = [f"svc-{i:02d}" for i in range(cfg.n_services)]
    # alias[canonical_id] = currently-alive name
    alias: dict[str, str] = {s: s for s in canonical}

    train: list[Event] = []
    eval_: list[Event] = []
    signals: list[Event] = []
    truth: list[dict[str, Any]] = []

    def emit(e: Event, t: datetime) -> None:
        (train if t < train_cutoff else eval_).append(e)

    # ---- topology mutations ----
    mutation_times = sorted(start + duration * rng.random()
                            for _ in range(cfg.topology_mutations))
    for mt in mutation_times:
        change = rng.choices(
            ["rename", "dep_add", "dep_remove"],
            weights=[0.6, 0.2, 0.2],
        )[0]
        if change == "rename":
            victim = rng.choice(canonical)
            old = alias[victim]
            new = f"{victim}-r{rng.randint(2, 9)}"
            emit({
                "ts": _iso(mt), "kind": "topology", "change": "rename",
                "from_": old, "to": new,
            }, mt)
            alias[victim] = new
        else:
            a, b = rng.sample(canonical, 2)
            emit({
                "ts": _iso(mt), "kind": "topology", "change": change,
                "from_": alias[a], "to": alias[b],
            }, mt)

    # ---- deploys ----
    for _ in range(cfg.deploys):
        t = start + duration * rng.random()
        s = rng.choice(canonical)
        emit({
            "ts": _iso(t), "kind": "deploy",
            "service": alias[s],
            "version": f"v{rng.randint(1, 9)}.{rng.randint(0, 99)}.{rng.randint(0, 9)}",
            "actor": "ci",
        }, t)

    # ---- incident families & patterns ----
    family_services: dict[int, str] = {
        fam: rng.choice(canonical) for fam in range(cfg.incident_families)
    }

    def emit_incident(t: datetime, fam: int, is_eval: bool) -> None:
        canonical_svc = family_services[fam]
        live_svc = alias[canonical_svc]
        version = f"v{rng.randint(1, 9)}.{rng.randint(0, 99)}.{rng.randint(0, 9)}"
        prev_version = f"v{rng.randint(1, 9)}.{rng.randint(0, 99)}.{rng.randint(0, 9)}"
        upstream = alias[rng.choice([c for c in canonical if c != canonical_svc])]
        trace_id = f"tr-{rng.randint(100000, 999999)}"
        incident_id = f"INC-{int(t.timestamp()) % 100000}-{fam}"

        pre = [
            {
                "ts": _iso(t - timedelta(minutes=30)), "kind": "deploy",
                "service": live_svc, "version": version, "actor": "ci",
            },
            {
                "ts": _iso(t - timedelta(minutes=10)), "kind": "metric",
                "service": live_svc, "name": "latency_p99_ms",
                "value": float(rng.randint(3000, 9000)),
            },
            {
                "ts": _iso(t - timedelta(seconds=30)), "kind": "log",
                "service": upstream, "level": "error",
                "msg": f"timeout calling {live_svc}",
                "trace_id": trace_id,
            },
        ]
        signal: Event = {
            "ts": _iso(t), "kind": "incident_signal",
            "incident_id": incident_id,
            "trigger": f"alert:{live_svc}/latency_p99_ms>3000",
            "service": live_svc,
        }
        remediation: Event = {
            "ts": _iso(t + timedelta(minutes=20)), "kind": "remediation",
            "incident_id": incident_id, "action": "rollback",
            "target": live_svc, "version": prev_version, "outcome": "resolved",
        }

        for e in pre:
            emit(e, _parse(e["ts"]))

        if is_eval:
            eval_.append(signal)
            signals.append(signal)
            truth.append({
                "incident_id":              incident_id,
                "family":                   fam,
                "trigger_service_live":     live_svc,
                "trigger_service_canonical": canonical_svc,
                "expected_remediation":     "rollback",
            })
        else:
            train.append(signal)
            train.append(remediation)

    for _ in range(cfg.incidents_train):
        t = start + (train_cutoff - start) * rng.random()
        emit_incident(t, rng.randrange(cfg.incident_families), is_eval=False)

    for _ in range(cfg.incidents_eval):
        t = train_cutoff + (end - train_cutoff) * rng.random()
        emit_incident(t, rng.randrange(cfg.incident_families), is_eval=True)

    # ---- background telemetry ----
    n_bg = cfg.n_services * cfg.days * cfg.background_density
    for _ in range(n_bg):
        t = start + duration * rng.random()
        s = rng.choice(canonical)
        e: Event = {
            "ts": _iso(t), "kind": "metric",
            "service": alias[s], "name": "qps",
            "value": float(rng.randint(10, 1000)),
        }
        emit(e, t)

    train.sort(key=lambda e: e["ts"])
    eval_.sort(key=lambda e: e["ts"])
    signals.sort(key=lambda e: e["ts"])

    return Dataset(
        train_events=train,
        eval_events=eval_,
        eval_signals=signals,
        ground_truth=truth,
        config=cfg,
    )
