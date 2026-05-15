"""
Reference dummy adapter for P-01.

Uses a separate SQLite in-memory database per peer with naive
last-writer-wins sync. This adapter intentionally fails several
invariants — its purpose is to exercise the harness end-to-end and
to demonstrate the failure modes that real submissions must avoid.

Submissions that resemble this approach will score near zero.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from typing import Any

from adapter import Adapter


class DummyAdapter(Adapter):
    def __init__(self) -> None:
        self.peers: dict[str, sqlite3.Connection] = {}

    def open_peer(self, peer_id: str) -> None:
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON")
        self.peers[peer_id] = conn

    def apply_schema(self, peer_id: str, stmts: list[str]) -> None:
        conn = self.peers[peer_id]
        for s in stmts:
            conn.execute(s)
        conn.commit()

    def execute(
        self,
        peer_id: str,
        sql: str,
        params: tuple[Any, ...] = (),
    ) -> None:
        conn = self.peers[peer_id]
        try:
            conn.execute(sql, params)
            conn.commit()
        except sqlite3.IntegrityError:
            pass

    def sync(self, peer_a: str, peer_b: str) -> None:
        for src, dst in [(peer_b, peer_a), (peer_a, peer_b)]:
            state = self.snapshot_state(src)
            for table, rows in state.items():
                for row in rows:
                    cols = ",".join(row.keys())
                    placeholders = ",".join("?" * len(row))
                    self.execute(
                        dst,
                        f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({placeholders})",
                        tuple(row.values()),
                    )

    def snapshot_hash(self, peer_id: str) -> str:
        state = self.snapshot_state(peer_id)
        blob = json.dumps(state, sort_keys=True, default=str).encode()
        return hashlib.sha256(blob).hexdigest()

    def snapshot_state(
        self,
        peer_id: str,
    ) -> dict[str, list[dict[str, Any]]]:
        conn = self.peers[peer_id]
        out: dict[str, list[dict[str, Any]]] = {}
        cur = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = [r[0] for r in cur.fetchall()]
        for t in tables:
            cur = conn.execute(f"SELECT * FROM {t} ORDER BY id")
            cols = [d[0] for d in cur.description]
            out[t] = [dict(zip(cols, r)) for r in cur.fetchall()]
        return out

    def close(self) -> None:
        for c in self.peers.values():
            c.close()
        self.peers.clear()
