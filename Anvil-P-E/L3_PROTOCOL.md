# Anvil · L3 Final Benchmark — Submission Protocol

There is **one** bench per problem statement. Running it is the L3 evaluation. The output is what you submit.

## Run it

### P-01 · CRDT-Native OLTP
```bash
cd bench-p01-crdt
pip install -r requirements.txt
python run.py \
  --adapter adapters.myteam:Engine \
  --fk-policy <cascade|tombstone|orphan> \
  --out l3_report.json
```

### P-02 · Persistent Context Engine
```bash
cd bench-p02-context
pip install -r requirements.txt
python run.py \
  --adapter adapters.myteam:Engine \
  --out l3_report.json
```

That's the whole protocol. The script announces itself with a multi-line banner showing the L3 version string — judges look for this in your demo video to confirm you ran the right bench.

## Submit it

Paste the entire contents of `l3_report.json` into the submission form's L3 Output field. The report contains:
- `l3_version`     — must match the council release ID
- `timestamp`      — when you ran it
- `adapter`        — module:Class of your engine
- `l3_final_score` — the headline number
- `scenarios`      — per-scenario state samples and snapshot hashes for council spot-check

## Demo video requirement

Your demo video must include a shot of the terminal showing the L3 final banner — both the open banner (with the version string) and the close banner (with your final score). If the banner is not visible, the submission cannot be authenticated.

## What gets scored

L3 is the headline number. There is no L1/L2 partial credit anymore — the bench runs the full L3 evaluation in a single pass.

| Problem | L3 contents | Final score weight |
|---|---|---|
| P-01 | reference + cell-level-strict + chaos + randomized + composite-uniqueness + multi-level-FK + high-density + long-run | Composite: 60% core invariants, 40% stretch |
| P-02 | Multi-seed eval with stretch generator (30 services, 21 days, cascading renames, 20% decoys, 8 families) | Weighted sum of recall, precision, remediation, latency |

## Anti-fabrication

The L3 report contains state samples and snapshot hashes that the council uses to spot-check authenticity. Submissions that score implausibly high will be re-run by judges; if the council's re-run produces materially different numbers, the submission is disqualified.

## Timeline

| Time | Event |
|---|---|
| T-2h | Council pushes the final L3 release to the `main` branch of the repo |
| T-2h → T-0 | Pull, run `python run.py …`, paste `l3_report.json` into the form |
| T-0 | Submission closes |
