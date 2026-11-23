import pytest

from app.services.application_states import (
    ApplicationStateFactory,
    InvalidTransitionError,
)


def test_submitted_to_reviewed():
    state = ApplicationStateFactory.create("submitted")
    assert state.transition("mark_reviewed") == "reviewed"


def test_reviewed_to_shortlisted():
    state = ApplicationStateFactory.create("reviewed")
    assert state.transition("shortlist") == "shortlisted"


def test_shortlisted_to_hired():
    state = ApplicationStateFactory.create("shortlisted")
    assert state.transition("hire") == "hired"


def test_submitted_cannot_skip_to_hired():
    state = ApplicationStateFactory.create("submitted")

    with pytest.raises(InvalidTransitionError):
        state.transition("hire")


def test_rejected_is_final():
    state = ApplicationStateFactory.create("rejected")

    with pytest.raises(InvalidTransitionError):
        state.transition("hire")


def test_hired_is_final():
    state = ApplicationStateFactory.create("hired")

    with pytest.raises(InvalidTransitionError):
        state.transition("reject")