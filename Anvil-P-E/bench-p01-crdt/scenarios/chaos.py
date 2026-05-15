"""
Chaos variant: same operation trace, randomly permuted sync orderings.

The merged state must be invariant under sync permutation. Any divergence
indicates a violation of strong eventual consistency.
"""
from __future__ import annotations

import random

from .reference import FINAL_SYNC_ORDER


def permute_sync_order(seed: int) -> list[tuple[str, str]]:
    rng = random.Random(seed)
    base = FINAL_SYNC_ORDER[:]
    rng.shuffle(base)
    base += [("A", "B"), ("B", "C"), ("A", "C")]
    return base
