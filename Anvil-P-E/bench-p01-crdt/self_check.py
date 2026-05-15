"""
Self-check for P-01 participants.

Single entry point you run locally against your adapter. Prints a pass/fail
matrix and an indicative score. No deployment required.

    python self_check.py --adapter adapters.mine:Engine --fk-policy tombstone
"""
from __future__ import annotations

import argparse
import importlib
import sys
import time

from harness import (
    compute_score,
    run_chaos,
    run_randomized,
    run_reference,
)


def load_adapter(spec: str):
    mod, cls = spec.split(":")
    return getattr(importlib.import_module(mod), cls)()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="P-01 self-check")
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--fk-policy", choices=["cascade", "tombstone", "orphan"], required=True)
    ap.add_argument("--quick", action="store_true",
                    help="Fewer seeds for fast iteration during dev.")
    args = ap.parse_args(argv)

    chaos_seeds = [1, 2] if args.quick else [1, 2, 3, 5, 8]
    rand_seeds = [101, 202] if args.quick else [101, 202, 303, 404, 505, 606, 707, 808]

    adapter = load_adapter(args.adapter)
    t0 = time.monotonic()
    try:
        ref = run_reference(adapter, stated_fk_policy=args.fk_policy)
        chs = run_chaos(adapter, seeds=chaos_seeds)
        rnd = run_randomized(adapter, seeds=rand_seeds)
    finally:
        adapter.close()
    total_ms = (time.monotonic() - t0) * 1000.0

    score = compute_score(ref, chs, rnd)

    print()
    print("ANVIL · P-01 · CRDT-Native OLTP — Self-Check")
    print("=" * 60)
    print(f"  total wall time   {total_ms:>10.1f} ms")
    print(f"  reference         {ref.duration_ms:>10.1f} ms")
    print(f"  chaos seeds       {len(chs):>10d}")
    print(f"  random seeds      {len(rnd):>10d}")
    print()
    print("  AXIS                          PASS    WEIGHT")
    print("  " + "-" * 50)
    for axis, ok in score["axes"].items():
        w = {
            "convergence": 0.30,
            "uniqueness:users.email": 0.20,
            "fk": 0.15,
            "cell-level:u1": 0.10,
            "order-invariance": 0.10,
            "randomized": 0.15,
        }.get(axis, 0.0)
        mark = "PASS" if ok else "FAIL"
        print(f"  {axis:<30s}{mark:>6s}  {w:>6.2f}")
    print("  " + "-" * 50)
    print(f"  WEIGHTED SCORE              {score['weighted_score']:>6.2f}  / 1.00")
    print()

    # surface first failure for quick debugging
    failed: list[tuple[str, str]] = []
    for r in [ref] + chs + rnd:
        for a in r.assertions:
            if not a.passed:
                failed.append((r.scenario, f"{a.name}: {a.detail}"))
    if failed:
        print("  FIRST FAILURES")
        for scenario, msg in failed[:5]:
            print(f"    [{scenario}] {msg}")
        print()

    return 0 if all(score["axes"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
