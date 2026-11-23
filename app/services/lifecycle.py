"""
Application lifecycle — thin facade over the State Pattern.

Tracks submitted → reviewed → shortlisted → rejected|hired using a status
string *and* four boolean flags, updated through nested conditionals.

This is intentionally hard to extend safely. A State-pattern (or explicit
state machine) refactor is the intended design fix: one state object per
status, with allowed transitions and consistent persistence.
"""

from __future__ import annotations

from typing import Any

from app.services.application_states import (
    ApplicationStateFactory,
    InvalidTransitionError,
)

ACTIONS = (
    "mark_reviewed",
    "shortlist",
    "reject",
    "hire",
)


def apply_action(app: Any, action: str) -> Any:
    """Validate and apply one lifecycle action, mutating only on success."""
    if action not in ACTIONS:
        raise InvalidTransitionError(getattr(app, "status", "unknown"), action)

    current_status = getattr(app, "status", "unknown")
    try:
        state = ApplicationStateFactory.create(current_status)
        new_status = state.transition(action)
    except ValueError:
        raise InvalidTransitionError(current_status, action) from None

    app.status = new_status
    return app
