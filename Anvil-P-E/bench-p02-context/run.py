"""
P-02 benchmark runner.

Usage:
    python run.py --adapter adapters.dummy:DummyAdapter
    python run.py --adapter adapters.team_x:Engine --mode deep --seed 7 --out report.json
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys

from generator import GenConfig
from harness import run


def adapter_factory_from_spec(spec: str):
    module_name, class_name = spec.split(":")
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return lambda: cls()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Anvil P-02 benchmark")
    ap.add_argument("--adapter", required=True,
                    help="module:Class, e.g. adapters.dummy:DummyAdapter")
    ap.add_argument("--mode", choices=["fast", "deep"], default="fast")
    ap.add_argument("--seeds", type=int, nargs="+", default=[42, 101, 202, 303, 404],
                    help="One or more generator seeds. Run any integer.")
    ap.add_argument("--n-services", type=int, default=12)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--warmup", type=int, default=2,
                    help="Warmup queries per seed, excluded from latency.")
    ap.add_argument("--out", default="-")
    args = ap.parse_args(argv)

    cfg = GenConfig(
        seed=args.seeds[0],
        n_services=args.n_services,
        days=args.days,
    )
    factory = adapter_factory_from_spec(args.adapter)
    report = run(factory, cfg, mode=args.mode, seeds=args.seeds, warmup=args.warmup)

    payload = json.dumps(report, indent=2, default=str)
    if args.out == "-":
        print(payload)
    else:
        with open(args.out, "w") as f:
            f.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
