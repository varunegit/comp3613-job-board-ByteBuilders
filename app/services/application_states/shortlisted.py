from typing import Any

from .base import ApplicationState


class ShortlistedState(ApplicationState):
    name = "shortlisted"

    def transition(self, action: str) -> str:
        if action == "hire":
            return "hired"
        if action == "reject":
            return "rejected"
        self._invalid(action)

    def hire(self, app: Any) -> None:
        app.status = "hired"

    def reject(self, app: Any) -> None:
        app.status = "rejected"
