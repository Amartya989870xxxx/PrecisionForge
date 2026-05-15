"""Benchmark harness for P-01. Drives an Adapter through scenarios and scores it."""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from adapter import Adapter
from scenarios import chaos, randomized
from scenarios.reference import (
    FINAL_SYNC_ORDER,
    OPERATIONS,
    PEERS,
    SCHEMA,
    Stmt,
    Sync,
)
from scenarios.randomized import RandomizedConfig
from assertions import (
    AssertionResult,
    assert_cell_level_merge,
    assert_convergence,
    assert_fk_documented,
    assert_uniqueness_email,
)


# Axes and indicative weights for final scoring. Weights are illustrative;
# the council may rebalance before the event.
WEIGHTS: dict[str, float] = {
    "convergence":            0.30,
    "uniqueness:users.email": 0.20,
    "fk":                     0.15,
    "cell-level:u1":          0.10,
    "order-invariance":       0.10,
    "randomized":             0.15,
}


@dataclass
class ScenarioReport:
    scenario: str
    duration_ms: float
    snapshot_hashes: dict[str, str]
    state_sample: dict[str, Any] = field(default_factory=dict)
    assertions: list[AssertionResult] = field(default_factory=list)


def _apply_op(adapter: Adapter, op) -> None:
    if isinstance(op, Stmt):
        adapter.execute(op.peer, op.sql, op.params)
    elif isinstance(op, Sync):
        adapter.sync(op.a, op.b)


def run_reference(adapter: Adapter, stated_fk_policy: str) -> ScenarioReport:
    for p in PEERS:
        adapter.open_peer(p)
        adapter.apply_schema(p, SCHEMA)

    t0 = time.monotonic()
    for op in OPERATIONS:
        _apply_op(adapter, op)
    for a, b in FINAL_SYNC_ORDER:
        adapter.sync(a, b)
    duration = (time.monotonic() - t0) * 1000.0

    hashes = {p: adapter.snapshot_hash(p) for p in PEERS}
    state = adapter.snapshot_state(PEERS[0])

    return ScenarioReport(
        scenario="reference",
        duration_ms=duration,
        snapshot_hashes=hashes,
        state_sample=state,
        assertions=[
            assert_convergence(hashes),
            assert_uniqueness_email(state),
            assert_fk_documented(state, stated_fk_policy),
            assert_cell_level_merge(state),
        ],
    )


def run_chaos(adapter: Adapter, seeds: list[int]) -> list[ScenarioReport]:
    reports: list[ScenarioReport] = []
    canonical_hash: str | None = None

    for seed in seeds:
        scoped = {p: f"{p}@{seed}" for p in PEERS}
        for p in PEERS:
            adapter.open_peer(scoped[p])
            adapter.apply_schema(scoped[p], SCHEMA)

        t0 = time.monotonic()
        for op in OPERATIONS:
            if isinstance(op, Stmt):
                adapter.execute(scoped[op.peer], op.sql, op.params)
            else:
                adapter.sync(scoped[op.a], scoped[op.b])
        for a, b in chaos.permute_sync_order(seed):
            adapter.sync(scoped[a], scoped[b])
        duration = (time.monotonic() - t0) * 1000.0

        hashes = {p: adapter.snapshot_hash(scoped[p]) for p in PEERS}
        state = adapter.snapshot_state(scoped[PEERS[0]])

        conv = assert_convergence(hashes)
        peer_a_hash = hashes[PEERS[0]]
        if canonical_hash is None:
            canonical_hash = peer_a_hash
            inv = AssertionResult(
                "order-invariance",
                True,
                f"first canonical hash seed={seed}",
            )
        elif peer_a_hash == canonical_hash:
            inv = AssertionResult(
                "order-invariance",
                True,
                f"seed={seed} matches canonical",
            )
        else:
            inv = AssertionResult(
                "order-invariance",
                False,
                f"seed={seed} produced {peer_a_hash[:12]}…, "
                f"canonical={canonical_hash[:12]}…",
            )

        reports.append(ScenarioReport(
            scenario=f"chaos:seed={seed}",
            duration_ms=duration,
            snapshot_hashes=hashes,
            state_sample=state,
            assertions=[conv, inv],
        ))

    return reports


def run_randomized(
    adapter: Adapter,
    seeds: list[int],
    n_peers: int = 4,
    n_ops: int = 80,
) -> list[ScenarioReport]:
    reports: list[ScenarioReport] = []

    for seed in seeds:
        cfg = RandomizedConfig(seed=seed, n_peers=n_peers, n_ops=n_ops)
        peers, ops, tail = randomized.generate(cfg)
        scoped = {p: f"R{seed}:{p}" for p in peers}

        for p in peers:
            adapter.open_peer(scoped[p])
            adapter.apply_schema(scoped[p], SCHEMA)

        t0 = time.monotonic()
        for op in ops:
            if isinstance(op, Stmt):
                adapter.execute(scoped[op.peer], op.sql, op.params)
            else:
                adapter.sync(scoped[op.a], scoped[op.b])
        for a, b in tail:
            adapter.sync(scoped[a], scoped[b])
        duration = (time.monotonic() - t0) * 1000.0

        hashes = {p: adapter.snapshot_hash(scoped[p]) for p in peers}
        state = adapter.snapshot_state(scoped[peers[0]])

        # idempotence: a second pass of pairwise sync must not mutate state
        for a, b in tail[: len(peers)]:
            adapter.sync(scoped[a], scoped[b])
        hashes_after = {p: adapter.snapshot_hash(scoped[p]) for p in peers}
        idempotent = AssertionResult(
            "idempotent-sync",
            hashes == hashes_after,
            "second sync pass left state unchanged"
            if hashes == hashes_after
            else f"state changed on second sync — quiescence not reached",
        )

        results = [
            assert_convergence(hashes),
            assert_uniqueness_email(state),
            idempotent,
        ]

        reports.append(ScenarioReport(
            scenario=f"randomized:seed={seed}:peers={n_peers}:ops={n_ops}",
            duration_ms=duration,
            snapshot_hashes=hashes,
            state_sample={
                t: rows[:5] for t, rows in state.items()
            },
            assertions=results,
        ))

    return reports


def compute_score(
    reference: ScenarioReport,
    chaos_runs: list[ScenarioReport],
    randomized_runs: list[ScenarioReport] | None = None,
) -> dict[str, Any]:
    axis_pass: dict[str, bool] = {}

    for r in reference.assertions:
        key = "fk" if r.name.startswith("fk:") else r.name
        axis_pass[key] = r.passed

    if chaos_runs:
        axis_pass["order-invariance"] = all(
            any(a.name == "order-invariance" and a.passed for a in run.assertions)
            for run in chaos_runs
        )

    if randomized_runs:
        # randomized passes only if EVERY seed passes EVERY randomized invariant
        axis_pass["randomized"] = all(
            all(a.passed for a in run.assertions)
            for run in randomized_runs
        )

    total = sum(WEIGHTS.get(k, 0.0) for k, v in axis_pass.items() if v)
    return {"axes": axis_pass, "weighted_score": round(total, 4), "max": 1.0}


def render(reports: list[ScenarioReport], score: dict[str, Any]) -> str:
    return json.dumps(
        {
            "score": score,
            "scenarios": [asdict(r) for r in reports],
        },
        indent=2,
        default=str,
    )
