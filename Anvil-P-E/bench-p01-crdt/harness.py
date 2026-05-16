"""Benchmark harness for P-01. Drives an Adapter through scenarios and scores it."""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from adapter import Adapter
from scenarios import cell_level, chaos, randomized
from scenarios.reference import (
    FINAL_SYNC_ORDER,
    OPERATIONS,
    PEERS,
    SCHEMA,
    Stmt,
    Sync,
)
from scenarios.randomized import RandomizedConfig
from scenarios.stretch import REGISTRY as STRETCH_REGISTRY
from assertions import (
    AssertionResult,
    assert_cell_level_merge,
    assert_cell_level_strict,
    assert_convergence,
    assert_data_preservation,
    assert_fk_documented,
    assert_uniqueness_email,
)


# L1/L2 axes and indicative weights. Weights are illustrative; the
# council may rebalance before the event. L3 stretch scenarios are
# scored separately via stretch_score() so they don't dilute the
# core L1/L2 number.
WEIGHTS: dict[str, float] = {
    "convergence":            0.25,
    "uniqueness:users.email": 0.15,
    "fk":                     0.10,
    "cell-level:u1":          0.05,   # vacuous-on-cascade — kept for compat
    "cell-level-strict":      0.20,   # non-vacuous — kills LWW
    "order-invariance":       0.10,
    "randomized":             0.15,
}


# L3 stretch scenarios — each scenario is one axis, equal weight inside
# the L3 score (council can rebalance via the L3 config file).
STRETCH_WEIGHTS: dict[str, float] = {
    "composite_uniqueness": 0.25,
    "multi_level_fk":       0.25,
    "high_density":         0.25,
    "long_run":             0.25,
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


def run_cell_level(adapter: Adapter) -> ScenarioReport:
    """Pure cell-level merge scenario — non-vacuous test of column merging.

    Setup ensures u1 is never deleted and never has a uniqueness conflict,
    so the only thing being tested is whether the engine preserves BOTH
    concurrent column updates. LWW-on-row implementations fail by design.
    """
    scoped = {p: f"CL:{p}" for p in PEERS}
    for p in PEERS:
        adapter.open_peer(scoped[p])
        adapter.apply_schema(scoped[p], SCHEMA)

    t0 = time.monotonic()
    for op in cell_level.OPERATIONS:
        if isinstance(op, Stmt):
            adapter.execute(scoped[op.peer], op.sql, op.params)
        else:
            adapter.sync(scoped[op.a], scoped[op.b])
    for a, b in cell_level.FINAL_SYNC_ORDER:
        adapter.sync(scoped[a], scoped[b])
    duration = (time.monotonic() - t0) * 1000.0

    hashes = {p: adapter.snapshot_hash(scoped[p]) for p in PEERS}
    state = adapter.snapshot_state(scoped[PEERS[0]])

    return ScenarioReport(
        scenario="cell-level-strict",
        duration_ms=duration,
        snapshot_hashes=hashes,
        state_sample=state,
        assertions=[
            assert_convergence(hashes),
            assert_cell_level_strict(state),
        ],
    )


def run_stretch_scenario(adapter: Adapter,
                         scenario_name: str,
                         scope_prefix: str = "S") -> ScenarioReport:
    """Run a single stretch / L3 scenario module from the registry."""
    mod = STRETCH_REGISTRY[scenario_name]
    scoped = {p: f"{scope_prefix}:{scenario_name}:{p}" for p in mod.PEERS}

    for p in mod.PEERS:
        adapter.open_peer(scoped[p])
        adapter.apply_schema(scoped[p], mod.SCHEMA)

    t0 = time.monotonic()
    for op in mod.OPERATIONS:
        if isinstance(op, Stmt):
            adapter.execute(scoped[op.peer], op.sql, op.params)
        else:
            adapter.sync(scoped[op.a], scoped[op.b])
    for a, b in mod.FINAL_SYNC:
        adapter.sync(scoped[a], scoped[b])
    duration = (time.monotonic() - t0) * 1000.0

    hashes = {p: adapter.snapshot_hash(scoped[p]) for p in mod.PEERS}
    state = adapter.snapshot_state(scoped[mod.PEERS[0]])

    return ScenarioReport(
        scenario=f"stretch:{scenario_name}",
        duration_ms=duration,
        snapshot_hashes=hashes,
        state_sample=state,
        assertions=mod.run_assertions(state, hashes),
    )


def run_stretch_all(adapter: Adapter,
                    scenarios: list[str] | None = None,
                    scope_prefix: str = "S") -> list[ScenarioReport]:
    """Run every named stretch scenario (defaults to the full registry)."""
    names = scenarios if scenarios is not None else list(STRETCH_REGISTRY.keys())
    return [run_stretch_scenario(adapter, n, scope_prefix) for n in names]


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
        peers, ops, tail, inserted_ids, deleted_ids = randomized.generate(cfg)
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

        # Data preservation: catch INSERT OR REPLACE-style silent drops.
        # No randomized scenario triggers cascade (orders never inserted),
        # so cascaded_ids is empty — every inserted id must be present or
        # explicitly deleted.
        preservation = assert_data_preservation(
            inserted_ids, deleted_ids, set(), state
        )

        results = [
            assert_convergence(hashes),
            assert_uniqueness_email(state),
            idempotent,
            preservation,
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
    cell_level_run: ScenarioReport | None = None,
) -> dict[str, Any]:
    axis_pass: dict[str, bool] = {}

    for r in reference.assertions:
        key = "fk" if r.name.startswith("fk:") else r.name
        axis_pass[key] = r.passed

    if cell_level_run is not None:
        for r in cell_level_run.assertions:
            if r.name == "cell-level-strict":
                axis_pass["cell-level-strict"] = r.passed
            # cell-level scenario also asserts convergence — only override
            # if the main reference scenario failed it.
            if r.name == "convergence" and not axis_pass.get("convergence", True):
                pass  # keep the reference's failed result

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


def stretch_score(stretch_runs: list[ScenarioReport]) -> dict[str, Any]:
    """Score the L3 stretch run. Each scenario is one axis; the axis
    passes only if EVERY assertion in that scenario passes. The total
    is the weighted sum of passed axes (max 1.0).
    """
    per_scenario: dict[str, bool] = {}
    for run in stretch_runs:
        name = run.scenario.split("stretch:", 1)[-1]
        per_scenario[name] = all(a.passed for a in run.assertions)
    weighted = sum(
        STRETCH_WEIGHTS.get(name, 0.0)
        for name, passed in per_scenario.items() if passed
    )
    return {
        "axes": per_scenario,
        "weighted_score": round(weighted, 4),
        "max": round(sum(STRETCH_WEIGHTS.values()), 4),
    }


def render(reports: list[ScenarioReport], score: dict[str, Any]) -> str:
    return json.dumps(
        {
            "score": score,
            "scenarios": [asdict(r) for r in reports],
        },
        indent=2,
        default=str,
    )
