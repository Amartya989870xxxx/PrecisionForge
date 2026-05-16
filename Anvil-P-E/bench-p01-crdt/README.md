# Anvil · P-01 · L3 Final Benchmark

This is the **only** bench for P-01. Running it is the L3 evaluation. The output is the submission.

## Quickstart

```bash
cd bench-p01-crdt
pip install -r requirements.txt
python run.py \
  --adapter adapters.dummy:DummyAdapter \
  --fk-policy cascade
```

You should see a multi-line banner:

```
██████████████████████████████████████████████████████████████████████
██████████████████████████████████████████████████████████████████████
★★★     A N V I L   ·   P - 0 1   ·   L 3   F I N A L   B E N C H     ★★★
★★★     Council Release · anvil-2026-p01-L3-final              ★★★
★★★     2026-…                                                ★★★
██████████████████████████████████████████████████████████████████████
██████████████████████████████████████████████████████████████████████
```

If you don't see this banner, you're running an outdated copy of the bench. Pull the latest from `main`.

## What it tests

A single `python run.py` invocation runs the full L3 suite:

| Scenario | Tests |
|---|---|
| reference | The canonical 3-peer trace from the problem-statement annex |
| cell-level-strict | Pure concurrent column merge on a row that is never deleted — LWW-on-row physically fails |
| chaos (5 seeds) | Same operations, randomly permuted sync orderings — order-invariance check |
| randomized (8 seeds) | Property-based random traces with data-preservation check |
| composite_uniqueness | `UNIQUE(user_id, team_id)` — kills CRDTs that only handle single-column uniqueness |
| multi_level_fk | `organizations → users → orders` — cascade through 3 FK levels |
| high_density | 6 peers all INSERT the same email — extreme concurrent uniqueness |
| long_run | 1500-op randomized stress + data preservation |

## Final score

The output JSON has `l3_final_score` as the headline number:

```
final = 0.6 × core_score + 0.4 × stretch_score
```

- **core_score**: L1/L2 invariants (reference, cell-level-strict, chaos, randomized)
- **stretch_score**: L3 hard scenarios (composite, multi-fk, high-density, long-run)

Reported on a 0.0 – 1.0 scale.

## Implementing your engine

Subclass `Adapter` in `adapters/<your_team>.py`. Implement:

```python
from adapter import Adapter

class Engine(Adapter):
    def open_peer(self, peer_id):           ...
    def apply_schema(self, peer_id, stmts): ...
    def execute(self, peer_id, sql, params=()): ...
    def sync(self, peer_a, peer_b):         ...
    def snapshot_hash(self, peer_id):       ...
    def snapshot_state(self, peer_id):      ...   # {table: [row_dict, ...]}
    def close(self):                        ...
```

For non-Python engines, the adapter bridges via subprocess / gRPC / HTTP.

## FK policy declaration

Your engine declares one FK-under-partition policy and applies it uniformly:

| Policy | Behaviour |
|---|---|
| `cascade` | Children of a deleted parent are also deleted |
| `tombstone` | Children remain; their `user_id` references a tombstoned row |
| `orphan` | Children remain; their `user_id` is set to NULL or a documented sentinel |

Switching policy mid-run, or picking different policies per table, is disqualifying.

## Constraints

- The bench is **frozen** — you do not modify `pcam_model.py`, `harness.py`, `assertions.py`, or any scenario file.
- Precision matrices and merged states must satisfy the assertions listed in each scenario module.
- One forward pass per query / one merge step per sync — no iterative refinement after observing dynamics.

## Submission

Paste the JSON output into the submission form's L3 Output field. Your demo video must show the L3 banner.

## Anti-cheating

- The output includes per-scenario state samples and snapshot hashes
- The council reserves the right to re-run any submission on judges' machines
- Submissions whose numbers can't be reproduced are disqualified

## Pure stdlib + NumPy. CPU only. No GPU required.
