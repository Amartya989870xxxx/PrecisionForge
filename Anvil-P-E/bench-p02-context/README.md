# Anvil · P-02 · L3 Final Benchmark

This is the **only** bench for P-02. Running it is the L3 evaluation. The output is the submission.

## Quickstart

```bash
cd bench-p02-context
pip install -r requirements.txt
python run.py \
  --adapter adapters.dummy:DummyAdapter \
  --out l3_report.json
```

You should see a multi-line banner:

```
██████████████████████████████████████████████████████████████████████
██████████████████████████████████████████████████████████████████████
★★★     A N V I L   ·   P - 0 2   ·   L 3   F I N A L   B E N C H     ★★★
★★★     Council Release · anvil-2026-p02-L3-final              ★★★
★★★     2026-…                                                ★★★
██████████████████████████████████████████████████████████████████████
██████████████████████████████████████████████████████████████████████
  ▸ L3 generator: 30 services · 21 days · 80 topology mutations · 60+25 incidents · 8 families
  ▸ Cascading renames: ON · decoy rate: 20%
  ▸ Seeds: [314159, 271828, 161803, 141421, 173205]
  ▸ Mode: fast

  ▸ Running L3 evaluation across all seeds …
```

If you don't see this banner, you're running an outdated copy of the bench. Pull the latest from `main`.

## What it tests

A single `python run.py` invocation runs the full L3 evaluation across **5 seeds** with the stretch generator config:

- **30 services** with cascading renames (most services renamed 2+ times across the timeline)
- **21 simulated days**
- **80 topology mutations** (~85% renames)
- **60 train + 25 eval incidents** across **8 incident families**
- **20% decoy rate** — eval signals with no matching family; engines that confidently match them lose credit

## Metrics

| Metric | Weight | Description |
|---|---|---|
| `recall@5` | 0.30 | Same-family training incident appears in top-5 (for decoys: NO confident match = correct) |
| `precision@5_mean` | 0.15 | Mean precision of top-5 matches |
| `remediation_acc` | 0.20 | Engine suggested the correct remediation action (5 actions per family: rollback / restart / scale_up / config_change / failover) |
| `latency_p95_ms` vs budget | 0.15 | min(1, budget / worst-seed p95) |
| `manual_context` | 0.10 | Panel-graded on Context Quality |
| `manual_explain` | 0.10 | Panel-graded on `explain` field |

Headline number: weighted automated total (max 0.80) + manual axes (max 0.20) at panel time.

## Implementing your engine

Subclass `Adapter` in `adapters/<your_team>.py`:

```python
from adapter import Adapter
from schema import Event, IncidentSignal, Context

class Engine(Adapter):
    def ingest(self, events): ...
    def reconstruct_context(self, signal, mode="fast") -> Context: ...
    def close(self): ...
```

See `schema.py` for the exact `Event`, `IncidentSignal`, and `Context` shapes.

For non-Python engines, the adapter bridges via subprocess / gRPC / HTTP.

## Decoys

20% of eval signals are decoys — bare `incident_signal` events with no matching family in train. A correct engine returns:
- `similar_past_incidents`: empty OR all with `similarity` below 0.5
- `suggested_remediations`: empty OR all with `confidence` below 0.5

False positives (confidently matching a decoy) score 0 on that incident.

## Cascading renames

The same service can be renamed 2-4 times across the timeline. An engine that handles only one rename hop fails on most renamed-family incidents. Build an alias chain.

## Submission

Paste the JSON output into the submission form's L3 Output field. Your demo video must show the L3 banner.

## Anti-cheating

- The output includes full per-seed metric breakdown
- The council reserves the right to re-run any submission on judges' machines
- Submissions whose numbers can't be reproduced are disqualified

## Pure Python + NumPy. CPU only. No GPU required.
