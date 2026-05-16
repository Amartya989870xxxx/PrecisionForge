"""
Long-run stress scenario.

A randomized 1500-op trace across 4 peers with high email-collision
density (every other insert reuses an email from a small common pool).
After execution, the engine must:
  - Converge to bit-identical state across all peers
  - Preserve every inserted id (present, deleted, or cascaded —
    no silent drops to satisfy UNIQUE)
  - Achieve idempotent sync (a second sync pass is a no-op)

Engines whose sync metadata grows per-write rather than per-writer
will hit memory pressure here; engines using INSERT-OR-REPLACE-style
silent drops fail data preservation immediately.

This scenario is parameterised by the L3 config so the council can
swap seeds and op-counts at evaluation time.
"""
from __future__ import annotations

import random
from typing import Any

from ..reference import SCHEMA as REF_SCHEMA, Stmt, Sync


SCHEMA = REF_SCHEMA
PEERS = ["P0", "P1", "P2", "P3"]


def _build_trace(seed: int = 31415,
                 n_ops: int = 1500,
                 p_sync: float = 0.18,
                 p_email_collision: float = 0.35,
                 p_delete: float = 0.06,
                 p_update: float = 0.25) -> tuple[list, list[tuple[str, str]], set[str], set[str]]:
    rng = random.Random(seed)
    common_emails = ["admin@x.com", "root@x.com", "alice@x.com", "bob@x.com"]
    known: dict[str, list[str]] = {p: [] for p in PEERS}
    inserted: set[str] = set()
    deleted: set[str] = set()
    next_uid = 0
    ops: list = []

    for _ in range(n_ops):
        if rng.random() < p_sync and len(PEERS) >= 2:
            a, b = rng.sample(PEERS, 2)
            ops.append(Sync(a, b))
            continue
        peer = rng.choice(PEERS)
        roll = rng.random()

        if roll < p_delete and known[peer]:
            uid = rng.choice(known[peer])
            ops.append(Stmt(peer, "DELETE FROM users WHERE id = ?", (uid,)))
            known[peer] = [u for u in known[peer] if u != uid]
            deleted.add(uid)
        elif roll < p_delete + p_update and known[peer]:
            uid = rng.choice(known[peer])
            col = "name" if rng.random() < 0.5 else "email"
            val = (f"name-{rng.randint(0, 99999)}" if col == "name"
                   else f"e{rng.randint(0, 99999)}@x.com")
            ops.append(Stmt(
                peer,
                f"UPDATE users SET {col} = ? WHERE id = ?",
                (val, uid),
            ))
        else:
            uid = f"u{next_uid}"
            next_uid += 1
            email = (rng.choice(common_emails)
                     if rng.random() < p_email_collision
                     else f"e{rng.randint(0, 999999)}@x.com")
            ops.append(Stmt(
                peer,
                "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
                (uid, email, f"name-{rng.randint(0, 999)}"),
            ))
            known[peer].append(uid)
            inserted.add(uid)

    sync_tail = []
    for _ in range(3):  # extra rounds for the high-density trace
        for i in range(len(PEERS)):
            for j in range(i + 1, len(PEERS)):
                sync_tail.append((PEERS[i], PEERS[j]))

    return ops, sync_tail, inserted, deleted


# Default trace (seed=31415, 1500 ops). Council overrides via L3 config.
OPERATIONS, FINAL_SYNC, INSERTED_IDS, DELETED_IDS = _build_trace()


def run_assertions(state: dict[str, Any], hashes: dict[str, str]) -> list:
    from assertions import (
        assert_convergence,
        assert_data_preservation,
        assert_uniqueness_email,
    )

    return [
        assert_convergence(hashes),
        assert_uniqueness_email(state),
        assert_data_preservation(
            INSERTED_IDS, DELETED_IDS, set(), state, table="users",
        ),
    ]


def rebuild_with_seed(seed: int, n_ops: int = 1500) -> None:
    """Council/L3 hook: regenerate the trace under a fresh seed before
    `run_stretch_scenario` is called.
    """
    global OPERATIONS, FINAL_SYNC, INSERTED_IDS, DELETED_IDS
    OPERATIONS, FINAL_SYNC, INSERTED_IDS, DELETED_IDS = _build_trace(
        seed=seed, n_ops=n_ops,
    )
