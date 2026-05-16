"""
High-density concurrent uniqueness scenario.

Six peers simultaneously INSERT users with the SAME email
('admin@x.com'), each with a distinct primary-key id. The UNIQUE
constraint on `users.email` allows at most one winner.

A correct engine:
  - Converges to a single live row with that email
  - Documents the rest as tombstoned / recoverable
  - Does NOT silently drop rows

LWW + INSERT-OR-REPLACE silently drops 5 of 6 inserts → fails the
data-preservation check. Engines without a real uniqueness escrow
protocol fail this scenario.
"""
from __future__ import annotations

from typing import Any

from ..reference import SCHEMA as REF_SCHEMA, Stmt, Sync


SCHEMA = REF_SCHEMA
PEERS = ["A", "B", "C", "D", "E", "F"]


# Six concurrent inserts on the same email, each with a different id
OPERATIONS = [
    Stmt("A", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("ua", "admin@x.com", "Alice")),
    Stmt("B", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("ub", "admin@x.com", "Bob")),
    Stmt("C", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("uc", "admin@x.com", "Carol")),
    Stmt("D", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("ud", "admin@x.com", "Dave")),
    Stmt("E", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("ue", "admin@x.com", "Eve")),
    Stmt("F", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("uf", "admin@x.com", "Frank")),

    # Some peers also insert non-conflicting rows for context.
    Stmt("A", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("ga", "g.alice@x.com", "Alice-G")),
    Stmt("B", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("gb", "g.bob@x.com", "Bob-G")),
]


FINAL_SYNC = [
    # full pairwise sync pass
    ("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "F"),
    ("B", "C"), ("B", "D"), ("B", "E"), ("B", "F"),
    ("C", "D"), ("C", "E"), ("C", "F"),
    ("D", "E"), ("D", "F"),
    ("E", "F"),
    # second round to settle
    ("A", "B"), ("C", "D"), ("E", "F"),
    ("A", "C"), ("B", "D"), ("E", "A"),
]


INSERTED_IDS = {"ua", "ub", "uc", "ud", "ue", "uf", "ga", "gb"}
DELETED_IDS: set[str] = set()


def run_assertions(state: dict[str, Any], hashes: dict[str, str]) -> list:
    from assertions import (
        AssertionResult,
        assert_convergence,
        assert_data_preservation,
        assert_uniqueness_email,
    )

    results = [
        assert_convergence(hashes),
        assert_uniqueness_email(state),
        assert_data_preservation(
            INSERTED_IDS, DELETED_IDS, set(), state, table="users",
        ),
    ]

    # Also check: exactly one row with email='admin@x.com' (must be the winner).
    users = state.get("users", [])
    admins = [u for u in users if u.get("email") == "admin@x.com"]
    if len(admins) == 1:
        results.append(AssertionResult(
            "uniqueness-winner",
            True,
            f"single winner for admin@x.com: id={admins[0]['id']}",
        ))
    else:
        results.append(AssertionResult(
            "uniqueness-winner",
            False,
            f"{len(admins)} live rows with admin@x.com — uniqueness broken",
        ))

    return results
