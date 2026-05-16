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


def assert_cell_level_strict(state: dict[str, list[dict[str, Any]]]) -> AssertionResult:
    """Non-vacuous version: u1 cannot have been deleted (no DELETE happened
    in this scenario, no cascade applies). Both concurrent column updates
    MUST be present in the merged row.

    This is the killer test for last-writer-wins-on-row implementations,
    which lose one of the two concurrent updates by construction.
    """
    users = state.get("users", [])
    u1 = next((u for u in users if u["id"] == "u1"), None)
    if u1 is None:
        return AssertionResult(
            "cell-level-strict",
            False,
            "u1 absent — but no DELETE was issued and no cascade applies. "
            "The engine has silently dropped a row.",
        )
    name_ok = u1.get("name") == "Alice Cooper"
    email_ok = u1.get("email") == "alice@ex.org"
    if name_ok and email_ok:
        return AssertionResult(
            "cell-level-strict",
            True,
            "both concurrent column updates preserved (real cell-level merge)",
        )
    missing = []
    if not name_ok:
        missing.append(f"name='{u1.get('name')}' (expected 'Alice Cooper')")
    if not email_ok:
        missing.append(f"email='{u1.get('email')}' (expected 'alice@ex.org')")
    return AssertionResult(
        "cell-level-strict",
        False,
        f"u1 preserved but {' and '.join(missing)} — likely LWW-on-row dropped a column update",
    )


def assert_data_preservation(
    inserted_ids: set[str],
    deleted_ids: set[str],
    cascaded_ids: set[str],
    state: dict[str, list[dict[str, Any]]],
    table: str = "users",
) -> AssertionResult:
    """Every INSERTed id must end up in one of three places:
        (a) present in the final `table`, OR
        (b) explicitly DELETEd by some peer, OR
        (c) cascade-deleted because a parent it referenced was deleted.

    Anything else is silent data loss — an INSERT OR REPLACE that
    dropped a row to satisfy a UNIQUE constraint, for instance.
    """
    final_ids = {u["id"] for u in state.get(table, [])}
    unaccounted = inserted_ids - final_ids - deleted_ids - cascaded_ids
    if not unaccounted:
        return AssertionResult(
            "data-preservation",
            True,
            f"all {len(inserted_ids)} inserted ids in `{table}` are accounted for",
        )
    return AssertionResult(
        "data-preservation",
        False,
        f"{len(unaccounted)} ids inserted into `{table}` silently lost: "
        f"{sorted(list(unaccounted))[:6]}{' …' if len(unaccounted) > 6 else ''}",
    )


def assert_fk_chain_integrity(
    state: dict[str, list[dict[str, Any]]],
) -> AssertionResult:
    """For the multi-level FK scenario:
       organizations -> users -> orders
    No user may reference a non-existent org. No order may reference a
    non-existent user (modulo the engine's declared FK policy — for
    cascade engines, deleted-org descendants must be gone).
    """
    orgs = {o["id"] for o in state.get("organizations", [])}
    users = state.get("users", [])
    orders = state.get("orders", [])
    user_ids = {u["id"] for u in users}

    orphan_users = [u["id"] for u in users
                    if u.get("org_id") not in orgs]
    orphan_orders = [o["id"] for o in orders
                     if o.get("user_id") not in user_ids]

    issues = []
    if orphan_users:
        issues.append(f"users referencing deleted orgs: {orphan_users[:5]}")
    if orphan_orders:
        issues.append(f"orders referencing deleted users: {orphan_orders[:5]}")

    if not issues:
        return AssertionResult(
            "fk-chain-integrity",
            True,
            f"chain consistent · {len(orgs)} orgs, {len(users)} users, "
            f"{len(orders)} orders",
        )
    return AssertionResult(
        "fk-chain-integrity",
        False,
        "; ".join(issues),
    )
