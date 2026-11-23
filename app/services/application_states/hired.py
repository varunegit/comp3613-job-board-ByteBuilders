from .base import ApplicationState


class HiredState(ApplicationState):
    """Final state: every action raises InvalidTransitionError."""

    name = "hired"
