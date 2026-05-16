"""
Stretch / L3 scenarios for P-01.

These are the harder, grilled scenarios used in the council-released
L3 benchmark and made available to participants under `--stretch` so
they can self-test their designs against the same shapes.

Each module exposes:
  - SCHEMA       : list of CREATE statements
  - PEERS        : list of peer ids
  - OPERATIONS   : list of Stmt / Sync ops
  - FINAL_SYNC   : list of (peer_a, peer_b) sync pairs to run after ops
  - INSERTED_IDS : set of ids inserted (data-preservation check)
  - DELETED_IDS  : set of ids explicitly deleted
  - run_assertions(state, hashes) -> list[AssertionResult]
"""
from . import composite_uniqueness, high_density, long_run, multi_level_fk

REGISTRY = {
    "composite_uniqueness": composite_uniqueness,
    "multi_level_fk":       multi_level_fk,
    "high_density":         high_density,
    "long_run":             long_run,
}
