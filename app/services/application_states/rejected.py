from .base import ApplicationState


class RejectedState(ApplicationState):
    """Final state: every action raises InvalidTransitionError."""

    name = "rejected"
