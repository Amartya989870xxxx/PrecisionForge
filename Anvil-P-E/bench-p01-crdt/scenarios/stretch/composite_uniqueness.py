"""
Composite uniqueness scenario.

Schema enforces UNIQUE(user_id, team_id). Multiple peers attempt to
INSERT memberships with overlapping (user_id, team_id) tuples. A
correct engine must:
  - End with at most one live row per (user_id, team_id)
  - Either tombstone or expose the loser so it is recoverable
    (no silent drops)
  - Converge to identical state across all peers

LWW or single-column-uniqueness CRDTs fail this scenario.
"""
from __future__ import annotations

from typing import Any

from ..reference import Stmt, Sync


SCHEMA = [
    """CREATE TABLE memberships (
         id      TEXT PRIMARY KEY,
         user_id TEXT NOT NULL,
         team_id TEXT NOT NULL,
         role    TEXT NOT NULL,
         UNIQUE(user_id, team_id)
       )""",
    "CREATE INDEX memberships_by_team ON memberships(team_id)",
]

PEERS = ["A", "B", "C", "D"]


OPERATIONS = [
    # Concurrent inserts on the same (u1, t1) pair from three peers.
    Stmt("A", "INSERT INTO memberships (id, user_id, team_id, role) "
              "VALUES (?, ?, ?, ?)", ("m1", "u1", "t1", "admin")),
    Stmt("B", "INSERT INTO memberships (id, user_id, team_id, role) "
              "VALUES (?, ?, ?, ?)", ("m2", "u1", "t1", "member")),
    Stmt("C", "INSERT INTO memberships (id, user_id, team_id, role) "
              "VALUES (?, ?, ?, ?)", ("m3", "u1", "t1", "owner")),

    # Non-conflicting inserts to provide context.
    Stmt("D", "INSERT INTO memberships (id, user_id, team_id, role) "
              "VALUES (?, ?, ?, ?)", ("m4", "u2", "t1", "admin")),
    Stmt("A", "INSERT INTO memberships (id, user_id, team_id, role) "
              "VALUES (?, ?, ?, ?)", ("m5", "u1", "t2", "member")),

    # Sync once to surface the (u1, t1) collision.
    Sync("A", "B"),

    # Now another peer further mutates the conflicting key.
    Stmt("C", "UPDATE memberships SET role = ? WHERE id = ?", ("guest", "m3")),

    # And one peer DELETEs its own row in the conflict — must propagate.
    Stmt("B", "DELETE FROM memberships WHERE id = ?", ("m2",)),
]


FINAL_SYNC = [
    ("A", "B"), ("B", "C"), ("C", "D"),
    ("A", "C"), ("B", "D"), ("A", "D"),
    ("A", "B"), ("B", "C"), ("C", "D"),
]

INSERTED_IDS = {"m1", "m2", "m3", "m4", "m5"}
DELETED_IDS = {"m2"}


def run_assertions(state: dict[str, Any], hashes: dict[str, str]) -> list:
    """Returns a list of AssertionResult objects."""
    from assertions import (
        AssertionResult,
        assert_convergence,
        assert_data_preservation,
    )

    results = [assert_convergence(hashes)]

    memberships = state.get("memberships", [])

    # Composite uniqueness: at most one row per (user_id, team_id)
    seen: dict[tuple[str, str], str] = {}
    duplicates: list[tuple[str, str]] = []
    for r in memberships:
        key = (r.get("user_id"), r.get("team_id"))
        if key in seen:
            duplicates.append(key)
        seen[key] = r.get("id", "?")
    if not duplicates:
        results.append(AssertionResult(
            "composite-uniqueness",
            True,
            f"{len(memberships)} live rows, all (user_id, team_id) pairs distinct",
        ))
    else:
        results.append(AssertionResult(
            "composite-uniqueness",
            False,
            f"composite key collisions present: {sorted(set(duplicates))}",
        ))

    # Data preservation: every inserted id either present or explicitly deleted.
    results.append(assert_data_preservation(
        INSERTED_IDS, DELETED_IDS, set(), state, table="memberships",
    ))

    return results
