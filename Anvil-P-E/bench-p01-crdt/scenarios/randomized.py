"""
Property-based randomized scenarios for P-01.

Generates random operation sequences over N peers and verifies CRDT
invariants hold for any seed. No fixed expected state is asserted —
only the invariants that ANY conformant CRDT-relational engine must
preserve.

A hardcoded solution cannot pass this. The expected hash is not known
until the scenario runs.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from .reference import Stmt, Sync


@dataclass(frozen=True)
class RandomizedConfig:
    seed: int = 0
    n_peers: int = 4
    n_ops: int = 80
    p_sync: float = 0.20
    p_email_collision: float = 0.15
    p_delete: float = 0.10
    p_update: float = 0.30


def generate(cfg: RandomizedConfig) -> tuple[list[str], list, list[tuple[str, str]]]:
    rng = random.Random(cfg.seed)
    peers = [f"P{i}" for i in range(cfg.n_peers)]
    common_emails = ["alice@x.com", "bob@x.com", "carol@x.com", "dave@x.com"]

    known: dict[str, list[str]] = {p: [] for p in peers}
    next_uid = 0
    ops: list = []

    for _ in range(cfg.n_ops):
        if rng.random() < cfg.p_sync and len(peers) >= 2:
            a, b = rng.sample(peers, 2)
            ops.append(Sync(a, b))
            continue

        peer = rng.choice(peers)
        roll = rng.random()

        if roll < cfg.p_delete and known[peer]:
            uid = rng.choice(known[peer])
            ops.append(Stmt(peer, "DELETE FROM users WHERE id = ?", (uid,)))
            known[peer] = [u for u in known[peer] if u != uid]

        elif roll < cfg.p_delete + cfg.p_update and known[peer]:
            uid = rng.choice(known[peer])
            if rng.random() < 0.5:
                ops.append(Stmt(
                    peer,
                    "UPDATE users SET name = ? WHERE id = ?",
                    (f"name-{rng.randint(0, 99999)}", uid),
                ))
            else:
                ops.append(Stmt(
                    peer,
                    "UPDATE users SET email = ? WHERE id = ?",
                    (f"e{rng.randint(0, 99999)}@x.com", uid),
                ))

        else:
            uid = f"u{next_uid}"
            next_uid += 1
            email = (
                rng.choice(common_emails)
                if rng.random() < cfg.p_email_collision
                else f"e{rng.randint(0, 999999)}@x.com"
            )
            ops.append(Stmt(
                peer,
                "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
                (uid, email, f"name-{rng.randint(0, 999)}"),
            ))
            known[peer].append(uid)

    sync_tail: list[tuple[str, str]] = []
    for _ in range(2):
        for i in range(len(peers)):
            for j in range(i + 1, len(peers)):
                sync_tail.append((peers[i], peers[j]))

    return peers, ops, sync_tail
