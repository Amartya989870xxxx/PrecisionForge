"""
Canonical 3-peer scenario from Annex A of problem statement P-01.

Operations execute in declaration order on the named peer. Sync is
bidirectional and exchanges all known state between two peers.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Union


@dataclass(frozen=True)
class Stmt:
    peer: str
    sql: str
    params: tuple[Any, ...] = ()


@dataclass(frozen=True)
class Sync:
    a: str
    b: str


Op = Union[Stmt, Sync]


SCHEMA: list[str] = [
    """CREATE TABLE users (
         id    TEXT PRIMARY KEY,
         email TEXT NOT NULL UNIQUE,
         name  TEXT
       )""",
    """CREATE TABLE orders (
         id          TEXT PRIMARY KEY,
         user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
         status      TEXT NOT NULL,
         total_cents INTEGER NOT NULL DEFAULT 0
       )""",
    "CREATE INDEX orders_by_user ON orders(user_id, status)",
]


PEERS: list[str] = ["A", "B", "C"]


OPERATIONS: list[Op] = [
    Stmt("A", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("u1", "alice@x.com", "Alice")),
    Stmt("A", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("u2", "bob@x.com", "Bob")),

    Stmt("B", "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
         ("u3", "alice@x.com", "Alice2")),

    Sync("A", "C"),

    Stmt("C", "DELETE FROM users WHERE id = ?", ("u1",)),

    Stmt("A",
         "INSERT INTO orders (id, user_id, status, total_cents) VALUES (?, ?, ?, ?)",
         ("o1", "u1", "pending", 1200)),

    Sync("A", "B"),

    Stmt("A", "UPDATE users SET name  = ? WHERE id = ?", ("Alice Cooper", "u1")),
    Stmt("B", "UPDATE users SET email = ? WHERE id = ?", ("alice@ex.org", "u1")),
]


FINAL_SYNC_ORDER: list[tuple[str, str]] = [
    ("A", "B"), ("B", "C"), ("A", "C"),
    ("A", "B"), ("B", "C"), ("A", "C"),
]
