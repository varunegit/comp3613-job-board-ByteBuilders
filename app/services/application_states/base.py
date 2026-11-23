from __future__ import annotations

from typing import Any


class InvalidTransitionError(Exception):
    """Raised when an action is not permitted from the current state."""

    def __init__(self, current: str, action: str) -> None:
        super().__init__(f"cannot {action} an application that is {current}")
        self.current = current
        self.action = action


class ApplicationState:
    """Interface. Every action is invalid unless a subclass overrides it."""

    name: str = ""

    def _invalid(self, action: str) -> None:
        raise InvalidTransitionError(self.name, action)

    def transition(self, action: str) -> str:
        """Return the next status for an action, or raise for invalid actions."""
        self._invalid(action)

    def review(self, app: Any) -> None:
        self._invalid("review")

    def shortlist(self, app: Any) -> None:
        self._invalid("shortlist")

    def reject(self, app: Any) -> None:
        self._invalid("reject")

    def hire(self, app: Any) -> None:
        self._invalid("hire")
