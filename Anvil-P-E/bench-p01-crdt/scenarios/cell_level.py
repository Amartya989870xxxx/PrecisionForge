"""
Cell-level merge scenario (non-vacuous).

Pure test of the engine's per-column merge semantics. No foreign-key
conflicts, no uniqueness conflicts — every peer agrees on which row
exists. The ONLY thing being tested is whether concurrent UPDATEs on
different columns of the same row are BOTH preserved at merge.

LWW (last-writer-wins-on-row) implementations replace the entire row
with whichever sync arrives last, losing one of the two updates. Real
cell-level CRDTs (multi-value registers per column) preserve both.

The dummy SQLite-with-INSERT-OR-REPLACE adapter fails this scenario by
construction — that's the point.
"""
from __future__ import annotations

from .reference import Stmt, Sync, SCHEMA, PEERS


# Setup: A creates users, distributes them. Then all three peers agree on
# the row contents. After this point, no INSERTs and no DELETEs — just
# concurrent UPDATEs on different columns of the SAME row.
OPERATIONS = [
    Stmt("A", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("u1", "alice@x.com", "Alice")),
    Stmt("A", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("u2", "bob@x.com", "Bob")),

    # Distribute the rows to everyone.
    Sync("A", "B"),
    Sync("A", "C"),
    Sync("B", "C"),

    # Concurrent column updates on u1. A updates name; B updates email.
    # No conflict on the row's existence — just on which column got the
    # newer value. A correct CRDT preserves BOTH.
    Stmt("A", "UPDATE users SET name  = ? WHERE id = ?", ("Alice Cooper", "u1")),
    Stmt("B", "UPDATE users SET email = ? WHERE id = ?", ("alice@ex.org",  "u1")),
]

FINAL_SYNC_ORDER = [
    ("A", "B"), ("B", "C"), ("A", "C"),
    ("A", "B"), ("B", "C"), ("A", "C"),
]
