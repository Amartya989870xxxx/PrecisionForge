"""
Adapter interface for P-02 (Persistent Context Engine) submissions.

Every submission must provide a concrete Adapter wrapping its engine.
For non-Python engines, the adapter bridges via subprocess / gRPC / HTTP.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Literal

from schema import Context, Event, IncidentSignal


class Adapter(ABC):
    @abstractmethod
    def ingest(self, events: Iterable[Event]) -> None:
        """Consume a stream of telemetry events."""

    @abstractmethod
    def reconstruct_context(
        self,
        signal: IncidentSignal,
        mode: Literal["fast", "deep"] = "fast",
    ) -> Context:
        """Synthesise operational context for the given incident signal."""

    @abstractmethod
    def close(self) -> None:
        """Tear down."""
