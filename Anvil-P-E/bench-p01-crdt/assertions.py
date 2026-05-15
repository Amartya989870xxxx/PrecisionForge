"""Invariant checkers for P-01."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class AssertionResult:
    name: str
    passed: bool
    detail: str = ""


def assert_convergence(snapshots: dict[str, str]) -> AssertionResult:
    hashes = set(snapshots.values())
    if len(hashes) == 1:
        return AssertionResult(
            "convergence",
            True,
            f"all peers agree on hash {next(iter(hashes))[:12]}…",
        )
    return AssertionResult(
        "convergence",
        False,
        f"divergent state across peers: {snapshots}",
    )


def assert_uniqueness_email(state: dict[str, list[dict[str, Any]]]) -> AssertionResult:
    users = state.get("users", [])
    emails = [u.get("email") for u in users if u.get("email") is not None]
    if len(emails) == len(set(emails)):
        return AssertionResult(
            "uniqueness:users.email",
            True,
            f"{len(emails)} live emails, all distinct",
        )
    dups = sorted({e for e in emails if emails.count(e) > 1})
    return AssertionResult(
        "uniqueness:users.email",
        False,
        f"duplicate emails after merge: {dups}",
    )


def assert_fk_documented(
    state: dict[str, list[dict[str, Any]]],
    stated_policy: str,
) -> AssertionResult:
    """The engine declares its FK-under-partition policy; this checks the
    observed state matches the declaration.

    Accepted policies:
      - cascade  : o1 is gone (cascaded with u1's delete)
      - tombstone: o1 is present and references a tombstoned user_id
      - orphan   : o1 is present with user_id null or a sentinel
    """
    users = state.get("users", [])
    orders = state.get("orders", [])
    user_ids = {u["id"] for u in users}
    o1 = next((o for o in orders if o["id"] == "o1"), None)

    if stated_policy == "cascade":
        ok = o1 is None
        return AssertionResult(
            "fk:cascade",
            ok,
            "o1 cascaded" if ok else f"o1 still present: {o1}",
        )
    if stated_policy == "tombstone":
        ok = o1 is not None and o1.get("user_id") not in user_ids
        return AssertionResult(
            "fk:tombstone",
            ok,
            f"o1={o1}, live_user_ids={sorted(user_ids)}",
        )
    if stated_policy == "orphan":
        ok = o1 is not None and o1.get("user_id") in (None, "__orphan__")
        return AssertionResult(
            "fk:orphan",
            ok,
            f"o1={o1}",
        )
    return AssertionResult(
        "fk:unknown-policy",
        False,
        f"engine declared unknown FK policy '{stated_policy}'",
    )


def assert_cell_level_merge(state: dict[str, list[dict[str, Any]]]) -> AssertionResult:
    """Concurrent updates to u1.name (peer A) and u1.email (peer B) must
    both be preserved. If u1 was cascaded out, this passes vacuously."""
    users = state.get("users", [])
    u1 = next((u for u in users if u["id"] == "u1"), None)
    if u1 is None:
        return AssertionResult(
            "cell-level:u1",
            True,
            "u1 absent (cascade) — vacuously preserved",
        )
    name_ok = u1.get("name") == "Alice Cooper"
    email_ok = u1.get("email") == "alice@ex.org"
    if name_ok and email_ok:
        return AssertionResult(
            "cell-level:u1",
            True,
            "both concurrent column updates preserved",
        )
    return AssertionResult(
        "cell-level:u1",
        False,
        f"u1={u1}; expected name='Alice Cooper', email='alice@ex.org'",
    )
