"""
Self-check for P-02 participants.

Single entry point you run locally against your adapter. Prints a
compact summary across multiple seeds and an indicative score.
No deployment required, no external services contacted.

    python self_check.py --adapter adapters.mine:Engine
"""
from __future__ import annotations

import argparse
import importlib
import sys
import time

from generator import GenConfig
from harness import run


def adapter_factory_from_spec(spec: str):
    mod, cls = spec.split(":")
    cls_obj = getattr(importlib.import_module(mod), cls)
    return lambda: cls_obj()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="P-02 self-check")
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--mode", choices=["fast", "deep"], default="fast")
    ap.add_argument("--quick", action="store_true",
                    help="Two seeds + small dataset, for fast iteration.")
    args = ap.parse_args(argv)

    if args.quick:
        seeds = [42, 101]
        cfg = GenConfig(seed=42, n_services=6, days=2)
    else:
        seeds = [42, 101, 202, 303, 404]
        cfg = GenConfig(seed=42, n_services=12, days=7)

    factory = adapter_factory_from_spec(args.adapter)
    t0 = time.monotonic()
    report = run(factory, cfg, mode=args.mode, seeds=seeds, warmup=2)
    total_ms = (time.monotonic() - t0) * 1000.0

    agg = report["aggregated"]
    sc = report["score"]
    axes = sc["axes"]

    print()
    print("ANVIL · P-02 · Persistent Context Engine — Self-Check")
    print("=" * 60)
    print(f"  total wall time   {total_ms:>10.1f} ms")
    print(f"  seeds             {len(seeds):>10d}")
    print(f"  signals (sum)     {agg['n_signals_total']:>10d}")
    print(f"  mode              {args.mode:>10s}")
    print()
    print("  METRIC                          VALUE")
    print("  " + "-" * 50)
    print(f"  recall@5                       {agg['recall@5']:>6.3f}")
    print(f"  precision@5_mean               {agg['precision@5_mean']:>6.3f}")
    print(f"  remediation_acc                {agg['remediation_acc']:>6.3f}")
    print(f"  latency_p95_ms (worst seed)    {agg['latency_p95_ms']:>6.2f}")
    print(f"  latency_mean_ms                {agg['latency_mean_ms']:>6.2f}")
    print()
    print("  AXIS (weighted)                 VALUE")
    print("  " + "-" * 50)
    for k, v in axes.items():
        v_str = "(panel)" if v is None else f"{v:>6.3f}"
        print(f"  {k:<30s}  {v_str}")
    print("  " + "-" * 50)
    print(f"  WEIGHTED AUTOMATED            {sc['weighted_score']:>6.3f}"
          f"  / {sc.get('max_automated', 0.80):>4.2f}")
    print()
    print(f"  Manual axes (panel-graded at event) are excluded above.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
