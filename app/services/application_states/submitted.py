from typing import Any

from .base import ApplicationState


class SubmittedState(ApplicationState):
    name = "submitted"

    def transition(self, action: str) -> str:
        if action == "mark_reviewed":
            return "reviewed"
        self._invalid(action)

    def review(self, app: Any) -> None:
        app.status = "reviewed"
