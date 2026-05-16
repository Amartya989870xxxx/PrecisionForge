"""
ANVIL · P-01 · L3 Final Benchmark Runner

This is the ONLY bench. There is no L1/L2/L3 selector. Running this
script IS the L3 evaluation. The output is what participants submit.

Usage:
    python run.py --adapter adapters.myteam:Engine --fk-policy tombstone --out l3_report.json

The output JSON must be pasted into the submission form. The output
prints a council-verifiable banner that judges look for in demo videos.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import time
from dataclasses import asdict

from harness import (
    STRETCH_WEIGHTS,
    WEIGHTS,
    compute_score,
    run_cell_level,
    run_chaos,
    run_randomized,
    run_reference,
    run_stretch_all,
    run_stretch_scenario,
    stretch_score,
)
from scenarios.stretch import REGISTRY as STRETCH_REGISTRY
from scenarios.stretch import long_run as _long_run_module


L3_VERSION = "anvil-2026-p01-L3-final"


# =====================================================================
# COUNCIL: Replace these seed lists at T-2h with the L3 release values.
# Participants pulling the repo at T-2h will get the updated seeds and
# their bench-maxxing precomputations against the public seeds become
# worthless. Keep the names — the harness imports them by name.
# =====================================================================
L3_CHAOS_SEEDS      = [1, 2, 3, 5, 8]
L3_RANDOMIZED_SEEDS = [101, 202, 303, 404, 505, 606, 707, 808]
L3_LONG_RUN_SEEDS   = [31415, 27182]
L3_LONG_RUN_OPS     = 1500
# =====================================================================


# --------------------------------------------------------------------------- #
# Visual banners — designed for video identification.
# --------------------------------------------------------------------------- #

def _banner_open() -> str:
    bar = "█" * 70
    star = "★" * 3
    return "\n".join([
        "",
        bar,
        bar,
        f"{star}     A N V I L   ·   P - 0 1   ·   L 3   F I N A L   B E N C H     {star}",
        f"{star}     Council Release · {L3_VERSION:<32}     {star}",
        f"{star}     {time.strftime('%Y-%m-%d %H:%M:%S %z'):<58}{star}",
        bar,
        bar,
        "",
    ])


def _banner_close(score_value: float, score_max: float) -> str:
    bar = "█" * 70
    star = "★" * 3
    pct = (score_value / score_max * 100) if score_max else 0.0
    return "\n".join([
        "",
        bar,
        bar,
        f"{star}     A N V I L   ·   P - 0 1   ·   L 3   F I N A L   S C O R E     {star}",
        f"{star}     {score_value:>6.4f}  /  {score_max:.4f}    ({pct:>5.1f} %)         {star}",
        f"{star}     {L3_VERSION:<58}{star}",
        bar,
        bar,
        "",
    ])


# --------------------------------------------------------------------------- #
# Adapter loading
# --------------------------------------------------------------------------- #

def load_adapter(spec: str) -> tuple[object, str, str]:
    """Load adapter and return (instance, module_path, source_sha256).

    The source hash is included in the report so the council can verify
    that the submitted adapter source matches what was actually run.
    """
    import hashlib
    module_name, class_name = spec.split(":")
    module = importlib.import_module(module_name)
    try:
        source_path = module.__file__ or "<unknown>"
        with open(source_path, "rb") as f:
            source = f.read()
        source_hash = hashlib.sha256(source).hexdigest()
    except Exception:
        source_path = "<unknown>"
        source_hash = "<unhashable>"
    return getattr(module, class_name)(), source_path, source_hash


# --------------------------------------------------------------------------- #
# Final L3 run
# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Anvil · P-01 · L3 final benchmark (single mode, single output)",
    )
    ap.add_argument("--adapter", required=True,
                    help="module:Class, e.g. adapters.myteam:Engine")
    ap.add_argument("--fk-policy", choices=["cascade", "tombstone", "orphan"],
                    required=True,
                    help="Your engine's declared FK-under-partition policy.")
    ap.add_argument("--chaos-seeds", type=int, nargs="+",
                    default=L3_CHAOS_SEEDS,
                    help="Seeds for the order-invariance check.")
    ap.add_argument("--randomized-seeds", type=int, nargs="+",
                    default=L3_RANDOMIZED_SEEDS,
                    help="Property-based seeds for the randomized check.")
    ap.add_argument("--long-run-seeds", type=int, nargs="+",
                    default=L3_LONG_RUN_SEEDS,
                    help="Seeds for the long_run stress scenario.")
    ap.add_argument("--long-run-ops", type=int, default=L3_LONG_RUN_OPS,
                    help="Op count per long_run scenario.")
    ap.add_argument("--out", default="-",
                    help="Output path. '-' for stdout.")
    args = ap.parse_args(argv)

    # --- OPEN BANNER ---
    sys.stderr.write(_banner_open())
    sys.stderr.write(
        f"  ▸ Adapter:           {args.adapter}\n"
        f"  ▸ FK policy:         {args.fk_policy}\n"
        f"  ▸ Chaos seeds:       {args.chaos_seeds}\n"
        f"  ▸ Randomized seeds:  {args.randomized_seeds}\n"
        f"  ▸ Long-run seeds:    {args.long_run_seeds} (ops={args.long_run_ops})\n\n"
    )
    sys.stderr.flush()

    adapter, adapter_path, adapter_hash = load_adapter(args.adapter)
    sys.stderr.write(
        f"  ▸ Adapter source:    {adapter_path}\n"
        f"  ▸ Adapter SHA-256:   {adapter_hash[:16]}…\n\n"
    )
    sys.stderr.flush()
    try:
        sys.stderr.write("  ▸ Running L3 scenario: REFERENCE                       …\n")
        sys.stderr.flush()
        ref = run_reference(adapter, stated_fk_policy=args.fk_policy)

        sys.stderr.write("  ▸ Running L3 scenario: CELL-LEVEL-STRICT               …\n")
        sys.stderr.flush()
        cell = run_cell_level(adapter)

        sys.stderr.write("  ▸ Running L3 scenario: CHAOS (order-invariance)        …\n")
        sys.stderr.flush()
        chs = run_chaos(adapter, seeds=args.chaos_seeds)

        sys.stderr.write("  ▸ Running L3 scenario: RANDOMIZED (property-based)     …\n")
        sys.stderr.flush()
        rnd = run_randomized(adapter, seeds=args.randomized_seeds)

        sys.stderr.write("  ▸ Running L3 scenario: COMPOSITE UNIQUENESS            …\n")
        sys.stderr.flush()
        s_comp = run_stretch_scenario(adapter, "composite_uniqueness", scope_prefix="L3")

        sys.stderr.write("  ▸ Running L3 scenario: MULTI-LEVEL FK CHAIN            …\n")
        sys.stderr.flush()
        s_mfk = run_stretch_scenario(adapter, "multi_level_fk", scope_prefix="L3")

        sys.stderr.write("  ▸ Running L3 scenario: HIGH-DENSITY UNIQUENESS         …\n")
        sys.stderr.flush()
        s_hd = run_stretch_scenario(adapter, "high_density", scope_prefix="L3")

        long_run_runs = []
        for s in args.long_run_seeds:
            sys.stderr.write(f"  ▸ Running L3 scenario: LONG-RUN STRESS · seed={s}      …\n")
            sys.stderr.flush()
            _long_run_module.rebuild_with_seed(s, args.long_run_ops)
            long_run_runs.append(run_stretch_scenario(
                adapter, "long_run", scope_prefix=f"L3:lr-{s}",
            ))

        stretch_runs = [s_comp, s_mfk, s_hd] + long_run_runs
    finally:
        adapter.close()

    core_score = compute_score(ref, chs, rnd, cell_level_run=cell)
    s_score = stretch_score(stretch_runs)

    # Composite final score: 60% core (L1/L2 invariants) + 40% stretch (L3 hard)
    final = round(
        0.6 * core_score["weighted_score"] + 0.4 * s_score["weighted_score"],
        4,
    )

    report = {
        "l3_version":    L3_VERSION,
        "timestamp":     time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "adapter":       args.adapter,
        "adapter_path":  adapter_path,
        "adapter_sha256": adapter_hash,
        "fk_policy":     args.fk_policy,
        "seeds": {
            "chaos":     args.chaos_seeds,
            "randomized": args.randomized_seeds,
            "long_run":  args.long_run_seeds,
            "long_run_ops": args.long_run_ops,
        },
        "core_score":    core_score,
        "stretch_score": s_score,
        "l3_final_score": {
            "value": final,
            "max":   1.0,
            "weights": {"core": 0.6, "stretch": 0.4},
        },
        "scenarios": [asdict(r) for r in
                      ([ref, cell] + chs + rnd + stretch_runs)],
    }

    payload = json.dumps(report, indent=2, default=str)
    if args.out == "-":
        print(payload)
    else:
        with open(args.out, "w") as f:
            f.write(payload)

    # --- CLOSE BANNER ---
    sys.stderr.write(_banner_close(final, 1.0))
    sys.stderr.flush()

    return 0 if final >= 0.5 else 1


if __name__ == "__main__":
    sys.exit(main())
