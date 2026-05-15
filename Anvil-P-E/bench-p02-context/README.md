# Anvil P-02 · Persistent Context Engine — Benchmark Harness

Reference benchmark for problem statement **P-02 · Persistent Context Engine for AI SRE**.

Pure Python · stdlib only · no network access · no external dependencies.

## Self-check (run this locally, often)

```bash
cd bench-p02-context
python self_check.py --adapter adapters.mine:Engine
```

Prints aggregated metrics across multiple seeds and an indicative weighted score. Add `--quick` while iterating.

## Full run

```bash
python run.py --adapter adapters.mine:Engine --mode fast --seeds 42 101 202 303 404 --out report.json
```

## Layout

```
schema.py         # Event, IncidentSignal, Context TypedDicts
adapter.py        # the abstract base every submission implements
generator.py      # deterministic synthetic telemetry generator (seedable)
metrics.py        # precision/recall/latency aggregation
harness.py        # multi-seed ingest + query loop + scoring
run.py            # full CLI entry point
self_check.py     # condensed entry point for local iteration
adapters/
  dummy.py        # naive baseline; matches by exact service name only
```

## Anti-gaming · how the benchmark resists hardcoding

Three layers of evaluation. You see L1 and L2; you do not see L3.

**L1 — Worked example.** The single canonical trace from Annex A of the problem statement. Passes are necessary but not sufficient.

**L2 — Property-based multi-seed evaluation.** `--seeds` accepts ANY integers. The generator produces a fully deterministic dataset per seed: services, deploys, topology mutations, recurring incident families with morphed signatures. For an honest engine, **every** seed produces good metrics. A hardcoded lookup table fails for any seed it was not trained on.

The harness runs each seed in a **freshly constructed adapter**. State cannot leak between seeds. In-memory caches do not give a cross-seed signal.

Try arbitrary seeds locally:

```bash
python run.py --adapter adapters.mine:Engine \
  --seeds 9999 31415 27182 16180 11235 --n-services 20 --days 14
```

**L3 — Held-out adversarial scenarios.** The council holds:

- Private seeds at higher parameter values (more services, denser drift, more incident families per dataset).
- Hand-crafted scenarios that the generator alone does not produce — e.g., correlated multi-service outages, cascading rename chains, families whose signature is morphed across both rename and dependency-graph shifts.

L3 runs only at final evaluation. It is never distributed.

## Robustness · what the harness does to ensure clean numbers

- **Per-seed adapter instances.** Cached state, JIT caches, embedding stores — all reset per seed. Eliminates accidental cross-seed leakage as a confound.
- **Warmup queries.** First `--warmup N` queries per seed are discarded from latency aggregation. Cold-start effects do not poison p95.
- **p95 across the worst seed.** Latency budget is enforced against the worst-seed p95, not the mean. Tail behaviour matters.
- **Mean across seeds for quality metrics.** Random good luck on one seed does not inflate the score.

## Writing an adapter

Subclass `Adapter` in `adapters/<your_team>.py` and implement:

| Method | Purpose |
|---|---|
| `ingest(events)` | Consume an iterable of `Event` dicts |
| `reconstruct_context(signal, mode)` | Return a `Context` dict |
| `close()` | Tear down |

See `schema.py` for the exact `Event`, `IncidentSignal`, and `Context` shapes.

For non-Python engines, the adapter bridges via subprocess / gRPC / HTTP.

## Generator

`generator.py` produces a deterministic dataset with:

- **N services** with periodic background metrics (`qps`)
- **Deploys** across the time window
- **Topology mutations** — renames (the central test for drift), plus dependency add/remove
- **Incidents** drawn from **K recurring families**. Each incident is a pattern of (deploy → latency spike → upstream error → signal → remediation). Families repeat across the dataset with morphed signatures — when the involved service has been renamed, the same family looks superficially different.

Train / eval split: 70 / 30 by time. Eval signals are held out; the engine sees pre-signal context but not the remediation, which it must predict.

Defaults are small for fast local runs. Production scale is set by the council at event start via `--n-services`, `--days`, and generator config.

## Metrics

Computed per held-out incident, then aggregated:

| Metric | Definition |
|---|---|
| `recall@5` | Fraction of held-out incidents where a same-family training incident appears in the top-5 `similar_past_incidents` |
| `precision@5_mean` | Average precision of the top-5 `similar_past_incidents` across all held-out incidents |
| `remediation_acc` | Fraction of held-out incidents where the engine suggested the correct remediation action |
| `latency_p95_ms` | p95 of `reconstruct_context` wall-clock latency |
| `latency_mean_ms` | mean of `reconstruct_context` wall-clock latency |

## What is judged

Six axes, weighted (indicative):

| Axis | Weight | Source |
|---|---|---|
| `recall@5` | 0.30 | Automated |
| `precision@5_mean` | 0.15 | Automated |
| `remediation_acc` | 0.20 | Automated |
| `latency_p95_ms` vs budget | 0.15 | Automated — scored as `min(1, budget / p95)` |
| `manual_context` | 0.10 | Panel-graded on a sampled subset |
| `manual_explain` | 0.10 | Panel-graded on `explain` field |

Latency budgets: `fast` mode `≤ 2000 ms`, `deep` mode `≤ 6000 ms`.

Weights are illustrative — the technical council may rebalance before the event.

## The central test: topology drift

Families are anchored to a **canonical service id**, but events on the wire carry the **currently-aliased name** at the time of the event. When a service is renamed mid-dataset, the same incident family appears under different service names in train vs eval. A submission that matches by raw string compare on `service` will fail recall on these cases. The engine must recognise behavioural equivalence across the rename boundary.

## Caveats

- Defaults are scaled down so the dummy adapter completes in seconds. Larger scales are exercised at event time via L3 parameters.
- The dummy adapter exists to validate the harness — it matches by exact service-name only and will score poorly on drift cases. Do not benchmark against it.
- Manual axes (`manual_context`, `manual_explain`) are placeholders in the automated runner; the panel scores them post-hoc on sampled outputs.
