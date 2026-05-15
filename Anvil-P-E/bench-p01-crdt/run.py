"""
P-01 benchmark runner.

Usage:
    python run.py --adapter adapters.dummy:DummyAdapter --fk-policy cascade
    python run.py --adapter adapters.team_x:Engine     --fk-policy tombstone --out report.json

Exit code 0 if all axes pass, 1 otherwise.
"""
from __future__ import annotations

import argparse
import importlib
import sys

from harness import (
    compute_score,
    render,
    run_chaos,
    run_randomized,
    run_reference,
)


def load_adapter(spec: str):
    module_name, class_name = spec.split(":")
    module = importlib.import_module(module_name)
    return getattr(module, class_name)()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Anvil P-01 benchmark")
    ap.add_argument(
        "--adapter", required=True,
        help="module:Class, e.g. adapters.dummy:DummyAdapter",
    )
    ap.add_argument(
        "--fk-policy", choices=["cascade", "tombstone", "orphan"], required=True,
        help="Engine's declared FK-under-partition policy. Must match observed state.",
    )
    ap.add_argument(
        "--chaos-seeds", type=int, nargs="+", default=[1, 2, 3, 5, 8],
        help="Seeds for sync-ordering permutation runs over the canonical trace.",
    )
    ap.add_argument(
        "--randomized-seeds", type=int, nargs="+",
        default=[101, 202, 303, 404, 505, 606, 707, 808],
        help="Seeds for property-based randomized scenarios. Use ANY integers.",
    )
    ap.add_argument(
        "--rand-peers", type=int, default=4,
        help="Number of peers in each randomized scenario.",
    )
    ap.add_argument(
        "--rand-ops", type=int, default=80,
        help="Operations per randomized scenario.",
    )
    ap.add_argument(
        "--skip-randomized", action="store_true",
        help="Skip property-based scenarios. Faster, but you only validate L1.",
    )
    ap.add_argument(
        "--out", default="-",
        help="Output path. '-' for stdout.",
    )
    args = ap.parse_args(argv)

    adapter = load_adapter(args.adapter)
    try:
        ref = run_reference(adapter, stated_fk_policy=args.fk_policy)
        chs = run_chaos(adapter, seeds=args.chaos_seeds)
        rnd = (
            []
            if args.skip_randomized
            else run_randomized(
                adapter,
                seeds=args.randomized_seeds,
                n_peers=args.rand_peers,
                n_ops=args.rand_ops,
            )
        )
    finally:
        adapter.close()

    score = compute_score(ref, chs, rnd if rnd else None)
    out = render([ref] + chs + rnd, score)

    if args.out == "-":
        print(out)
    else:
        with open(args.out, "w") as f:
            f.write(out)

    all_pass = all(score["axes"].values())
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
