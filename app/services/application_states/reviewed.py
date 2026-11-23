from typing import Any

from .base import ApplicationState


class ReviewedState(ApplicationState):
    name = "reviewed"

    def transition(self, action: str) -> str:
        if action == "shortlist":
            return "shortlisted"
        if action == "reject":
            return "rejected"
        self._invalid(action)

    def shortlist(self, app: Any) -> None:
        app.status = "shortlisted"

    def reject(self, app: Any) -> None:
        app.status = "rejected"
