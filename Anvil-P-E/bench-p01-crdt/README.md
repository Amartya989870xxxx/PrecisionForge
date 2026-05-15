# Anvil P-01 · CRDT-Native OLTP — Benchmark Harness

Reference benchmark for problem statement **P-01 · Conflict-Free Collaborative OLTP**.

Pure Python · stdlib only · no network access · no external dependencies.

## Self-check (run this locally, often)

```bash
cd bench-p01-crdt
python self_check.py --adapter adapters.mine:Engine --fk-policy tombstone
```

Prints a pass/fail matrix and an indicative weighted score. Add `--quick` while iterating.

## Full run

```bash
python run.py --adapter adapters.mine:Engine --fk-policy tombstone --out report.json
```

Exit code `0` if all axes pass, `1` otherwise.

## Layout

```
adapter.py          # the abstract base every submission implements
assertions.py       # invariant checkers
harness.py          # scenario orchestration + scoring
run.py              # full CLI entry point
self_check.py       # condensed entry point for local iteration
scenarios/
  reference.py      # canonical 3-peer trace (Annex A)
  chaos.py          # randomly-permuted sync orderings
  randomized.py     # property-based random scenarios
adapters/
  dummy.py          # reference adapter; intentionally weak — for harness validation
```

## Anti-gaming · how the benchmark resists hardcoding

Three layers of evaluation. You see L1 and L2; you do not see L3.

**L1 — Canonical scenarios.** The 3-peer trace from Annex A and its sync-permuted twin. Pass these and your engine handles the documented edge cases.

**L2 — Property-based randomized scenarios.** The harness accepts `--randomized-seeds` with ANY integers. The generator produces fresh operation sequences from each seed. The assertions are *invariants* — not fixed expected outputs:

- Convergence: all peers reach the same hash after sync-to-quiescence.
- Uniqueness on `users.email` holds across the merged state.
- Idempotent sync: a second sync pass at quiescence does not change state.

A hardcoded solution passes L1 trivially. It fails L2 immediately because the expected hash is unknown until the scenario runs. **Run with arbitrary seeds locally**:

```bash
python run.py --adapter adapters.mine:Engine --fk-policy tombstone \
  --randomized-seeds 9999 31415 27182 16180 11235 --rand-peers 5 --rand-ops 150
```

If your engine is correct, every seed passes. If it is hardcoded, none do.

**L3 — Held-out adversarial scenarios.** The technical council holds a private set of seeds and hand-crafted edge cases at higher parameter values (more peers, denser conflicts, schema variants). Used only at final evaluation. Not distributed.

## Writing an adapter

Subclass `Adapter` in `adapters/<your_team>.py` and implement:

| Method | Purpose |
|---|---|
| `open_peer(peer_id)` | Initialise a fresh peer with empty state |
| `apply_schema(peer_id, stmts)` | Apply DDL |
| `execute(peer_id, sql, params)` | Local DML (no sync) |
| `sync(peer_a, peer_b)` | Pairwise bidirectional sync |
| `snapshot_hash(peer_id)` | Deterministic hex hash of the peer's visible state |
| `snapshot_state(peer_id)` | `{table: [row_dict, ...]}` ordered by PK |
| `close()` | Tear down |

For non-Python engines, the adapter bridges via subprocess / gRPC / HTTP to your real implementation.

## What is judged

Six axes, each pass/fail per the harness:

| Axis | Indicative weight | Source |
|---|---|---|
| Convergence | 0.30 | All peers reach an identical snapshot hash after the reference trace |
| Uniqueness on `users.email` | 0.20 | No two live rows share an email after merge |
| FK policy adherence | 0.15 | The engine's declared `--fk-policy` matches observed behaviour for `o1` against the deleted parent `u1` |
| Cell-level merge | 0.10 | Concurrent updates to `u1.name` (peer A) and `u1.email` (peer B) are both preserved |
| Order-invariance | 0.10 | The chaos scenario, with permuted sync orderings, produces the same final hash as the canonical run |
| Randomized | 0.15 | All randomized seeds preserve convergence, uniqueness, and idempotent sync |

Weights are illustrative — the technical council may rebalance before the event.

## Scenarios

- **`reference`** — the canonical operation trace from Annex A. Tests uniqueness, FK-under-partition, cell-level merge, convergence.
- **`chaos:seed=<n>`** — same trace, sync orderings permuted by seed. Tests order-invariance.
- **`randomized:seed=<n>:peers=<m>:ops=<k>`** — fresh random op sequence per seed. Tests CRDT invariants on previously-unseen inputs.

## FK policy

Submissions declare their FK-under-partition policy via `--fk-policy {cascade|tombstone|orphan}`:

- `cascade` — `o1` must NOT exist after merge
- `tombstone` — `o1` is present but its `user_id` references a tombstoned row
- `orphan` — `o1` is present with `user_id` set to NULL or a documented sentinel

The harness checks observed state against the declared policy.

## Caveats

- Defaults are small and run in seconds. Wider chaos seed coverage and additional scenarios may be added before the event.
- The dummy adapter exists to validate the harness — it deliberately fails invariants. Do not benchmark against it.
