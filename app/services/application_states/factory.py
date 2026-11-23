from .base import ApplicationState
from .submitted import SubmittedState
from .reviewed import ReviewedState
from .shortlisted import ShortlistedState
from .rejected import RejectedState
from .hired import HiredState


class ApplicationStateFactory:
    """Maps a stored status string to its state object."""

    _states: dict[str, ApplicationState] = {
        s.name: s
        for s in (
            SubmittedState(),
            ReviewedState(),
            ShortlistedState(),
            RejectedState(),
            HiredState(),
        )
    }

    @classmethod
    def create(cls, status: str) -> ApplicationState:
        try:
            return cls._states[status]
        except KeyError:
            raise ValueError(f"unknown application status: {status!r}") from None

    @classmethod
    def from_status(cls, status: str) -> ApplicationState:
        return cls.create(status)
