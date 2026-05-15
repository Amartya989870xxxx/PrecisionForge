"""
Adapter interface for P-01 (CRDT-Native OLTP) submissions.

Every submission must provide a concrete Adapter that wraps its engine.
The benchmark harness drives all operations through this interface.

For non-Python engines, write a thin Python adapter that bridges via
subprocess, gRPC, or HTTP to your real implementation.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Adapter(ABC):
    """Subclass in adapters/<your_team>.py."""

    @abstractmethod
    def open_peer(self, peer_id: str) -> None:
        """Initialise an independent peer with the given id. Empty state."""

    @abstractmethod
    def apply_schema(self, peer_id: str, stmts: list[str]) -> None:
        """Apply DDL statements to a peer."""

    @abstractmethod
    def execute(self, peer_id: str, sql: str, params: tuple[Any, ...] = ()) -> None:
        """Execute a single DML statement locally on a peer. No sync."""

    @abstractmethod
    def sync(self, peer_a: str, peer_b: str) -> None:
        """Pairwise bidirectional sync. After return, both peers reflect
        the union of each other's known state per the engine's merge semantics."""

    @abstractmethod
    def snapshot_hash(self, peer_id: str) -> str:
        """Deterministic hex hash of the peer's full state. Used for convergence."""

    @abstractmethod
    def snapshot_state(self, peer_id: str) -> dict[str, list[dict[str, Any]]]:
        """Peer state as {table_name: [row_dict, ...]} ordered deterministically by PK.
        Rows must be the engine's *visible* live state — tombstones excluded
        unless the engine's stated FK policy requires their visibility."""

    @abstractmethod
    def close(self) -> None:
        """Tear down all peer state and release resources."""
