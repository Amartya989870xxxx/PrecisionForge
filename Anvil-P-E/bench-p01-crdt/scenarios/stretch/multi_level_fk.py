"""
Multi-level FK chain scenario.

   organizations  ← users  ← orders

DELETE on an organization must propagate through the chain per the
engine's declared FK policy. The chain consistency assertion runs
regardless of cascade/tombstone/orphan policy — what changes is
*how* the engine documents the descendants of a deleted root.

Engines that only handle one level of FK cascade fail this scenario.
"""
from __future__ import annotations

from typing import Any

from ..reference import Stmt, Sync


SCHEMA = [
    """CREATE TABLE organizations (
         id   TEXT PRIMARY KEY,
         name TEXT NOT NULL
       )""",
    """CREATE TABLE users (
         id     TEXT PRIMARY KEY,
         org_id TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
         email  TEXT NOT NULL UNIQUE
       )""",
    """CREATE TABLE orders (
         id          TEXT PRIMARY KEY,
         user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
         status      TEXT NOT NULL,
         total_cents INTEGER NOT NULL DEFAULT 0
       )""",
    "CREATE INDEX users_by_org    ON users(org_id)",
    "CREATE INDEX orders_by_user  ON orders(user_id)",
]

PEERS = ["A", "B", "C"]


OPERATIONS = [
    # A populates the full chain
    Stmt("A", "INSERT INTO organizations (id, name) VALUES (?, ?)",
         ("org1", "Acme")),
    Stmt("A", "INSERT INTO organizations (id, name) VALUES (?, ?)",
         ("org2", "Beta")),

    Stmt("A", "INSERT INTO users (id, org_id, email) VALUES (?, ?, ?)",
         ("u1", "org1", "alice@acme.com")),
    Stmt("A", "INSERT INTO users (id, org_id, email) VALUES (?, ?, ?)",
         ("u2", "org1", "bob@acme.com")),
    Stmt("A", "INSERT INTO users (id, org_id, email) VALUES (?, ?, ?)",
         ("u3", "org2", "carol@beta.com")),

    Stmt("A", "INSERT INTO orders (id, user_id, status, total_cents) "
              "VALUES (?, ?, ?, ?)", ("o1", "u1", "pending", 1200)),
    Stmt("A", "INSERT INTO orders (id, user_id, status, total_cents) "
              "VALUES (?, ?, ?, ?)", ("o2", "u1", "shipped", 800)),
    Stmt("A", "INSERT INTO orders (id, user_id, status, total_cents) "
              "VALUES (?, ?, ?, ?)", ("o3", "u3", "pending", 4500)),

    # Distribute the chain to B and C.
    Sync("A", "B"),
    Sync("A", "C"),

    # B creates one more user + order on the existing org
    Stmt("B", "INSERT INTO users (id, org_id, email) VALUES (?, ?, ?)",
         ("u4", "org1", "dave@acme.com")),
    Stmt("B", "INSERT INTO orders (id, user_id, status, total_cents) "
              "VALUES (?, ?, ?, ?)", ("o4", "u4", "pending", 2300)),

    # The killer: C deletes the root of the chain.
    Stmt("C", "DELETE FROM organizations WHERE id = ?", ("org1",)),

    # Concurrently, A adds another descendant to the doomed org.
    Stmt("A", "INSERT INTO orders (id, user_id, status, total_cents) "
              "VALUES (?, ?, ?, ?)", ("o5", "u2", "pending", 600)),
]

FINAL_SYNC = [
    ("A", "B"), ("B", "C"), ("A", "C"),
    ("A", "B"), ("B", "C"), ("A", "C"),
]

# org1 and its full descendant set
INSERTED_ORG_IDS = {"org1", "org2"}
DELETED_ORG_IDS = {"org1"}
INSERTED_USER_IDS = {"u1", "u2", "u3", "u4"}
USER_IDS_CASCADED = {"u1", "u2", "u4"}     # children of org1 under cascade
INSERTED_ORDER_IDS = {"o1", "o2", "o3", "o4", "o5"}
ORDER_IDS_CASCADED = {"o1", "o2", "o4", "o5"}  # all referencing u1/u2/u4


def run_assertions(state: dict[str, Any], hashes: dict[str, str]) -> list:
    from assertions import (
        assert_convergence,
        assert_fk_chain_integrity,
        assert_data_preservation,
    )

    return [
        assert_convergence(hashes),
        assert_fk_chain_integrity(state),
        # For cascade engines, every cascaded child must be either absent
        # or documented as tombstoned. We treat cascaded sets as accounted-for.
        assert_data_preservation(
            INSERTED_ORG_IDS, DELETED_ORG_IDS, set(), state, table="organizations",
        ),
        assert_data_preservation(
            INSERTED_USER_IDS, set(), USER_IDS_CASCADED, state, table="users",
        ),
        assert_data_preservation(
            INSERTED_ORDER_IDS, set(), ORDER_IDS_CASCADED, state, table="orders",
        ),
    ]
