"""
ANVIL · P-02 · L3 Final Benchmark Runner

This is the ONLY bench. Running this script IS the L3 evaluation.
The output JSON is what participants paste into the submission form.

Usage:
    python run.py --adapter adapters.myteam:Engine --out l3_report.json
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import time
from typing import Any, Callable

import numpy as np

from generator import GenConfig, stretch_config
from harness import run


L3_VERSION = "anvil-2026-p02-L3-final"


# =====================================================================
# COUNCIL: Replace these seeds at T-2h with the L3 release values.
# Participants who precompute against the public seeds become useless
# the moment the seeds change.
# =====================================================================
L3_SEEDS = [314159, 271828, 161803, 141421, 173205]
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
        f"{star}     A N V I L   ·   P - 0 2   ·   L 3   F I N A L   B E N C H     {star}",
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
        f"{star}     A N V I L   ·   P - 0 2   ·   L 3   F I N A L   S C O R E     {star}",
        f"{star}     {score_value:>6.4f}  /  {score_max:.4f}    ({pct:>5.1f} %)         {star}",
        f"{star}     {L3_VERSION:<58}{star}",
        bar,
        bar,
        "",
    ])


# --------------------------------------------------------------------------- #
# Adapter factory
# --------------------------------------------------------------------------- #

def adapter_factory_from_spec(spec: str) -> tuple[Callable[[], Any], str, str]:
    """Returns (factory, source_path, source_sha256)."""
    import hashlib
    module_name, class_name = spec.split(":")
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    try:
        source_path = module.__file__ or "<unknown>"
        with open(source_path, "rb") as f:
            source = f.read()
        source_hash = hashlib.sha256(source).hexdigest()
    except Exception:
        source_path = "<unknown>"
        source_hash = "<unhashable>"
    return (lambda: cls()), source_path, source_hash


# --------------------------------------------------------------------------- #
# Final L3 run
# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Anvil · P-02 · L3 final benchmark (single mode, single output)",
    )
    ap.add_argument("--adapter", required=True,
                    help="module:Class, e.g. adapters.myteam:Engine")
    ap.add_argument("--mode", choices=["fast", "deep"], default="fast")
    ap.add_argument("--seeds", type=int, nargs="+", default=L3_SEEDS,
                    help="L3 generator seeds.")
    ap.add_argument("--warmup", type=int, default=2,
                    help="Warmup queries per seed, excluded from latency.")
    ap.add_argument("--out", default="-")
    args = ap.parse_args(argv)

    # --- OPEN BANNER ---
    sys.stderr.write(_banner_open())
    sys.stderr.flush()

    cfg = stretch_config(seed=args.seeds[0])
    sys.stderr.write(
        f"  ▸ L3 generator: "
        f"{cfg.n_services} services · {cfg.days} days · "
        f"{cfg.topology_mutations} topology mutations · "
        f"{cfg.incidents_train}+{cfg.incidents_eval} incidents · "
        f"{cfg.incident_families} families\n"
        f"  ▸ Cascading renames: ON · decoy rate: {cfg.decoy_rate:.0%}\n"
        f"  ▸ Seeds: {args.seeds}\n"
        f"  ▸ Mode: {args.mode}\n\n"
    )
    sys.stderr.flush()

    factory, adapter_path, adapter_hash = adapter_factory_from_spec(args.adapter)
    sys.stderr.write(
        f"  ▸ Adapter source:    {adapter_path}\n"
        f"  ▸ Adapter SHA-256:   {adapter_hash[:16]}…\n\n"
        "  ▸ Running L3 evaluation across all seeds …\n"
    )
    sys.stderr.flush()
    report = run(
        factory, cfg, mode=args.mode, seeds=args.seeds, warmup=args.warmup,
    )

    report["l3_version"] = L3_VERSION
    report["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    report["adapter"] = args.adapter
    report["adapter_path"] = adapter_path
    report["adapter_sha256"] = adapter_hash
    report["seeds"] = args.seeds

    sc = report["score"]
    final = sc["weighted_score"]
    final_max = sc.get("max_automated", 0.80)

    payload = json.dumps(report, indent=2, default=str)
    if args.out == "-":
        print(payload)
    else:
        with open(args.out, "w") as f:
            f.write(payload)

    # --- CLOSE BANNER ---
    sys.stderr.write(_banner_close(final, final_max))
    sys.stderr.flush()

    return 0


if __name__ == "__main__":
    sys.exit(main())
